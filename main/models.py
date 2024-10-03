import uuid
from django.db import models

class FoodEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food = models.CharField(max_length=255)
    time = models.DateField(auto_now_add=True)
    description = models.TextField()
    rating = models.IntegerField()

    @property
    def is_food_strong(self):
        return self.rating > 5