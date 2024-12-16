from django.urls import path
from admin_role.views import edit_restaurant, create_restaurant, delete_restaurant_via_ajax, edit_restaurant_api,\
create_restaurant_api, delete_restaurant_api
app_name = 'admin_role' 
urlpatterns = [
    path('edit_resto/<uuid:id>/', edit_restaurant, name='edit_restaurant'),
    path('create_resto/', create_restaurant, name='create_restaurant'),
    path('delete_resto_ajax/<uuid:id>/', delete_restaurant_via_ajax, name='delete_restaurant_via_ajax'),
    path('edit_resto_api/<uuid:id>/', edit_restaurant_api, name='edit_restaurant_api'),
    path('create_resto_api/', create_restaurant_api, name='create_restaurant_api'),
    path('delete_resto_api/<uuid:id>/', delete_restaurant_api, name='delete_restaurant_api'),

]
