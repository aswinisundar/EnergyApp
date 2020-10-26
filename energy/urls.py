from django.urls import path
from . import views


urlpatterns = [
    path('', views.customer_login, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('usage_data/', views.usage_data, name='usage_data'),
    path('usage_data/<int:year>/<int:month>/', views.usage_data, name='usage_data1'),
    path('register/', views.register, name='register'),
    path('logout/', views.customer_logout, name='logout'),
    path('home/', views.home, name='home'),
]