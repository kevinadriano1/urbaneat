from django.urls import path
from main.views import show_main
from main.views import show_main, create_food_entry, show_xml

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-food-entry', create_food_entry, name='create_food_entry'),
    path('xml/', show_xml, name='show_xml'),
]