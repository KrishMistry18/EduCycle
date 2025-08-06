from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File
from hub.models import Item
import os
from PIL import Image, ImageDraw, ImageFont
import io


class Command(BaseCommand):
    help = 'Add engineering graphics tools items to the database with images'

    def create_placeholder_image(self, item_name, width=400, height=300):
        """Create a placeholder image for the item"""
        # Create a new image with a light gray background
        img = Image.new('RGB', (width, height), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Add a border
        draw.rectangle([0, 0, width-1, height-1], outline='#cccccc', width=2)
        
        # Add text
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        # Split item name into lines if it's too long
        words = item_name.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= 20:
                current_line += (" " + word if current_line else word)
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Draw text lines
        text_color = '#333333'
        y_position = height // 2 - (len(lines) * 20) // 2
        
        for line in lines:
            # Get text size
            if font:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
            else:
                text_width = len(line) * 10  # Approximate width
            
            x_position = (width - text_width) // 2
            draw.text((x_position, y_position), line, fill=text_color, font=font)
            y_position += 25
        
        # Add "Image Placeholder" text at bottom
        placeholder_text = "Image Placeholder"
        if font:
            bbox = draw.textbbox((0, 0), placeholder_text, font=font)
            text_width = bbox[2] - bbox[0]
        else:
            text_width = len(placeholder_text) * 8
        
        x_position = (width - text_width) // 2
        draw.text((x_position, height - 30), placeholder_text, fill='#999999', font=font)
        
        # Convert to bytes
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        return img_io

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

        # Engineering Graphics Tools items with image info
        items_data = [
            {
                'name': 'Mini Drafter',
                'description': 'Professional mini drafter with blue and silver design. Features two rulers connected by a protractor head for drawing parallel lines and angles. Includes a blue carrying bag with "Dushala MINI DRAFTER" branding. Perfect for engineering students and professionals.',
                'category': 'equipment',
                'price': 45.00,
                'desired_swap_item': 'Engineering drawing set or technical instruments',
                'image_name': 'mini_drafter.png'
            },
            {
                'name': 'Roller Scale',
                'description': 'Transparent plastic ruler with integrated red cylindrical roller. Features clear measurement markings including a protractor scale. Branded "ROLL-N-DRAW" with 30 CM ruler. Ideal for technical drawing and engineering work.',
                'category': 'equipment',
                'price': 25.00,
                'desired_swap_item': 'Drawing instruments or technical tools',
                'image_name': 'roller_scale.png'
            },
            {
                'name': 'Drawing Board',
                'description': 'Light brown wooden drawing board with adjustable incline. Features a black metal stand and two silver clips at the top edge for securing paper. Professional quality for engineering and architectural drawing.',
                'category': 'equipment',
                'price': 120.00,
                'desired_swap_item': 'Technical drawing equipment or drafting tools',
                'image_name': 'drawing_board.png'
            },
            {
                'name': 'Set Squares (45° & 30-60-90°)',
                'description': 'Professional set of two transparent plastic set squares by Jet Scholar. Includes 45-degree set square with protractor arc (0-180°) and 30-60-90 degree set square. Both feature centimeter/millimeter scales and precision cut-outs.',
                'category': 'equipment',
                'price': 35.00,
                'desired_swap_item': 'Technical drawing tools or engineering instruments',
                'image_name': 'set_squares.png'
            },
            {
                'name': 'Compass Set',
                'description': 'Complete compass set in black rectangular case with white interior. Features silver and dark grey compass with adjustable leg opening, needle point, and pencil lead holder. Includes spare lead refills and mechanical pencil. Professional quality for technical drawing.',
                'category': 'equipment',
                'price': 55.00,
                'desired_swap_item': 'Drawing instruments or technical tools',
                'image_name': 'compass_set.png'
            },
            {
                'name': 'French Curves Set',
                'description': 'Professional French curves set including one large bright yellow plastic curve and two smaller wooden curves. Designed for drawing smooth, non-circular arcs and complex curves. Essential for engineering and architectural drawing.',
                'category': 'equipment',
                'price': 40.00,
                'desired_swap_item': 'Technical drawing tools or drafting instruments',
                'image_name': 'french_curves_set.png'
            },
            {
                'name': 'Mechanical Pencil',
                'description': 'Professional mechanical pencil with dark blue body and black grip. Features silver clip and precision lead mechanism. Complete with eraser cap, spare leads, and spring mechanism. Perfect for technical drawing and engineering work.',
                'category': 'equipment',
                'price': 15.00,
                'desired_swap_item': 'Writing instruments or technical tools',
                'image_name': 'mechanical_pencil.png'
            },
            {
                'name': 'Drafting Brush',
                'description': 'Professional drafting brush with light brown wooden handle. Features wide, flat brush end with dense black bristles in rectangular shape. Essential for cleaning drawing surfaces and removing eraser debris.',
                'category': 'equipment',
                'price': 12.00,
                'desired_swap_item': 'Drawing accessories or technical tools',
                'image_name': 'drafting_brush.png'
            },
            {
                'name': 'Drawing Sheets Pack',
                'description': 'High-quality drawing sheets pack for technical and engineering drawings. Professional grade paper suitable for pencil, ink, and marker work. Standard sizes for engineering and architectural projects.',
                'category': 'equipment',
                'price': 20.00,
                'desired_swap_item': 'Paper supplies or drawing materials',
                'image_name': 'drawing_sheets_pack.png'
            },
            {
                'name': 'Sheet Protector Folder',
                'description': 'Professional sheet protector folder with punched holes for binder insertion. Clear transparent protectors for organizing and preserving technical drawings and documents. Essential for maintaining drawing portfolios.',
                'category': 'equipment',
                'price': 18.00,
                'desired_swap_item': 'Organization supplies or technical accessories',
                'image_name': 'sheet_protector_folder.png'
            },
            {
                'name': 'Flap File Set',
                'description': 'Colorful flap file set with six files in various colors (gray, pink, green, purple, blue, bright pink). Each file features black spine and colored body with snap closure flap. Perfect for organizing technical documents and drawings.',
                'category': 'equipment',
                'price': 30.00,
                'desired_swap_item': 'Organization supplies or technical accessories',
                'image_name': 'flap_file_set.png'
            },
            {
                'name': 'Zipper File Bag',
                'description': 'Professional zipper file bag for storing and protecting technical drawings and documents. Durable construction with secure zipper closure. Ideal for carrying engineering drawings and technical documents.',
                'category': 'equipment',
                'price': 25.00,
                'desired_swap_item': 'Storage solutions or technical accessories',
                'image_name': 'zipper_file_bag.png'
            }
        ]

        created_count = 0
        for item_data in items_data:
            # Check if item already exists
            if not Item.objects.filter(name=item_data['name']).exists():
                # Create placeholder image
                img_io = self.create_placeholder_image(item_data['name'])
                
                # Create the item
                item = Item.objects.create(
                    name=item_data['name'],
                    description=item_data['description'],
                    category=item_data['category'],
                    price=item_data['price'],
                    desired_swap_item=item_data['desired_swap_item'],
                    seller=user,
                    is_active=True
                )
                
                # Save the image
                item.image1.save(
                    item_data['image_name'],
                    File(img_io),
                    save=True
                )
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created item with image: {item.name} -> {item_data["image_name"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Item already exists: {item_data["name"]}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} engineering tools items with placeholder images.'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                'Note: Placeholder images have been created. You can replace them with actual images by uploading the exact images you want to use.'
            )
        ) 