# user_role/forms.py

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'name', 'birth_date', 'email', 'phone_number']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': '+999999999'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number == '':
            return None
        return phone_number

class UserUpdateForm(forms.Form):
    new_username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
        label="New Username"
    )
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
        label="New Password"
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
        label="Confirm New Password"
    )

    def clean_new_username(self):
        new_username = self.cleaned_data.get('new_username')
        if new_username and User.objects.filter(username=new_username).exists():
            raise ValidationError("This username is already taken.")
        return new_username

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password:
            if new_password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")
            else:
                try:
                    # Validate password strength, including checks for "too common" passwords
                    validate_password(new_password)
                except ValidationError as e:
                    # Display all validation errors
                    self.add_error('new_password', e.messages)

        return cleaned_data
