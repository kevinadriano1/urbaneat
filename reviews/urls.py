from django.urls import path
from reviews.views import restaurant_details, add_review, delete_review

app_name = 'review' 

urlpatterns = [
    path('<uuid:pk>/', restaurant_details, name='restaurant_details'),
    path('<uuid:pk>/add_review', add_review, name='add_review'),
    path('<int:pk>/delete/', delete_review, name='delete_review'),
]
