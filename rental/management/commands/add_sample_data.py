from django.core.management.base import BaseCommand
from rental.models import Car, CarImage, CarFeature
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Adds sample car data to the database'

    def handle(self, *args, **kwargs):
        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        # Add sample cars
        cars_data = [
            {
                'make': 'Lamborghini',
                'model': 'Aventador',
                'year': 2023,
                'price_per_day': 1500.00,
                'description': 'The Lamborghini Aventador is a mid-engine sports car produced by the Italian automotive manufacturer Lamborghini. Experience unparalleled performance and luxury with this iconic supercar featuring a powerful V12 engine and scissor doors.',
                'engine': 'V12',
                'horsepower': 740,
                'top_speed': 350,
                'acceleration': 2.8,
                'transmission': 'automatic',
                'seats': 2,
                'is_available': True,
                'main_image_url': 'https://images.unsplash.com/photo-1511919884226-fd3cad34687c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                'features': ['Carbon Fiber Interior', 'Scissor Doors', 'Advanced Navigation System', 'Premium Sound System'],
                'images': [
                    'https://images.unsplash.com/photo-1511919884226-fd3cad34687c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                    'https://images.unsplash.com/photo-1554744512-d6c603f27c54?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                    'https://images.unsplash.com/photo-1566024287286-457247b70310?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80'
                ]
            },
            {
                'make': 'Ferrari',
                'model': '488 GTB',
                'year': 2022,
                'price_per_day': 1200.00,
                'description': 'The Ferrari 488 GTB is a mid-engine sports car produced by the Italian automobile manufacturer Ferrari. This stunning vehicle combines elegance with raw power, featuring a twin-turbocharged V8 engine that delivers an unforgettable driving experience.',
                'engine': 'Twin-Turbo V8',
                'horsepower': 660,
                'top_speed': 330,
                'acceleration': 3.0,
                'transmission': 'semi-automatic',
                'seats': 2,
                'is_available': True,
                'main_image_url': 'https://images.unsplash.com/photo-1592198084033-aade902d1aae?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                'features': ['Carbon Ceramic Brakes', 'Racing Seats', 'LED Headlights', 'Adaptive Suspension'],
                'images': [
                    'https://images.unsplash.com/photo-1592198084033-aade902d1aae?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                    'https://images.unsplash.com/photo-1503376780353-7e6692767b70?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                    'https://images.unsplash.com/photo-1583121274602-3e2820c69888?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80'
                ]
            },
            {
                'make': 'Rolls-Royce',
                'model': 'Phantom',
                'year': 2022,
                'price_per_day': 1800.00,
                'description': 'The Rolls-Royce Phantom is the pinnacle of luxury motoring. This iconic sedan combines timeless elegance with modern technology, providing an unparalleled experience for both driver and passengers. The cabin offers supreme comfort and the finest materials.',
                'engine': 'V12',
                'horsepower': 563,
                'top_speed': 250,
                'acceleration': 5.3,
                'transmission': 'automatic',
                'seats': 5,
                'is_available': True,
                'main_image_url': 'https://images.unsplash.com/photo-1632145683309-153c7c135b3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                'features': ['Starlight Headliner', 'Bespoke Audio System', 'Champagne Cooler', 'Massage Seats'],
                'images': [
                    'https://images.unsplash.com/photo-1632145683309-153c7c135b3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                    'https://images.unsplash.com/photo-1563720223889-5c373f354333?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                    'https://images.unsplash.com/photo-1512749491228-caef5a7831d7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80'
                ]
            },
            {
                'make': 'Bentley',
                'model': 'Continental GT',
                'year': 2023,
                'price_per_day': 1100.00,
                'description': 'The Bentley Continental GT is a grand tourer manufactured by British automaker Bentley Motors. This luxurious coupe combines performance with handcrafted luxury, featuring a powerful W12 engine, exquisite leather interior, and cutting-edge technology.',
                'engine': 'W12',
                'horsepower': 626,
                'top_speed': 333,
                'acceleration': 3.6,
                'transmission': 'automatic',
                'seats': 4,
                'is_available': True,
                'main_image_url': 'https://images.unsplash.com/photo-1539786774582-0707555f5124?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                'features': ['Diamond Quilted Leather', 'Rotating Display', 'Air Suspension', 'Panoramic Roof'],
                'images': [
                    'https://images.unsplash.com/photo-1539786774582-0707555f5124?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                    'https://images.unsplash.com/photo-1621800043295-a73fe2f70e80?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                    'https://images.unsplash.com/photo-1558486012-817176f84c6d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80'
                ]
            },
            {
                'make': 'Porsche',
                'model': '911 Turbo S',
                'year': 2023,
                'price_per_day': 950.00,
                'description': 'The Porsche 911 Turbo S is the pinnacle of the iconic 911 series. This sports car delivers extraordinary performance with its twin-turbocharged flat-six engine, all-wheel drive, and sophisticated aerodynamics, all while maintaining everyday usability.',
                'engine': 'Twin-Turbo Flat-Six',
                'horsepower': 640,
                'top_speed': 330,
                'acceleration': 2.7,
                'transmission': 'automatic',
                'seats': 4,
                'is_available': True,
                'main_image_url': 'https://images.unsplash.com/photo-1614162692292-7ac56d7f571e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                'features': ['Sport Chrono Package', 'Adaptive Sports Seats', 'Bose Surround Sound', 'Carbon Fiber Elements'],
                'images': [
                    'https://images.unsplash.com/photo-1614162692292-7ac56d7f571e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                    'https://images.unsplash.com/photo-1503376780353-7e6692767b70?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80',
                    'https://images.unsplash.com/photo-1611821064430-0d40291922d1?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80'
                ]
            }
        ]

        # Add cars to database
        car_count = 0
        for car_data in cars_data:
            # Extract features and images
            features = car_data.pop('features')
            images = car_data.pop('images')
            
            # Create car if it doesn't exist already
            car, created = Car.objects.get_or_create(
                make=car_data['make'],
                model=car_data['model'],
                year=car_data['year'],
                defaults=car_data
            )
            
            if created:
                car_count += 1
                
                # Add features
                for feature_name in features:
                    CarFeature.objects.create(car=car, name=feature_name)
                
                # Add images
                for i, image_url in enumerate(images):
                    CarImage.objects.create(
                        car=car,
                        image_url=image_url,
                        is_main=(i == 0)  # First image is main
                    )
                
                self.stdout.write(self.style.SUCCESS(f'Created {car.year} {car.make} {car.model}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {car_count} cars to the database'))