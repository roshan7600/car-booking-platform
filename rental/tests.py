from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Car, Booking
import datetime

class CarModelTest(TestCase):
    def setUp(self):
        self.car = Car.objects.create(
            make="Lamborghini",
            model="Aventador",
            year=2022,
            price_per_day=1200.00,
            description="Luxury sports car",
            engine="V12",
            horsepower=730,
            top_speed=350,
            acceleration=2.9,
            transmission="automatic",
            seats=2,
            is_available=True,
            main_image_url="https://example.com/car.jpg"
        )

    def test_car_creation(self):
        self.assertTrue(isinstance(self.car, Car))
        self.assertEqual(str(self.car), "2022 Lamborghini Aventador")

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.car = Car.objects.create(
            make="Lamborghini",
            model="Aventador",
            year=2022,
            price_per_day=1200.00,
            description="Luxury sports car",
            engine="V12",
            horsepower=730,
            top_speed=350,
            acceleration=2.9,
            transmission="automatic",
            seats=2,
            is_available=True,
            main_image_url="https://example.com/car.jpg"
        )
        
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        
        self.booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            start_date=today,
            end_date=tomorrow,
            status='confirmed'
        )

    def test_booking_creation(self):
        self.assertTrue(isinstance(self.booking, Booking))
        self.assertEqual(self.booking.total_price, self.car.price_per_day)
        self.assertEqual(self.booking.get_duration_days(), 1)

class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.car = Car.objects.create(
            make="Lamborghini",
            model="Aventador",
            year=2022,
            price_per_day=1200.00,
            description="Luxury sports car",
            engine="V12",
            horsepower=730,
            top_speed=350,
            acceleration=2.9,
            transmission="automatic",
            seats=2,
            is_available=True,
            main_image_url="https://example.com/car.jpg"
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_car_list_view(self):
        response = self.client.get(reverse('car_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_list.html')
        self.assertContains(response, "Lamborghini")

    def test_car_detail_view(self):
        response = self.client.get(reverse('car_detail', args=[self.car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_detail.html')
        self.assertContains(response, "Aventador")

    def test_booking_view_requires_login(self):
        response = self.client.get(reverse('booking', args=[self.car.id]))
        self.assertRedirects(response, f'/login/?next=/cars/{self.car.id}/booking/')
        
        # Now login and try again
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('booking', args=[self.car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking.html')
