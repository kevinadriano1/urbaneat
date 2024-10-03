from django.shortcuts import render, redirect
from main.models import FoodEntry
from django.http import HttpResponse
from django.core import serializers
from .models import FoodEntry  # Import your model
from .forms import FoodEntryForm  # Import your form


def show_main(request):
    food_entries = FoodEntry.objects.all()  # Querying all food entries
    context = {
        'npm': '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E',
        'food_entries': food_entries  # Adding the queried data to the context
    }
    return render(request, "main.html", context)

def create_food_entry(request):
    if request.method == "POST":
        form = FoodEntryForm(request.POST)
        
        if form.is_valid():
            form.save()  # Directly save the form if valid
            return redirect('main:show_main')
        else:
            print(form.errors)  # Debug: Print any validation errors to the console
    else:
        form = FoodEntryForm()

    context = {'form': form}
    return render(request, "create_food_entry.html", context)

def show_xml(request):
    data = FoodEntry.objects.all()

def show_xml(request):
    data = FoodEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")



