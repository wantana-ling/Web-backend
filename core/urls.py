# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_api, name='register'),
    path('login/', views.login_api, name='login'),
    path('get_user/', views.get_user_info, name='get_user_info'),
    path('get_user_all/', views.get_user_all_info, name='get_user_all'),
    path('get_products/', views.get_all_product_details, name='get_all_product_details'),
    path('get_product_names/', views.get_product_names, name='get_product_names'),
    path('get_product_details/<int:product_id>/', views.get_product_details_by_id, name='get_product_details_by_id'),
    path('update_username/', views.update_username, name='update_username'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('add_donation/', views.add_donation, name='add_donation'),
    path('update_rank/', views.update_rank, name='update_rank'),
    path('get_all_donations/', views.get_all_donations, name='get_all_donations'),

]
