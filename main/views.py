from django.shortcuts import render, redirect
from main.models import FoodEntry
from django.http import HttpResponse
from django.core import serializers
#from main.forms import FoodEntryForm  # Import your form
import os
from django.contrib.auth.models import Group
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

@login_required(login_url='/auth/login/')
def show_main(request):
    # Get the search query from the URL parameters (search bar input)
    query = request.GET.get('q')  # "q" is the query parameter

    if query:
        # Filter food entries based on the search query (case-insensitive)
        food_entries = FoodEntry.objects.filter(name__icontains=query)
    else:
        # If no search query, return all food entries
        food_entries = FoodEntry.objects.all()


    is_manager = request.user.groups.filter(name='Restaurant_Manager').exists()
    # Prepare context for the template
    context = {
        'npm': '2306170414',
        'name': request.user.username,
        'class': 'PBP KKI',
        'food_entries': food_entries,  # Adding the queried (filtered) food entries to the context
        'star_range': range(5),
        'last_login': request.COOKIES.get('last_login', 'Not set'),
        'is_manager': is_manager, 
    }

    return render(request, "main.html", context)

def show_xml(request):
    data = FoodEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = FoodEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = FoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = FoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


