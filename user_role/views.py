from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

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