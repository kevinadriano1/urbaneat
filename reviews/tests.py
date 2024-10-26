from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Review
from main.models import FoodEntry
from .forms import ReviewForm

User = get_user_model()

class RestaurantReviewTests(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create a FoodEntry instance
        self.restaurant = FoodEntry.objects.create(
            name='Test Restaurant',
            street_address='123 Test St',
            location='Test City',
            food_type='Test Cuisine',
            reviews_rating=4.0,
            number_of_reviews=0,
            comments='Great place!',
            contact_number='1234567890',
            trip_advisor_url='http://tripadvisor.com',
            menu_info='Test menu',
            image_url='http://image.url',
            avg_rating=0.0
        )

    def test_restaurant_details_view(self):
        response = self.client.get(reverse('review:restaurant_details', kwargs={'pk': self.restaurant.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant_details.html')
        self.assertContains(response, 'Test Restaurant')

    def test_add_review_view(self):
        self.client.login(username='testuser', password='password')  # Log in the user
        response = self.client.post(reverse('review:add_review', kwargs={'pk': self.restaurant.pk}), {
            'rating': 5,
            'comment': 'Excellent food!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), {
            'success': True,
            'rating': 5,
            'comment': 'Excellent food!',
            'user': 'testuser',
            'average_rating': 5.0
        })
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.avg_rating, 5.0)
        self.assertEqual(self.restaurant.number_of_reviews, 1)

    def test_delete_review_view(self):
        self.client.login(username='testuser', password='password')  # Log in the user
        # First, add a review
        review = Review.objects.create(restaurant=self.restaurant, user=self.user, rating=4, comment='Good food!')
        
        response = self.client.post(reverse('review:delete_review', kwargs={'pk': review.pk}))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertFalse(Review.objects.filter(pk=review.pk).exists())  # Ensure review is deleted

    def test_edit_review_view(self):
        self.client.login(username='testuser', password='password')  # Log in the user
        # Create a review to edit
        review = Review.objects.create(restaurant=self.restaurant, user=self.user, rating=4, comment='Good food!')

        response = self.client.post(reverse('review:edit_review', kwargs={'pk': review.pk}), {
            'rating': 5,
            'comment': 'Excellent food!',
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect
        review.refresh_from_db()  # Refresh the review from the database
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Excellent food!')

    def tearDown(self):
        # Clean up after each test
        self.restaurant.delete()
        self.user.delete()
