from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from main.models import FoodEntry

class ShowMainViewTest(TestCase):
    def setUp(self):
        # Set up the client and create a user
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create sample FoodEntry data
        FoodEntry.objects.create(
            name="The Capital Grille",
            street_address="155 E 42nd St",
            location="New York City, NY",
            food_type="American",
            avg_rating=4.5
        )
        
        # Log the user in
        self.client.login(username='testuser', password='password')
        
    def test_show_main_no_query(self):
        response = self.client.get(reverse('show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('food_entries', response.context)
        self.assertTrue(response.context['food_entries'])  # Food entries should be present
        
    def test_show_main_with_query(self):
        response = self.client.get(reverse('show_main'), {'q': 'Capital'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('food_entries', response.context)
        self.assertTrue(any(entry.name == "The Capital Grille" for entry in response.context['food_entries']))

    def test_show_main_is_manager(self):
        manager_group, created = Group.objects.get_or_create(name='Restaurant_Manager')
        self.user.groups.add(manager_group)
        
        response = self.client.get(reverse('show_main'))
        self.assertTrue(response.context['is_manager'])
        
    def test_show_main_last_login_cookie(self):
        self.client.cookies['last_login'] = '2023-10-27 12:00:00'
        
        response = self.client.get(reverse('show_main'))
        self.assertEqual(response.context['last_login'], '2023-10-27 12:00:00')
