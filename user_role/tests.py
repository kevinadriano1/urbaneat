import os

# Set up Django settings inline
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midterm_project.settings')

import django
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Profile
from .forms import ProfileForm


class UserRoleProfileTests(TestCase):

    def setUp(self):
        self.client = Client()
        
        # Define groups for user roles to avoid IntegrityError
        self.admin_group, created = Group.objects.get_or_create(name='Admin')
        self.user_group, created = Group.objects.get_or_create(name='User')

        # Create users and assign roles
        self.admin_user, created = User.objects.get_or_create(username='admin')
        self.admin_user.set_password('adminpass')
        self.admin_user.groups.add(self.admin_group)
        self.admin_user.save()

        self.regular_user, created = User.objects.get_or_create(username='regular')
        self.regular_user.set_password('userpass')
        self.regular_user.groups.add(self.user_group)
        self.regular_user.save()

        # URL paths for profile and edit profile views
        self.profile_url = reverse('profile')
        self.edit_profile_url = reverse('edit_profile')

    def test_profile_view_access_for_regular_user(self):
        self.client.login(username='regular', password='userpass')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_view_access_for_admin_user(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_edit_profile_creates_profile_if_not_exists(self):
        self.client.login(username='regular', password='userpass')
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Profile.objects.filter(user=self.regular_user).exists())

    def test_edit_profile_updates_profile_data(self):
        Profile.objects.create(user=self.regular_user, name="Initial Name")
        self.client.login(username='regular', password='userpass')
        response = self.client.post(self.edit_profile_url, {
            'name': 'Updated Name',
        })
        self.regular_user.profile.refresh_from_db()
        self.assertEqual(self.regular_user.profile.name, 'Updated Name')
        self.assertRedirects(response, self.profile_url)

