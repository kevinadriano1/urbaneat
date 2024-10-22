from django.shortcuts import render, redirect
from main.models import FoodEntry
from django.http import HttpResponse
from django.core import serializers
from main.models import FoodEntry  # Import your model
from main.forms import FoodEntryForm  # Import your form
import os
import csv
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

@login_required(login_url='/auth/login/')
def show_main(request):
    food_entries = FoodEntry.objects.all()  # Querying all food entries

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Construct the full path to the CSV file
    csv_file_path = os.path.join(base_dir, 'main', 'food_database.csv')
    print(f"CSV file path: {csv_file_path}")

    # Read the CSV content
    
    if not FoodEntry.objects.exists():

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:

                    food_entry = FoodEntry(
                            user=request.user,  # Associate the current user with the entry
                            name=row.get('Name', 'gka da'),  # Replace with your actual CSV headers
                            street_address=row.get('Street_Address', 'N/A'),
                            location=row.get('Location', 'N/A'),
                            food_type=row.get('Type', 'N/A'),
                            number_of_reviews=int(row.get('No_of_Reviews', 0)),  # Ensure it's an int
                            reviews_rating = float(row.get('Reviews', 0)),
                            comments=row.get('Comments', 'N/A'),
                            contact_number=row.get('Contact_Number', 'N/A'),
                            trip_advisor_url=row.get('Trip_advisor_Url', 'N/A'),
                            menu_info=row.get('Menu', 'N/A')
                        )

                    food_entry.save() 
        except FileNotFoundError:
            csv_content = None
    
    food_entries = FoodEntry.objects.all()



    context = {
        'npm': '2306170414',
        'name': request.user.username,
        'class': 'PBP KKI',
        'food_entries': food_entries,  # Adding the queried data to the context
        'star_range': range(5),
        'last_login': request.COOKIES.get('last_login','Not set'),
    }

    return render(request, "main.html", context)

def create_food_entry(request):
    form = FoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        food_entry = form.save(commit=False)
        food_entry.user = request.user
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







