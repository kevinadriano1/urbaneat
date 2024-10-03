import uuid
from django.db import models

class FoodEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food = models.CharField(max_length=255)
    time = models.DateField(auto_now_add=True)
    feelings = models.TextField()
    food_intensity = models.IntegerField()

    @property
    def is_food_strong(self):
        return self.food_intensity > 5