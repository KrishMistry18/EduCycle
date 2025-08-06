from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hub.models import Item, UserProfile
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Add sample items to the marketplace'

    def handle(self, *args, **options):
        # Create a sample user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='sample_seller',
            defaults={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@university.edu'
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            UserProfile.objects.create(
                user=user,
                student_id='STU2024001',
                department='computer_science',
                year_of_study='3'
            )
            self.stdout.write(self.style.SUCCESS('Created sample user: sample_seller'))

        # Sample items data - Study related only, priced in INR
        sample_items = [
            # Textbooks
            {
                'name': 'Introduction to Computer Science',
                'description': 'Excellent condition textbook for CS101. No highlighting or writing inside. Perfect for first-year students.',
                'category': 'textbook',
                'price': Decimal('1200.00'),
                'desired_swap_item': 'Calculus textbook'
            },
            {
                'name': 'Data Structures and Algorithms',
                'description': 'Used but in good condition. Some notes in margins but very readable. Essential for CS majors.',
                'category': 'textbook',
                'price': Decimal('800.00'),
                'desired_swap_item': None
            },
            {
                'name': 'Organic Chemistry Textbook',
                'description': 'Comprehensive chemistry textbook. Includes practice problems and solutions. Great for pre-med students.',
                'category': 'textbook',
                'price': Decimal('1500.00'),
                'desired_swap_item': 'Biology textbook'
            },
            {
                'name': 'Business Management Principles',
                'description': 'Like new condition. Used for one semester only. Perfect for business students.',
                'category': 'textbook',
                'price': Decimal('600.00'),
                'desired_swap_item': None
            },
            {
                'name': 'Physics Fundamentals',
                'description': 'University Physics textbook, excellent condition. Covers mechanics and thermodynamics.',
                'category': 'textbook',
                'price': Decimal('900.00'),
                'desired_swap_item': 'Calculus textbook'
            },
            {
                'name': 'Biology Lab Manual',
                'description': 'Comprehensive lab manual with experiments and procedures.',
                'category': 'textbook',
                'price': Decimal('400.00'),
                'desired_swap_item': None
            },
            
            # Lab Equipment
            {
                'name': 'Scientific Calculator',
                'description': 'TI-84 Plus calculator in excellent condition. Perfect for math and science courses.',
                'category': 'equipment',
                'price': Decimal('2500.00'),
                'desired_swap_item': None
            },
            {
                'name': 'Lab Coat (Size M)',
                'description': 'Clean lab coat, barely used. Perfect for chemistry or biology labs.',
                'category': 'equipment',
                'price': Decimal('300.00'),
                'desired_swap_item': 'Safety goggles'
            },
            {
                'name': 'Microscope Slides Set',
                'description': 'Complete set of prepared microscope slides for biology lab. Includes 50+ slides.',
                'category': 'equipment',
                'price': Decimal('800.00'),
                'desired_swap_item': None
            },
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
                'name': 'Financial Calculator',
                'description': 'HP 12C financial calculator. Essential for finance and accounting courses.',
                'category': 'equipment',
                'price': Decimal('1800.00'),
                'desired_swap_item': None
            },
            {
                'name': 'Safety Goggles',
                'description': 'Lab safety goggles, barely used. Required for chemistry and biology labs.',
                'category': 'equipment',
                'price': Decimal('150.00'),
                'desired_swap_item': 'Lab coat'
            },
            
            # Study Supplies
            {
                'name': 'Premium Notebook Set',
                'description': 'Set of 5 high-quality notebooks with different colored covers. Perfect for organizing different subjects.',
                'category': 'other',
                'price': Decimal('400.00'),
                'desired_swap_item': None
            },
            {
                'name': 'Study Desk Lamp',
                'description': 'Adjustable LED desk lamp with USB port. Perfect for late-night studying.',
                'category': 'appliance',
                'price': Decimal('800.00'),
                'desired_swap_item': None
            },
            {
                'name': 'Backpack - Laptop Compatible',
                'description': 'High-quality backpack with laptop compartment. Water-resistant and comfortable for daily use.',
                'category': 'other',
                'price': Decimal('1200.00'),
                'desired_swap_item': None
            },
            {
                'name': 'Whiteboard Set',
                'description': 'Portable whiteboard with markers and eraser. Great for group study sessions.',
                'category': 'other',
                'price': Decimal('500.00'),
                'desired_swap_item': None
            },
            {
                'name': 'Study Planner',
                'description': 'Academic planner with monthly and weekly layouts. Perfect for organizing assignments and exams.',
                'category': 'other',
                'price': Decimal('200.00'),
                'desired_swap_item': None
            },
            {
                'name': 'USB Study Light',
                'description': 'Clip-on USB study light. Perfect for reading in dim lighting conditions.',
                'category': 'appliance',
                'price': Decimal('300.00'),
                'desired_swap_item': None
            }
        ]

        # Create items
        created_count = 0
        for item_data in sample_items:
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
                created_count += 1
                self.stdout.write(f"Created item: {item.name}")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {created_count} study-related items to the marketplace!')
        )
        self.stdout.write(
            self.style.WARNING('You can now view these items on the website. Login with username: sample_seller, password: password123')
        ) 