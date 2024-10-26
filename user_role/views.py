from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout
from .forms import ProfileForm, UserUpdateForm
from .models import Profile
from django.contrib import messages

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def change_username_password(request):
    user_update_form = UserUpdateForm()

    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST)
        
        if user_update_form.is_valid():
            new_username = user_update_form.cleaned_data.get('new_username')
            new_password = user_update_form.cleaned_data.get('new_password')

            if new_username:
                request.user.username = new_username

            if new_password:
                request.user.set_password(new_password)
                update_session_auth_hash(request, request.user)

            request.user.save()
            return redirect('profile')

    return render(request, 'change_username_password.html', {
        'user_update_form': user_update_form,
    })

@login_required
def delete_profile(request):
    if request.method == "POST":
        # Delete user and their profile
        user = request.user
        user.delete()  # This will also delete the profile due to the OneToOneField relationship
        messages.success(request, "Your profile has been successfully deleted.")
        logout(request)  # Log out the user after deletion
        return redirect('auth:login')  # Redirect to the home page or any other page

    return render(request, 'delete_profile.html')
