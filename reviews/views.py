from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Review
from main.models import FoodEntry
from .forms import ReviewForm
from django.http import JsonResponse

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

            # Return a JSON response for AJAX
            return JsonResponse({
                'success': True,
                'rating': review.rating,
                'comment': review.comment,
                'user': review.user.username,  # Include the username of the user
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

