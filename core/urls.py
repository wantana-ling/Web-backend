# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_api, name='register'),
    path('login/', views.login_api, name='login'),
    path('get_user/', views.get_user_info, name='get_user_info'),
]
