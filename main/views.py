from django.shortcuts import render, redirect
from main.models import FoodEntry
from django.http import HttpResponse
from django.core import serializers
from main.models import FoodEntry  # Import your model
from main.forms import FoodEntryForm  # Import your form
import os
import csv

def show_main(request):
    food_entries = FoodEntry.objects.all()  # Querying all food entries

    csv_file_path = "C:/Users/kevin/Documents/kevin/sem3/pbp/midterm/midterm_project/main/food_database.csv"

    # Read the CSV content
    csv_content = []
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                csv_content.append(row)  # Store each row as a dictionary
    except FileNotFoundError:
        csv_content = None

    context = {
        'npm': '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E',
        'food_entries': food_entries,  # Adding the queried data to the context
        'csv_content': csv_content
    }

    return render(request, "main.html", context)

def create_food_entry(request):
    form = FoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_food_entry.html", context)

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



