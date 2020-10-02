from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.customer_logout, name='logout'),
    path('home/', views.home, name='home'),
]