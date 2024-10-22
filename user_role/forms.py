from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'name', 'birth_date', 'email', 'phone_number', 'class1', "npm"]
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': '+999999999'}),
            'class1': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'npm': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number == '':
            return None 
        return phone_number
