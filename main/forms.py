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
            "reviews_rating",
            "number_of_reviews",
            "comments",
            "contact_number",
            "trip_advisor_url",
            "menu_info"
        ]  # Use the correct fields from the model

