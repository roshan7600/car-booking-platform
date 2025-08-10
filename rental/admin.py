from django.contrib import admin
from .models import Car, CarImage, CarFeature, Booking

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3

class CarFeatureInline(admin.TabularInline):
    model = CarFeature
    extra = 3

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'price_per_day', 'is_available')
    list_filter = ('make', 'is_available', 'year')
    search_fields = ('make', 'model', 'description')
    inlines = [CarImageInline, CarFeatureInline]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_date', 'end_date', 'total_price', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('user__username', 'car__make', 'car__model')
    readonly_fields = ('booking_date', 'total_price')
