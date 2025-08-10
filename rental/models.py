from django.db import models
from django.contrib.auth.models import User
import datetime

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    engine = models.CharField(max_length=100)
    horsepower = models.IntegerField()
    top_speed = models.IntegerField(help_text="Top speed in km/h")
    acceleration = models.DecimalField(max_digits=4, decimal_places=1, help_text="0-100 km/h in seconds")
    transmission = models.CharField(max_length=50, choices=[
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
        ('semi-automatic', 'Semi-Automatic')
    ])
    seats = models.IntegerField()
    is_available = models.BooleanField(default=True)
    main_image_url = models.URLField(help_text="URL to the main car image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    def is_booked(self, start_date, end_date):
        """Check if car is booked during the given date range"""
        bookings = self.booking_set.filter(
            status__in=['confirmed', 'pending'],
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        return bookings.exists()

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.car}"

class CarFeature(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.user.username} - {self.car} ({self.start_date} to {self.end_date})"
    
    def save(self, *args, **kwargs):
        """Calculate total price before saving"""
        if not self.total_price:
            days = (self.end_date - self.start_date).days
            self.total_price = self.car.price_per_day * days
        super().save(*args, **kwargs)

    def get_duration_days(self):
        """Calculate the duration of the booking in days"""
        return (self.end_date - self.start_date).days
