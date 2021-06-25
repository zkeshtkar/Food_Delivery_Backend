from django.contrib.auth import get_user_model
from django.shortcuts import render


def about_us(request):
    context = {
        'members': get_user_model().objects.all()
    }
    return render(request, 'about_us.html', context)
