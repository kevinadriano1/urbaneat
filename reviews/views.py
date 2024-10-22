from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Review
from main.models import FoodEntry
from .forms import ReviewForm

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
            review.save()
            return redirect('review:restaurant_details', pk=restaurant.pk)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'restaurant': restaurant, 'form': form})

def delete_review(request, pk):
    # Get the review based on the primary key (pk)
    review = get_object_or_404(Review, pk=pk)
    
    # Delete the review
    review.delete()
    
    # Redirect back to the restaurant details page
    return redirect('review:restaurant_details', pk=review.restaurant.pk)
