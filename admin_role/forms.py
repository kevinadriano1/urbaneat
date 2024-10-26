from django.forms import ModelForm
from main.models import FoodEntry

class FoodEntryForm(ModelForm):
    class Meta:
        model = FoodEntry
        fields = [
            "name",
            "street_address",
            "location",
            "food_type",
            "comments",
            "contact_number",
            "trip_advisor_url", 
            "menu_info", 
            "image_url"
        ]
        labels = {
            'trip_advisor_url': 'Restaurant URL',  
            'comments': 'Testimony', 
        }
