from django.shortcuts import render, redirect
from main.models import FoodEntry
from django.http import HttpResponse
from django.core import serializers
from main.models import FoodEntry  
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
from authentication.forms import CustomUserCreationForm

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout

@csrf_exempt
def logout_flutter(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout failed."
        }, status=401)

def register(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Add user to the appropriate group
            group_choice = form.cleaned_data.get('group_choice')
            if group_choice == 'user':
                group = Group.objects.get(name='User')
            elif group_choice == 'manager':
                group = Group.objects.get(name='Restaurant_Manager')

            user.groups.add(group)
            messages.success(request, 'Your account has been successfully created!')
            return redirect('auth:login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('auth:login'))
    response.delete_cookie('last_login')
    return response


from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_flutter(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            
            # Get the group(s) the user belongs to
            groups = user.groups.all()
            if groups.exists():
                # Assuming a user can only belong to one group, you can pick the first one or handle it as needed
                user_role = groups.first().name  # If multiple groups, you may concatenate them or choose one
            else:
                user_role = 'No role assigned'
                
            # Successful login status with user role (group name)
            return JsonResponse({
                "username": user.username,
                "user_role": user_role,
                "status": True,
                "message": "Login successful!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, account disabled."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed, check email or password again."
        }, status=401)


@csrf_exempt
def register_flutter(request):
    print("halo")
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        group_choice = data.get('group_choice', 'user')  # Default to 'user' if not provided

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)

        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        
        # Add user to the appropriate group
        try:
            if group_choice == 'user':
                group = Group.objects.get(name='User')
            elif group_choice == 'manager':
                group = Group.objects.get(name='Restaurant_Manager')
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Invalid group choice."
                }, status=400)
            
            user.groups.add(group)
        except Group.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Group does not exist."
            }, status=400)

        user.save()

        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)

    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
