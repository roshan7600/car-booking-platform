from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/<int:car_id>/booking/', views.booking, name='booking'),
    path('bookings/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    
    # Admin booking management routes - using rental-admin prefix to avoid conflicts with Django admin
    path('rental-admin/bookings/', views.admin_booking_management, name='admin_booking_management'),
    path('rental-admin/bookings/<int:booking_id>/update-status/', views.admin_update_booking_status, name='admin_update_booking_status'),
]
