from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import FoodEntry  # Adjust this import based on your project structure

class MainViewsTest(TestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create a FoodEntry object for testing
        self.food_entry = FoodEntry.objects.create(
            name='Test Food',
            street_address='123 Test St',
            location='Test Location',
            food_type='Test Type',
            reviews_rating=4.5,
            number_of_reviews=10,
            comments='Delicious!',
            contact_number='1234567890',
            trip_advisor_url='http://example.com',
            menu_info='Sample Menu'
        )

    def test_show_main(self):
        response = self.client.get(reverse('main:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Food')  # Check if the food entry is in the response

    def test_show_xml(self):
        response = self.client.get(reverse('main:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json(self):
        response = self.client.get(reverse('main:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml_by_id(self):
        response = self.client.get(reverse('main:show_xml_by_id', args=[self.food_entry.id]))  # Ensure to pass the food_entry id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_by_id(self):
        response = self.client.get(reverse('main:show_json_by_id', args=[self.food_entry.id]))  # Ensure to pass the food_entry id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

