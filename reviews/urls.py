from django.urls import path
from reviews.views import restaurant_details, add_review, delete_review, edit_review, restaurant_detail_json, add_review_flutter

app_name = 'review' 

urlpatterns = [
    path('<uuid:pk>/', restaurant_details, name='restaurant_details'),
    path('<uuid:pk>/add_review', add_review, name='add_review'),
    path('<int:pk>/delete/', delete_review, name='delete_review'),
    path('<int:pk>/edit/', edit_review, name='edit_review')  ,
    path('restaurant/<uuid:pk>/', restaurant_detail_json, name='restaurant_detail_json'),
    path('restaurant/<uuid:pk>/add_review_flutter/', add_review_flutter, name='add_review_flutter'),

]
