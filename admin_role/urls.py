from django.urls import path
from admin_role.views import edit_restaurant, create_restaurant, delete_restaurant_via_ajax
app_name = 'admin_role' 
urlpatterns = [
    path('edit_resto/<uuid:id>/', edit_restaurant, name='edit_restaurant'),
    path('create_resto/', create_restaurant, name='create_restaurant'),
    path('delete_resto_ajax/<uuid:id>/', delete_restaurant_via_ajax, name='delete_restaurant_via_ajax'),

]
