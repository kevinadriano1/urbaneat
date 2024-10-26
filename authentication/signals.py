#This is an added extension of admin_role!
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    # Create 'User' group if it doesn't exist
    Group.objects.get_or_create(name='User')
    
    # Create 'Restaurant Manager' group if it doesn't exist
    Group.objects.get_or_create(name='Restaurant_Manager')
