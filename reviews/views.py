from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Review
from main.models import FoodEntry
from .forms import ReviewForm
from django.http import JsonResponse
from django.db.models import Avg
from django.db.models import Sum, Avg
def restaurant_details(request, pk):
    restaurant = get_object_or_404(FoodEntry, pk=pk)
    reviews = restaurant.reviews.all()  # Using the related_name 'reviews' from the ForeignKey
    return render(request, 'restaurant_details.html', {'restaurant': restaurant, 'reviews': reviews})


def add_review(request, pk):
    restaurant = get_object_or_404(FoodEntry, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = restaurant  # Assign the restaurant to the review
            review.user = request.user  # Set the user as the current logged-in user
            review.save()

            if restaurant.reviews_rating not in [None, 0.0]:
                # Calculate the sum of the existing ratings
                rating_sum = restaurant.reviews.aggregate(Sum('rating'))['rating__sum']
                # Get the average of the existing reviews (this is 'None' if no reviews exist)
                average_rating = restaurant.reviews.aggregate(Avg('rating'))['rating__avg']
                
                if average_rating is not None:
                    # If there are existing reviews, include reviews_rating in the average calculation
                    # We need to add reviews_rating to the sum and divide by the new "total" count of reviews
                    average_rating = (rating_sum + restaurant.reviews_rating) / (restaurant.reviews.count() + 1)
                else:
                    # If no reviews exist, set the average_rating to reviews_rating
                    average_rating = restaurant.reviews_rating
            else:
                # If reviews_rating is None or 0.0, calculate the average from reviews only
                average_rating = restaurant.reviews.aggregate(Avg('rating'))['rating__avg']

            # Update the restaurant's reviews_rating field
            restaurant.avg_rating = average_rating if average_rating is not None else 0.0
            restaurant.number_of_reviews = restaurant.reviews.count()  # Update the number of reviews
            restaurant.save()

            # Return a JSON response for AJAX
            return JsonResponse({
                'success': True,
                'rating': review.rating,
                'comment': review.comment,
                'user': review.user.username, 
                'average_rating': average_rating  
            })
        else:
            # Return a JSON response with errors
            return JsonResponse({'success': False, 'errors': form.errors})

    form = ReviewForm()
    return render(request, 'add_review.html', {'restaurant': restaurant, 'form': form})

def delete_review(request, pk):
    # Get the review based on the primary key (pk)
    review = get_object_or_404(Review, pk=pk)
    
    if review.user == request.user:
        review.delete()
    
    # Redirect back to the restaurant details page
    return redirect('review:restaurant_details', pk=review.restaurant.pk)

def edit_review(request, pk):
    # Get the review based on the primary key (pk)
    review = get_object_or_404(Review, pk=pk)
    
    # Check if the logged-in user is the owner of the review
    if review.user != request.user:
        return redirect('review:restaurant_details', pk=review.restaurant.pk)  # Redirect if not authorized
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)  # Pass the existing review to the form
        if form.is_valid():
            form.save()  # Save the updated review
            return redirect('review:restaurant_details', pk=review.restaurant.pk)
    else:
        form = ReviewForm(instance=review)  # Pre-fill the form with existing review data

    return render(request, 'edit_review.html', {'form': form, 'restaurant': review.restaurant})

from django.http import JsonResponse

def restaurant_detail_json(request, pk):
    restaurant = get_object_or_404(FoodEntry, pk=pk)
    reviews = list(restaurant.reviews.values('id', 'rating', 'comment', 'user__username'))
    data = {
        'id': str(restaurant.id),
        'name': restaurant.name,
        'street_address': restaurant.street_address,
        'location': restaurant.location,
        'food_type': restaurant.food_type,
        'reviews_rating': restaurant.reviews_rating,
        'number_of_reviews': restaurant.number_of_reviews,
        'comments': restaurant.comments,
        'contact_number': restaurant.contact_number,
        'trip_advisor_url': restaurant.trip_advisor_url,
        'menu_info': restaurant.menu_info,
        'image_url': restaurant.image_url,
        'reviews': reviews,
    }
    return JsonResponse(data)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@csrf_exempt  # Disables CSRF protection for this view (use cautiously in production)
def add_review_flutter(request, pk):
    if request.method == 'POST':
        try:
            # Parse JSON body
            data = json.loads(request.body)
            rating = data.get('rating')
            comment = data.get('comment')

            if rating is None or comment is None:
                return JsonResponse({'success': False, 'error': 'Rating and comment are required.'}, status=400)

            # Validate and process the review
            restaurant = get_object_or_404(FoodEntry, pk=pk)
            review = Review(
                restaurant=restaurant,
                user=request.user if request.user.is_authenticated else None,
                rating=float(rating),
                comment=comment,
            )
            review.save()

            # Update the restaurant's average rating
            rating_sum = restaurant.reviews.aggregate(Sum('rating'))['rating__sum'] or 0.0
            average_rating = restaurant.reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0

            restaurant.avg_rating = average_rating
            restaurant.number_of_reviews = restaurant.reviews.count()
            restaurant.save()

            # Return success response
            return JsonResponse({
                'success': True,
                'rating': review.rating,
                'comment': review.comment,
                'user': review.user.username if review.user else 'Anonymous',
                'average_rating': restaurant.avg_rating,
                'number_of_reviews': restaurant.number_of_reviews,
            })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method. Use POST.'}, status=405)


