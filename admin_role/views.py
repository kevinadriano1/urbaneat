from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from main.models import FoodEntry
from .forms import FoodEntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

# Custom decorator to check if user is in the Restaurant_Manager group
def is_restaurant_manager(user):
    if user.groups.filter(name='Restaurant_Manager').exists():
        return True
    else:
        return False  # User is not in the group

@login_required(login_url='/auth/login/')
def edit_restaurant(request, id):
    if not is_restaurant_manager(request.user):
        return render(request, 'unauthorized.html')  # Redirect to unauthorized page

    # Get the restaurant entry by its id or return a 404 error if not found
    food_entry = get_object_or_404(FoodEntry, id=id)
    
    # Handle form submission
    if request.method == 'POST':
        # Bind form data with the existing food entry object
        form = FoodEntryForm(request.POST, instance=food_entry)
        if form.is_valid():
            # Save the changes to the database
            form.save()
            return HttpResponseRedirect(reverse('main:show_main'))
    else:
        # If it's a GET request, show the form pre-filled with the current data
        form = FoodEntryForm(instance=food_entry)
    
    # Render the edit restaurant form template with the current form and food_entry object
    context = {
        'form': form,
        'food_entry': food_entry,
    }
    return render(request, 'edit_restaurant.html', context)

@login_required(login_url='/auth/login/')
def create_restaurant(request):
    if not is_restaurant_manager(request.user):
        return render(request, 'unauthorized.html')  # Redirect to unauthorized page

    # Handle form submission
    if request.method == 'POST':
        # Create a new form instance with the submitted data
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            # Save the new food entry to the database
            food_entry = form.save(commit=False)
            food_entry.reviews_rating = 0.0
            food_entry.number_of_reviews = 0
            food_entry.user = request.user  # Associate the current user with the entry
            food_entry.save()
            # Redirect to the main view or another relevant page after creation
            return HttpResponseRedirect(reverse('main:show_main'))
    else:
        # If it's a GET request, display an empty form
        form = FoodEntryForm()
    
    # Render the create restaurant form template with the form instance
    context = {
        'form': form,
    }
    return render(request, 'create_restaurant.html', context)

@login_required(login_url='/auth/login/')
def delete_restaurant_via_ajax(request, id):
    if request.method == 'POST':
        if not is_restaurant_manager(request.user):
            return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)
        
        food_entry = get_object_or_404(FoodEntry, id=id)
        food_entry.delete()

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

