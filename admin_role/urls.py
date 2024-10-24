from django.urls import path
from admin_role.views import edit_restaurant, create_restaurant, delete_restaurant
app_name = 'admin_role' 
urlpatterns = [
    path('edit_resto/<uuid:id>/', edit_restaurant, name='edit_restaurant'),
    path('create_resto/', create_restaurant, name='create_restaurant'),
    path('delete_resto/<uuid:id>', delete_restaurant, name='delete_restaurant'),
]
