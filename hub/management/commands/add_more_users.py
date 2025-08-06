from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hub.models import Item, UserProfile
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add more users with sample items to the marketplace'

    def handle(self, *args, **options):
        # Create multiple users with different items
        users_data = [
            {
                'username': 'art_student',
                'first_name': 'Sarah',
                'last_name': 'Chen',
                'email': 'sarah.chen@university.edu',
                'student_id': 'STU2024002',
                'department': 'arts',
                'year_of_study': '2',
                'items': [
                    {
                        'name': 'Art History Textbook',
                        'description': 'Comprehensive art history textbook covering Renaissance to Modern Art. Excellent condition.',
                        'category': 'textbook',
                        'price': Decimal('1800.00'),
                        'desired_swap_item': None
                    },
                    {
                        'name': 'Sketchbook Collection',
                        'description': 'Set of 5 high-quality sketchbooks, various sizes. Great for drawing and sketching assignments.',
                        'category': 'other',
                        'price': Decimal('600.00'),
                        'desired_swap_item': None
                    },
                    {
                        'name': 'Drawing Pencils Set',
                        'description': 'Professional drawing pencil set with 12 different grades. Perfect for art students.',
                        'category': 'other',
                        'price': Decimal('400.00'),
                        'desired_swap_item': None
                    }
                ]
            },
            {
                'username': 'engineering_student',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'email': 'mike.johnson@university.edu',
                'student_id': 'STU2024003',
                'department': 'engineering',
                'year_of_study': '4',
                'items': [
                    {
                        'name': 'Arduino Starter Kit',
                        'description': 'Complete Arduino kit with sensors, LEDs, and components. Perfect for engineering projects.',
                        'category': 'equipment',
                        'price': Decimal('1200.00'),
                        'desired_swap_item': 'Raspberry Pi'
                    },
                    {
                        'name': 'Engineering Drawing Set',
                        'description': 'Professional drawing set with compass, rulers, and templates.',
                        'category': 'equipment',
                        'price': Decimal('600.00'),
                        'desired_swap_item': None
                    },
                    {
                        'name': 'Physics Textbook',
                        'description': 'University Physics textbook, excellent condition. Covers mechanics and thermodynamics.',
                        'category': 'textbook',
                        'price': Decimal('900.00'),
                        'desired_swap_item': 'Calculus textbook'
                    },
                    {
                        'name': 'Circuit Components Kit',
                        'description': 'Complete kit with resistors, capacitors, LEDs, and breadboard. Essential for electronics lab.',
                        'category': 'equipment',
                        'price': Decimal('800.00'),
                        'desired_swap_item': None
                    }
                ]
            },
            {
                'username': 'business_student',
                'first_name': 'Emma',
                'last_name': 'Wilson',
                'email': 'emma.wilson@university.edu',
                'student_id': 'STU2024004',
                'department': 'business',
                'year_of_study': '3',
                'items': [
                    {
                        'name': 'Business Statistics Textbook',
                        'description': 'Comprehensive statistics textbook for business students. Includes case studies and examples.',
                        'category': 'textbook',
                        'price': Decimal('1100.00'),
                        'desired_swap_item': None
                    },
                    {
                        'name': 'Financial Calculator',
                        'description': 'HP 12C financial calculator. Essential for finance and accounting courses.',
                        'category': 'equipment',
                        'price': Decimal('1800.00'),
                        'desired_swap_item': None
                    },
                    {
                        'name': 'Business Case Study Book',
                        'description': 'Collection of real business case studies. Perfect for MBA students.',
                        'category': 'textbook',
                        'price': Decimal('700.00'),
                        'desired_swap_item': None
                    }
                ]
            },
            {
                'username': 'science_student',
                'first_name': 'Alex',
                'last_name': 'Brown',
                'email': 'alex.brown@university.edu',
                'student_id': 'STU2024005',
                'department': 'science',
                'year_of_study': '1',
                'items': [
                    {
                        'name': 'Biology Lab Manual',
                        'description': 'Comprehensive lab manual with experiments and procedures.',
                        'category': 'textbook',
                        'price': Decimal('400.00'),
                        'desired_swap_item': None
                    },
                    {
                        'name': 'Safety Goggles',
                        'description': 'Lab safety goggles, barely used. Required for chemistry and biology labs.',
                        'category': 'equipment',
                        'price': Decimal('150.00'),
                        'desired_swap_item': 'Lab coat'
                    },
                    {
                        'name': 'Desk Lamp',
                        'description': 'Adjustable LED desk lamp with USB port. Perfect for late-night studying.',
                        'category': 'appliance',
                        'price': Decimal('800.00'),
                        'desired_swap_item': None
                    },
                    {
                        'name': 'Chemistry Lab Kit',
                        'description': 'Basic chemistry lab kit with test tubes, beakers, and safety equipment.',
                        'category': 'equipment',
                        'price': Decimal('1000.00'),
                        'desired_swap_item': None
                    }
                ]
            },
            {
                'username': 'medical_student',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'email': 'priya.sharma@university.edu',
                'student_id': 'STU2024006',
                'department': 'medicine',
                'year_of_study': '2',
                'items': [
                    {
                        'name': 'Anatomy Textbook',
                        'description': 'Comprehensive human anatomy textbook with detailed illustrations.',
                        'category': 'textbook',
                        'price': Decimal('2200.00'),
                        'desired_swap_item': None
                    },
                    {
                        'name': 'Stethoscope',
                        'description': 'Professional stethoscope in excellent condition. Perfect for medical students.',
                        'category': 'equipment',
                        'price': Decimal('1500.00'),
                        'desired_swap_item': None
                    },
                    {
                        'name': 'Medical Dictionary',
                        'description': 'Comprehensive medical dictionary. Essential reference for medical studies.',
                        'category': 'textbook',
                        'price': Decimal('600.00'),
                        'desired_swap_item': None
                    }
                ]
            }
        ]

        total_created = 0
        
        for user_data in users_data:
            # Create user
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': user_data['email']
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                UserProfile.objects.create(
                    user=user,
                    student_id=user_data['student_id'],
                    department=user_data['department'],
                    year_of_study=user_data['year_of_study']
                )
                self.stdout.write(f"Created user: {user.username}")

            # Create items for this user
            for item_data in user_data['items']:
                item, created = Item.objects.get_or_create(
                    name=item_data['name'],
                    seller=user,
                    defaults={
                        'description': item_data['description'],
                        'category': item_data['category'],
                        'price': item_data['price'],
                        'desired_swap_item': item_data['desired_swap_item'],
                        'is_active': True
                    }
                )
                if created:
                    total_created += 1
                    self.stdout.write(f"Created item: {item.name} (by {user.username})")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {total_created} more study-related items to the marketplace!')
        )
        self.stdout.write(
            self.style.WARNING('Additional users created: art_student, engineering_student, business_student, science_student, medical_student (all with password: password123)')
        ) 