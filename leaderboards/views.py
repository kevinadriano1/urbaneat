# leaderboards/views.py

from django.shortcuts import render
from main.models import FoodEntry
from reviews.models import Review
from django.contrib.auth.decorators import login_required
from collections import defaultdict

@login_required
def leaderboard_view(request):
    # Fetch FoodEntry instances where reviews_rating is not null
    restaurants = FoodEntry.objects.exclude(avg_rating__isnull=True).order_by('-avg_rating')

    # Group restaurants by food_type using defaultdict
    leaderboard = defaultdict(list)
    for restaurant in restaurants:
        food_type = restaurant.food_type
        leaderboard[food_type].append(restaurant)

    # Fetch user recommendations
    user = request.user
    high_rated_reviews = Review.objects.filter(user=user, rating__gte=4).select_related('restaurant')
    recommended_restaurants = set(review.restaurant for review in high_rated_reviews)

    recommendations = []
    for restaurant in recommended_restaurants:
        user_review = restaurant.reviews.filter(user=user).first()
        recommendations.append({
            'restaurant': restaurant,
            'user_review': user_review
        })

    # Debugging: Print recommendations
    print(f'Recommendations: {recommendations}')

    context = {
        'leaderboard': dict(leaderboard),
        'recommended_restaurants': recommendations,
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
