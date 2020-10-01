from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, 'energy/index.html')
