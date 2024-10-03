from django.forms import ModelForm
from main.models import FoodEntry


class FoodEntryForm(ModelForm):
    class Meta:
        model = FoodEntry
        fields = ["food", "feelings", "food_intensity"]  # Use the correct fields from the model

