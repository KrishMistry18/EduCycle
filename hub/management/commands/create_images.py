from django.core.management.base import BaseCommand
from hub.models import Item
import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import io

class Command(BaseCommand):
    help = 'Create proper PNG images for items'

    def handle(self, *args, **options):
        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'item_images')
        os.makedirs(media_dir, exist_ok=True)
        
        # Get all items
        items = Item.objects.all()
        updated_count = 0
        
        for item in items:
            # Create a unique filename for each item
            filename = f"{item.id}_{item.name.replace(' ', '_').lower()}.png"
            item_image_path = os.path.join(media_dir, filename)
            
            # Create a proper PNG image
            self.create_item_image(item, item_image_path)
            
            # Update the item's image field
            if not item.image1 or 'placeholder' in str(item.image1):
                item.image1.name = f'item_images/{filename}'
                item.save()
                updated_count += 1
                self.stdout.write(f"Created image for: {item.name}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created images for {updated_count} items!')
        )

    def create_item_image(self, item, filepath):
        """Create a custom image for the item"""
        # Create a 400x300 image with gradient background
        width, height = 400, 300
        
        # Create gradient background
        image = Image.new('RGB', (width, height), color='#f8f9fa')
        draw = ImageDraw.Draw(image)
        
        # Create gradient effect
        for y in range(height):
            r = int(248 - (y / height) * 20)
            g = int(249 - (y / height) * 20)
            b = int(250 - (y / height) * 20)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add category-specific background pattern
        if item.category == 'textbook':
            # Book pattern
            for i in range(0, width, 40):
                draw.rectangle([i, 0, i+20, height], fill='#e3f2fd', outline='#bbdefb')
        elif item.category == 'equipment':
            # Lab equipment pattern
            for i in range(0, width, 30):
                draw.ellipse([i, 0, i+20, 20], fill='#f3e5f5', outline='#ce93d8')
        elif item.category == 'appliance':
            # Appliance pattern
            for i in range(0, width, 35):
                draw.rectangle([i, 0, i+25, 25], fill='#e8f5e8', outline='#a5d6a7')
        else:
            # Other items pattern
            for i in range(0, width, 25):
                draw.polygon([(i, 0), (i+12, 12), (i, 25), (i-12, 12)], fill='#fff3e0', outline='#ffcc02')
        
        # Add category icon
        icon_size = 60
        icon_x = (width - icon_size) // 2
        icon_y = 50
        
        # Draw category icon background
        draw.ellipse([icon_x, icon_y, icon_x + icon_size, icon_y + icon_size], 
                    fill='#6366f1', outline='#4f46e5')
        
        # Add category text
        category_text = item.category.upper()
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw category text
        text_bbox = draw.textbbox((0, 0), category_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = icon_x + (icon_size - text_width) // 2
        text_y = icon_y + (icon_size - 10) // 2
        draw.text((text_x, text_y), category_text, fill='white', font=font)
        
        # Add item name
        name_lines = self.wrap_text(item.name, 25)
        name_y = icon_y + icon_size + 30
        
        for line in name_lines:
            text_bbox = draw.textbbox((0, 0), line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            draw.text((text_x, name_y), line, fill='#374151', font=font)
            name_y += 20
        
        # Add price if available
        if item.price:
            price_text = f"₹{item.price}"
            text_bbox = draw.textbbox((0, 0), price_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            text_y = height - 40
            draw.text((text_x, text_y), price_text, fill='#059669', font=font)
        
        # Add border
        draw.rectangle([0, 0, width-1, height-1], outline='#d1d5db', width=2)
        
        # Save the image
        image.save(filepath, 'PNG')

    def wrap_text(self, text, max_chars):
        """Wrap text to fit within max_chars per line"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_chars:
                current_line += (" " + word if current_line else word)
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines[:3]  # Limit to 3 lines 