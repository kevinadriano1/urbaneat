from django.db import models
from django.conf import settings

# Create your models here.
from main.models import FoodEntry
from django.contrib.auth.models import User

class Review(models.Model):
    restaurant = models.ForeignKey(FoodEntry, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # Allow null values


    def __str__(self):
        return f'Review for {self.restaurant.name} {self.restaurant.comments}- {self.rating}'

