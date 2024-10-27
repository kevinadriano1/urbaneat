from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from authentication.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
import datetime

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

class AuthenticationTests(TestCase):
    def setUp(self):
        # Check if the group already exists to avoid UNIQUE constraint errors
        self.user_group, created = Group.objects.get_or_create(name='User')
        self.manager_group, created = Group.objects.get_or_create(name='Restaurant_Manager')
        self.user_data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123',
            'group_choice': 'user'
        }
        self.login_data = {
            'username': 'testuser',
            'password': 'password123'
        }
    
    def test_register_user(self):
        response = self.client.post(reverse('auth:register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'group_choice': 'user'  # Ensure you include this field
        })
        
        # Assert the response status code for a successful registration
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        
        # Check if the user has been created successfully
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        # First, register the user
        user = User.objects.create_user(username='testuser', password='password123')
        user.save()

        # Test login functionality
        response = self.client.post(reverse('auth:login'), self.login_data)
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertRedirects(response, reverse('main:show_main'))
        
        # Check if 'last_login' cookie is set
        last_login = self.client.cookies.get('last_login')
        self.assertIsNotNone(last_login)
        self.assertTrue(isinstance(datetime.datetime.fromisoformat(last_login.value), datetime.datetime))

    def test_logout_user(self):
        # Log in a user to test logout functionality
        self.client.login(username='existinguser', password='password123')  # Ensure this user exists in your fixtures
        response = self.client.get(reverse('auth:logout'))  # Call the logout URL
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after logout
        
        # Check if the user is logged out
        self.assertNotIn('sessionid', self.client.cookies)

