from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from main.models import FoodEntry  

@login_required(login_url='/auth/login/')
def show_main(request):
    query = request.GET.get('q')
    if query:
        food_entries = FoodEntry.objects.filter(
            Q(name__icontains=query) |
            Q(street_address__icontains=query) |
            Q(location__icontains=query) |
            Q(food_type__icontains=query)
        )
        unique_food_entries = {entry.name: entry for entry in food_entries}.values()
    else:
        unique_food_entries = FoodEntry.objects.all()

    is_manager = request.user.groups.filter(name='Restaurant_Manager').exists()

    for row in unique_food_entries:
        row.full_stars = int(row.avg_rating)
        row.half_star = row.avg_rating % 1 >= 0.5

    context = {
        'npm': '2306170414',
        'name': request.user.username,
        'class': 'PBP KKI',
        'food_entries': unique_food_entries,
        'star_range': range(5),
        'last_login': request.COOKIES.get('last_login', 'Not set'),
        'is_manager': is_manager,
        'rows': unique_food_entries,
    }
    return render(request, "main.html", context)
