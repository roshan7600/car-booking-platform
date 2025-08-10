from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CustomUserCreationForm, BookingForm
from .models import Car, Booking
from datetime import date
from django.core.mail import send_mail

def home(request):
    # Get featured cars for carousel
    featured_cars = Car.objects.filter(is_available=True).order_by('-created_at')[:5]
    return render(request, 'home.html', {'featured_cars': featured_cars})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    # Get user's bookings
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    # Count different types of bookings
    total_bookings = bookings.count()
    active_bookings = bookings.filter(status__in=['pending', 'confirmed']).count()
    completed_bookings = bookings.filter(status='completed').count()
    
    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
        'user': request.user
    }
    
    return render(request, 'profile.html', context)

def car_list(request):
    # Initialize query
    cars = Car.objects.all()
    
    # Apply filters if provided
    make = request.GET.get('make', '')
    if make:
        cars = cars.filter(make__icontains=make)
        
    transmission = request.GET.get('transmission', '')
    if transmission:
        cars = cars.filter(transmission=transmission)
    
    min_price = request.GET.get('min_price', '')
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    
    max_price = request.GET.get('max_price', '')
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    
    # Search functionality
    query = request.GET.get('q', '')
    if query:
        cars = cars.filter(
            Q(make__icontains=query) | 
            Q(model__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Get available makes for filter
    all_makes = Car.objects.values_list('make', flat=True).distinct()
    
    context = {
        'cars': cars,
        'all_makes': all_makes,
        'current_make': make,
        'current_transmission': transmission,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'query': query
    }
    
    return render(request, 'car_list.html', context)

def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    # Get related cars (same make, different model)
    related_cars = Car.objects.filter(make=car.make).exclude(id=car.id)[:3]
    return render(request, 'car_detail.html', {'car': car, 'related_cars': related_cars})

@login_required
def booking(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Check if car is available for the selected dates
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            if car.is_booked(start_date, end_date):
                messages.error(request, 'Sorry, this car is not available for the selected dates.')
            else:
                # Create booking
                booking = form.save(commit=False)
                booking.user = request.user
                booking.car = car
                booking.save()
                
                messages.success(request, 'Booking created successfully!')
                return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'booking.html', {'form': form, 'car': car})

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    return render(request, 'booking_confirmation.html', {'booking': booking})

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def admin_booking_management(request):
    """
    Admin view for managing all bookings with options to approve, reject, etc.
    """
    # Get all bookings, newest first
    all_bookings = Booking.objects.all().order_by('-booking_date')
    
    # Get counts for dashboard
    pending_count = all_bookings.filter(status='pending').count()
    confirmed_count = all_bookings.filter(status='confirmed').count()
    cancelled_count = all_bookings.filter(status='cancelled').count()
    completed_count = all_bookings.filter(status='completed').count()
    
    # Filter based on query parameters
    status_filter = request.GET.get('status', '')
    if status_filter and status_filter != 'all':
        all_bookings = all_bookings.filter(status=status_filter)
    
    context = {
        'bookings': all_bookings,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'cancelled_count': cancelled_count, 
        'completed_count': completed_count,
        'current_filter': status_filter
    }
    
    return render(request, 'admin_booking_management.html', context)

@user_passes_test(is_admin)
def admin_update_booking_status(request, booking_id):
    """
    View for admins to update the status of a booking
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [status for status, _ in Booking.STATUS_CHOICES]:
            booking.status = new_status
            booking.save()
            
            # Add a success message
            action_map = {
                'confirmed': 'approved',
                'cancelled': 'rejected',
                'completed': 'marked as completed',
                'pending': 'marked as pending'
            }
            action = action_map.get(new_status, 'updated')
            messages.success(request, f'Booking #{booking.id} has been {action} successfully.')
        else:
            messages.error(request, 'Invalid status provided.')
    
    # Redirect back to the booking management page
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET.get('next'))
    return redirect('admin_booking_management')



