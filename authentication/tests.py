from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model

class AuthenticationViewsTest(TestCase):
    def setUp(self):
        # Membuat grup yang diperlukan
        Group.objects.create(name="User")
        Group.objects.create(name="Restaurant_Manager")

        # Detail akun untuk login testing
        self.credentials = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.user = User.objects.create_user(**self.credentials)

    def test_register_view(self):
        response = self.client.get(reverse('auth:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        # Data untuk simulasi registrasi user
        form_data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'group_choice': 'user'  # Sesuaikan dengan pilihan grup
        }
        response = self.client.post(reverse('auth:register'), form_data)
        self.assertRedirects(response, reverse('auth:login'))

        # Verifikasi user baru dan keanggotaan grup
        new_user = get_user_model().objects.get(username='newuser')
        self.assertTrue(new_user.groups.filter(name='User').exists())

    def test_login_user_view(self):
        # Mengakses halaman login
        response = self.client.get(reverse('auth:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        # Melakukan login dengan kredensial yang ada
        response = self.client.post(reverse('auth:login'), self.credentials, follow=True)
        self.assertRedirects(response, reverse('main:show_main'))
        
        # Verifikasi cookie "last_login" disetel
        self.assertIn('last_login', response.client.cookies)

    def test_logout_user_view(self):
        # Login terlebih dahulu sebelum logout
        self.client.login(username='testuser', password='testpassword')
        
        # Logout user
        response = self.client.get(reverse('auth:logout'))
        self.assertRedirects(response, reverse('auth:login'))
        
        # Verifikasi cookie "last_login" dihapus
        self.assertNotIn('last_login', response.client.cookies)
