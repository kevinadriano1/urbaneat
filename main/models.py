import uuid
from django.db import models
from django.contrib.auth.models import User

class FoodEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='N/A')  # For the restaurant name
    street_address = models.CharField(max_length=255, default='N/A')  # For the street address
    location = models.CharField(max_length=255, default='N/A')  # For the city and state
    food_type = models.CharField(max_length=255, default='N/A')  # For types of cuisine
    reviews_rating = models.FloatField(default=0.0)  # For the rating (default to 0.0)
    number_of_reviews = models.IntegerField(default=1)  # For the number of reviews (default to 0)
    comments = models.TextField(default='N/A')  # For comments
    contact_number = models.CharField(max_length=50, default='N/A')  # For contact number
    trip_advisor_url = models.URLField(default='N/A')  # For the Trip Advisor URL
    menu_info = models.TextField(default='N/A')  # For menu info
    image_url = models.URLField(max_length = 255, default='N/A') # For image URL
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0) # For the average rating

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.reviews_rating is not None and self.avg_rating == 0.0:
            self.avg_rating = self.reviews_rating