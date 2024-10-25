# leaderboards/urls.py

from django.urls import path
from . import views

app_name = 'leaderboards'

urlpatterns = [
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('recommendations/', views.user_recommendations_view, name='recommendations'),
]
