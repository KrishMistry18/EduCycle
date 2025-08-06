from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hub.models import Item
import os


class Command(BaseCommand):
    help = 'Add engineering graphics tools items to the database'

    def handle(self, *args, **options):
        # Get or create a default user for these items
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )

        # Engineering Graphics Tools items
        items_data = [
            {
                'name': 'Mini Drafter',
                'description': 'Professional mini drafter with blue and silver design. Features two rulers connected by a protractor head for drawing parallel lines and angles. Includes a blue carrying bag with "Dushala MINI DRAFTER" branding. Perfect for engineering students and professionals.',
                'category': 'equipment',
                'price': 45.00,
                'desired_swap_item': 'Engineering drawing set or technical instruments'
            },
            {
                'name': 'Roller Scale',
                'description': 'Transparent plastic ruler with integrated red cylindrical roller. Features clear measurement markings including a protractor scale. Branded "ROLL-N-DRAW" with 30 CM ruler. Ideal for technical drawing and engineering work.',
                'category': 'equipment',
                'price': 25.00,
                'desired_swap_item': 'Drawing instruments or technical tools'
            },
            {
                'name': 'Drawing Board',
                'description': 'Light brown wooden drawing board with adjustable incline. Features a black metal stand and two silver clips at the top edge for securing paper. Professional quality for engineering and architectural drawing.',
                'category': 'equipment',
                'price': 120.00,
                'desired_swap_item': 'Technical drawing equipment or drafting tools'
            },
            {
                'name': 'Set Squares (45° & 30-60-90°)',
                'description': 'Professional set of two transparent plastic set squares by Jet Scholar. Includes 45-degree set square with protractor arc (0-180°) and 30-60-90 degree set square. Both feature centimeter/millimeter scales and precision cut-outs.',
                'category': 'equipment',
                'price': 35.00,
                'desired_swap_item': 'Technical drawing tools or engineering instruments'
            },
            {
                'name': 'Compass Set',
                'description': 'Complete compass set in black rectangular case with white interior. Features silver and dark grey compass with adjustable leg opening, needle point, and pencil lead holder. Includes spare lead refills and mechanical pencil. Professional quality for technical drawing.',
                'category': 'equipment',
                'price': 55.00,
                'desired_swap_item': 'Drawing instruments or technical tools'
            },
            {
                'name': 'French Curves Set',
                'description': 'Professional French curves set including one large bright yellow plastic curve and two smaller wooden curves. Designed for drawing smooth, non-circular arcs and complex curves. Essential for engineering and architectural drawing.',
                'category': 'equipment',
                'price': 40.00,
                'desired_swap_item': 'Technical drawing tools or drafting instruments'
            },
            {
                'name': 'Mechanical Pencil',
                'description': 'Professional mechanical pencil with dark blue body and black grip. Features silver clip and precision lead mechanism. Complete with eraser cap, spare leads, and spring mechanism. Perfect for technical drawing and engineering work.',
                'category': 'equipment',
                'price': 15.00,
                'desired_swap_item': 'Writing instruments or technical tools'
            },
            {
                'name': 'Drafting Brush',
                'description': 'Professional drafting brush with light brown wooden handle. Features wide, flat brush end with dense black bristles in rectangular shape. Essential for cleaning drawing surfaces and removing eraser debris.',
                'category': 'equipment',
                'price': 12.00,
                'desired_swap_item': 'Drawing accessories or technical tools'
            },
            {
                'name': 'Drawing Sheets Pack',
                'description': 'High-quality drawing sheets pack for technical and engineering drawings. Professional grade paper suitable for pencil, ink, and marker work. Standard sizes for engineering and architectural projects.',
                'category': 'equipment',
                'price': 20.00,
                'desired_swap_item': 'Paper supplies or drawing materials'
            },
            {
                'name': 'Sheet Protector Folder',
                'description': 'Professional sheet protector folder with punched holes for binder insertion. Clear transparent protectors for organizing and preserving technical drawings and documents. Essential for maintaining drawing portfolios.',
                'category': 'equipment',
                'price': 18.00,
                'desired_swap_item': 'Organization supplies or technical accessories'
            },
            {
                'name': 'Flap File Set',
                'description': 'Colorful flap file set with six files in various colors (gray, pink, green, purple, blue, bright pink). Each file features black spine and colored body with snap closure flap. Perfect for organizing technical documents and drawings.',
                'category': 'equipment',
                'price': 30.00,
                'desired_swap_item': 'Organization supplies or technical accessories'
            },
            {
                'name': 'Zipper File Bag',
                'description': 'Professional zipper file bag for storing and protecting technical drawings and documents. Durable construction with secure zipper closure. Ideal for carrying engineering drawings and technical documents.',
                'category': 'equipment',
                'price': 25.00,
                'desired_swap_item': 'Storage solutions or technical accessories'
            }
        ]

        created_count = 0
        for item_data in items_data:
            # Check if item already exists
            if not Item.objects.filter(name=item_data['name']).exists():
                item = Item.objects.create(
                    name=item_data['name'],
                    description=item_data['description'],
                    category=item_data['category'],
                    price=item_data['price'],
                    desired_swap_item=item_data['desired_swap_item'],
                    seller=user,
                    is_active=True
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created item: {item.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Item already exists: {item_data["name"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} engineering tools items.'
            )
        ) 