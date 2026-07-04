from django.contrib import admin
from django.urls import path
from Users import views

app_name = 'users' 

urlpatterns = [
    path('user/register', views.register, name = 'register'),
    path('user/login', views.login, name = 'login'),
    path('user/logout', views.logout, name = 'logout'),
    path('', views.home, name = 'home'),
]