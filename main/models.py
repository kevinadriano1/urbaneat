import uuid
from django.db import models
from django.contrib.auth.models import User

class FoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='N/A')  # For the restaurant name
    street_address = models.CharField(max_length=255, default='N/A')  # For the street address
    location = models.CharField(max_length=255, default='N/A')  # For the city and state
    food_type = models.CharField(max_length=255, default='N/A')  # For types of cuisine
    reviews_rating = models.FloatField(default=0.0)  # For the rating (default to 0.0)
    number_of_reviews = models.IntegerField(default=0)  # For the number of reviews (default to 0)
    comments = models.TextField(default='N/A')  # For comments
    contact_number = models.CharField(max_length=50, default='N/A')  # For contact number
    trip_advisor_url = models.URLField(default='N/A')  # For the Trip Advisor URL
    menu_info = models.TextField(default='N/A')  # For menu info
 # For menu info

    @property
    def is_food_strong(self):
        return self.reviews_rating > 5