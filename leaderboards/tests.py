# leaderboards/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import FoodEntry
from reviews.models import Review

class LeaderboardViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create FoodEntry instances
        self.food_entry1 = FoodEntry.objects.create(
            name='Pizza Place',
            food_type='Italian',
            avg_rating=4.5
        )
        self.food_entry2 = FoodEntry.objects.create(
            name='Sushi Spot',
            food_type='Japanese',
            avg_rating=4.0
        )
        self.food_entry3 = FoodEntry.objects.create(
            name='Burger Joint',
            food_type='American',
            avg_rating=3.5
        )
        self.food_entry4 = FoodEntry.objects.create(
            name='Empty Rating',
            food_type='Misc',
            avg_rating=0.0  # This should be excluded
        )

        # Create Review instances without 'created_at'
        Review.objects.create(
            user=self.user,
            restaurant=self.food_entry1,
            rating=5,
            comment='Excellent pizza!'
        )
        Review.objects.create(
            user=self.user,
            restaurant=self.food_entry2,
            rating=4,
            comment='Great sushi!'
        )
        Review.objects.create(
            user=self.user,
            restaurant=self.food_entry3,
            rating=3,
            comment='Good burgers.'
        )
        Review.objects.create(
            user=self.user,
            restaurant=self.food_entry4,
            rating=0,
            comment='No rating.'
        )

        self.client = Client()

    def test_leaderboard_view_requires_login(self):
        """Test that leaderboard_view redirects to login if not authenticated."""
        response = self.client.get(reverse('leaderboards:leaderboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login/', response.url)

    def test_leaderboard_view_authenticated(self):
        """Test leaderboard_view with authenticated user."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('leaderboards:leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboards/leaderboard.html')
        
        # Check context data
        leaderboard = response.context['leaderboard']
        recommended_reviews = response.context['recommended_reviews']
        
        # Verify leaderboard excludes entries with avg_rating <= 0.0
        self.assertNotIn('Misc', leaderboard)
        
        # Verify correct grouping by food_type
        self.assertIn('Italian', leaderboard)
        self.assertIn('Japanese', leaderboard)
        self.assertIn('American', leaderboard)
        self.assertEqual(len(leaderboard['Italian']), 1)
        self.assertEqual(len(leaderboard['Japanese']), 1)
        self.assertEqual(len(leaderboard['American']), 1)
        
        # Verify ordering by avg_rating descending
        italian_restaurant = leaderboard['Italian'][0]
        japanese_restaurant = leaderboard['Japanese'][0]
        american_restaurant = leaderboard['American'][0]
        self.assertTrue(italian_restaurant.avg_rating >= japanese_restaurant.avg_rating >= american_restaurant.avg_rating)
        
        # Verify recommended_reviews contains only high-rated reviews (rating >=4)
        self.assertEqual(recommended_reviews.count(), 2)
        for review in recommended_reviews:
            self.assertGreaterEqual(review.rating, 4)

    def test_leaderboard_view_no_high_rated_reviews(self):
        """Test leaderboard_view when user has no high-rated reviews."""
        # Create a new user with no high-rated reviews
        new_user = User.objects.create_user(username='newuser', password='newpass')
        self.client.login(username='newuser', password='newpass')
        response = self.client.get(reverse('leaderboards:leaderboard'))
        self.assertEqual(response.status_code, 200)
        recommended_reviews = response.context['recommended_reviews']
        self.assertEqual(recommended_reviews.count(), 0)

    def test_user_recommendations_view_requires_login(self):
        """Test that user_recommendations_view redirects to login if not authenticated."""
        response = self.client.get(reverse('leaderboards:recommendations'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login/', response.url)

    def test_user_recommendations_view_authenticated(self):
        """Test user_recommendations_view with authenticated user."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('leaderboards:recommendations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboards/user_recommendations.html')
        
        # Check context data
        recommended_restaurants = response.context['recommended_restaurants']
        
        # Should include only restaurants with high-rated reviews by the user
        expected_restaurants = {self.food_entry1, self.food_entry2}
        self.assertEqual(recommended_restaurants, expected_restaurants)

    def test_user_recommendations_view_no_high_rated_reviews(self):
        """Test user_recommendations_view when user has no high-rated reviews."""
        # Create a new user with only low-rated reviews
        new_user = User.objects.create_user(username='lowuser', password='lowpass')
        Review.objects.create(
            user=new_user,
            restaurant=self.food_entry1,
            rating=2,
            comment='Not great.'
        )
        self.client.login(username='lowuser', password='lowpass')
        response = self.client.get(reverse('leaderboards:recommendations'))
        self.assertEqual(response.status_code, 200)
        recommended_restaurants = response.context['recommended_restaurants']
        self.assertEqual(len(recommended_restaurants), 0)
