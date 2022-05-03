from django.contrib import admin
from django.urls import path

# Telusko
from . import views

urlpatterns = [
    # For user registration
    path('register', views.register, name='register'),
    # For login
    path('login', views.login, name='login'),
    # For logout
    path('logout', views.logout, name='logout'),
]