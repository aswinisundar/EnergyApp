from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created successfully')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request,'energy/register.html',{'form':form})


def customer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'energy/login.html',
                  context={'customer_login_form': AuthenticationForm()})


def customer_logout(request):
    logout(request)
    return render(request, 'energy/logout.html')


def home(request):
    return render(request,'energy/home.html')



