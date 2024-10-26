from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from main.models import FoodEntry
from .forms import FoodEntryForm  # Import your form to use in the tests

class RestaurantManagerViewsTest(TestCase):
    
    def setUp(self):
        # Create a user and assign them to the Restaurant_Manager group
        self.user = User.objects.create_user(username='manager', password='1234pass')
        self.group = Group.objects.get(name='Restaurant_Manager')
        self.user.groups.add(self.group)
        self.client.login(username='manager', password='1234pass')

        # Create a FoodEntry instance for testing edit and delete
        self.restaurant = FoodEntry.objects.create(
            id='123e4567-e89b-12d3-a456-426614174000',
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

    def test_create_restaurant_view_as_manager(self):
        response = self.client.get(reverse('admin_role:create_restaurant'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_restaurant.html')

    def test_create_restaurant_post_success(self):
        response = self.client.post(reverse('admin_role:create_restaurant'), {
            'name': 'New Restaurant',
            'street_address': '456 New St',
            'location': 'New City',
            'food_type': 'New Cuisine',
            'reviews_rating': 4.5,
            'number_of_reviews': 10,
            'comments': 'Awesome!',
            'contact_number': '9876543210',
            'trip_advisor_url': 'http://tripadvisor.com/new',
            'menu_info': 'New menu details',
            'image_url': 'http://newimage.url',
            'avg_rating': 4.5,
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertTrue(FoodEntry.objects.filter(name='New Restaurant').exists())  # Verify the restaurant is created

    def test_create_restaurant_post_invalid(self):
        response = self.client.post(reverse('admin_role:create_restaurant'), {
            'name': '',  # Invalid: empty name
            'street_address': '456 New St',
            'location': 'New City',
            'food_type': 'New Cuisine',
            'reviews_rating': 4.5,
            'number_of_reviews': 10,
            'comments': 'Awesome!',
            'contact_number': '9876543210',
            'trip_advisor_url': 'http://tripadvisor.com/new',
            'menu_info': 'New menu details',
            'image_url': 'http://newimage.url',
            'avg_rating': 4.5,
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the same page

    def test_edit_restaurant_view_as_manager(self):
        response = self.client.get(reverse('admin_role:edit_restaurant', kwargs={'id': self.restaurant.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_restaurant.html')

    def test_edit_restaurant_post_success(self):
        response = self.client.post(reverse('admin_role:edit_restaurant', kwargs={'id': self.restaurant.id}), {
            'name': 'Updated Restaurant',
            'street_address': '789 Updated St',
            'location': 'Updated City',
            'food_type': 'Updated Cuisine',
            'reviews_rating': 4.7,
            'number_of_reviews': 15,
            'comments': 'Updated place!',
            'contact_number': '3216549870',
            'trip_advisor_url': 'http://tripadvisor.com/updated',
            'menu_info': 'Updated menu details',
            'image_url': 'http://updatedimage.url',
            'avg_rating': 4.7,
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.restaurant.refresh_from_db()  # Refresh the restaurant from the database
        self.assertEqual(self.restaurant.name, 'Updated Restaurant')  # Verify the update

    def test_delete_restaurant_success(self):
        response = self.client.post(reverse('admin_role:delete_restaurant_via_ajax', kwargs={'id': self.restaurant.id}))
        self.assertEqual(response.status_code, 200)  # Check for success
        self.assertFalse(FoodEntry.objects.filter(id=self.restaurant.id).exists())  # Ensure the restaurant is deleted

    def tearDown(self):
        # Clean up after each test
        self.restaurant.delete()
        self.user.delete()
