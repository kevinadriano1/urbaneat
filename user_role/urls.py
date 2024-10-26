from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-username-password/', views.change_username_password, name='change_username_password'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
]