# leaderboards/views.py

from django.shortcuts import render
from main.models import FoodEntry
from reviews.models import Review
from django.contrib.auth.decorators import login_required
from collections import defaultdict

@login_required
def leaderboard_view(request):
    # Fetch FoodEntry instances with avg_rating greater than 0.0
    restaurants = FoodEntry.objects.filter(avg_rating__gt=0.0).order_by('-avg_rating')

    # Group restaurants by food_type using defaultdict
    leaderboard = defaultdict(list)
    for restaurant in restaurants:
        food_type = restaurant.food_type
        leaderboard[food_type].append(restaurant)

    # Fetch user high-rated reviews (rating >= 4)
    user = request.user
    high_rated_reviews = Review.objects.filter(user=user, rating__gte=4).select_related('restaurant')

    # Prepare recommendations as a list of high-rated reviews
    recommendations = high_rated_reviews

    # Debugging: Print recommendations


    context = {
        'leaderboard': dict(leaderboard),
        'recommended_reviews': recommendations,  # Updated context variable
    }
    return render(request, 'leaderboards/leaderboard.html', context)


@login_required
def user_recommendations_view(request):
    user = request.user
    # Fetch reviews by the user with high ratings (e.g., 4 and above)
    high_rated_reviews = Review.objects.filter(user=user, rating__gte=4).select_related('restaurant')

    # Extract unique restaurants from these reviews
    recommended_restaurants = set(review.restaurant for review in high_rated_reviews)

    context = {
        'recommended_restaurants': recommended_restaurants,
    }
    return render(request, 'leaderboards/user_recommendations.html', context)
