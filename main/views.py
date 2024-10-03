from django.shortcuts import render, redirect
from main.models import FoodEntry
from django.http import HttpResponse
from django.core import serializers

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
    form = FoodEntry(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_mood_entry.html", context)

def show_xml(request):
    data = FoodEntry.objects.all()

def show_xml(request):
    data = FoodEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")



