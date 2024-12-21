from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import FoodEntry
from .forms import FoodEntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

@csrf_exempt
def edit_restaurant_api(request, id):
    if request.method == 'POST':
        restaurant_entry = get_object_or_404(FoodEntry, id=id)
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)

            #Data type validation yuh
            try:
                url_validator = URLValidator()
                url_validator(data.get('trip_advisor_url'))
            except ValidationError:
                return JsonResponse({'message': 'Invalid URL for Restaurant URL'}, status=400)
            
            try:
                url_validator(data.get('image_url'))
            except ValidationError:
                return JsonResponse({'message': 'Invalid URL for Image URL'}, status=400)
            
            if not data.get('contact_number', '').isdigit():
                return JsonResponse({'message': 'Invalid contact number, it must be numeric'}, status=400)
            
            # Update the restaurant object with the received data
            form = FoodEntryForm(data, instance=restaurant_entry)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Restaurant updated successfully.'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid data, form errors.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON decode error or 404.'}, status=400)
        
    elif request.method == 'GET':
        restaurant_entry = get_object_or_404(FoodEntry, id=id)
        data = {
            'name': restaurant_entry.name,
            'street_address': restaurant_entry.street_address,
            'location': restaurant_entry.location,
            'food_type': restaurant_entry.food_type,
            'comments': restaurant_entry.comments,
            'contact_number': restaurant_entry.contact_number,
            'trip_advisor_url': restaurant_entry.trip_advisor_url,
            'menu_info': restaurant_entry.menu_info,
            'image_url': restaurant_entry.image_url,
        }
        return JsonResponse(data, status=200)

@csrf_exempt
def create_restaurant_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Data type validation
            try:
                url_validator = URLValidator()
                url_validator(data.get('trip_advisor_url'))
            except ValidationError:
                return JsonResponse({'message': 'Invalid URL for Restaurant URL'}, status=400)
            
            try:
                url_validator(data.get('image_url'))
            except ValidationError:
                return JsonResponse({'message': 'Invalid URL for Image URL'}, status=400)
            
            if not data.get('contact_number', '').isdigit():
                return JsonResponse({'message': 'Invalid contact number, it must be numeric'}, status=400)
            
            # Now, validate using the form
            form = FoodEntryForm(data)
            if form.is_valid():
                food_entry = form.save(commit=False)
                food_entry.reviews_rating = 0.0
                food_entry.number_of_reviews = 0
                food_entry.avg_rating = "0.0"  # Ensure correct type for avg_rating
                food_entry.save()
                return JsonResponse({
                    'message': 'Restaurant created successfully',
                }, status=200)
            else:
                return JsonResponse({'errors': form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'Unexpected error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def delete_restaurant_api(request, id):
    if request.method == 'DELETE':
        try:
            food_entry = get_object_or_404(FoodEntry, id=id)
            food_entry.delete()
            return JsonResponse({'message': 'Restaurant deleted successfully'})
        except FoodEntry.DoesNotExist:
            return JsonResponse({'message': 'Restaurant not found'}, status=404)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

# Custom decorator to check if user is in the Restaurant_Manager group
def is_restaurant_manager(user):
    if user.groups.filter(name='Restaurant_Manager').exists():
        return True
    else:
        return False 

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

    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            # Save the new food entry to the database
            food_entry = form.save(commit=False)
            food_entry.reviews_rating = 0.0
            food_entry.number_of_reviews = 0
            food_entry.avg_rating = "0.0"
            food_entry.save()
            # Redirect to the main view 
            return HttpResponseRedirect(reverse('main:show_main'))
    else:
        # If it's a GET request, display an empty form
        form = FoodEntryForm()
    
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

