from django.urls import path
from authentication.views import register, login_user, logout_user, login_flutter, register_flutter

app_name = 'auth'  

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('login_flutter/', login_flutter, name='login_flutter'),
    path('register_flutter/', register_flutter, name='register_flutter'),
]