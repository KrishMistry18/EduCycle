from django.core.management.base import BaseCommand
from hub.models import Item
import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

class Command(BaseCommand):
    help = 'Fix image structure and create proper PNG images'

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
        
        # Create gradient background based on category
        if item.category == 'textbook':
            bg_color = '#e3f2fd'  # Light blue
            accent_color = '#1976d2'
        elif item.category == 'equipment':
            bg_color = '#f3e5f5'  # Light purple
            accent_color = '#7b1fa2'
        elif item.category == 'appliance':
            bg_color = '#e8f5e8'  # Light green
            accent_color = '#388e3c'
        elif item.category == 'decor':
            bg_color = '#fff3e0'  # Light orange
            accent_color = '#f57c00'
        else:
            bg_color = '#fce4ec'  # Light pink
            accent_color = '#c2185b'
        
        # Create base image
        image = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(image)
        
        # Add subtle pattern
        for i in range(0, width, 50):
            for j in range(0, height, 50):
                draw.rectangle([i, j, i+25, j+25], fill=accent_color, outline=None, width=0)
                draw.rectangle([i+25, j+25, i+50, j+50], fill=accent_color, outline=None, width=0)
        
        # Add category icon
        icon_size = 80
        icon_x = (width - icon_size) // 2
        icon_y = 60
        
        # Draw category icon background
        draw.ellipse([icon_x, icon_y, icon_x + icon_size, icon_y + icon_size], 
                    fill=accent_color, outline='white', width=3)
        
        # Add category icon symbol
        icon_symbol = self.get_category_symbol(item.category)
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw category symbol
        text_bbox = draw.textbbox((0, 0), icon_symbol, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = icon_x + (icon_size - text_width) // 2
        text_y = icon_y + (icon_size - text_height) // 2
        draw.text((text_x, text_y), icon_symbol, fill='white', font=font)
        
        # Add item name
        name_lines = self.wrap_text(item.name, 30)
        name_y = icon_y + icon_size + 40
        
        for line in name_lines:
            text_bbox = draw.textbbox((0, 0), line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            draw.text((text_x, name_y), line, fill='#1f2937', font=font)
            name_y += 25
        
        # Add price if available
        if item.price:
            price_text = f"₹{item.price}"
            text_bbox = draw.textbbox((0, 0), price_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            text_y = height - 50
            draw.text((text_x, text_y), price_text, fill='#059669', font=font)
        
        # Add category label
        category_text = item.get_category_display().upper()
        text_bbox = draw.textbbox((0, 0), category_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (width - text_width) // 2
        text_y = height - 25
        draw.text((text_x, text_y), category_text, fill=accent_color, font=font)
        
        # Add border
        draw.rectangle([0, 0, width-1, height-1], outline='#d1d5db', width=2)
        
        # Save the image
        image.save(filepath, 'PNG')

    def get_category_symbol(self, category):
        """Get symbol for category"""
        symbols = {
            'textbook': '📚',
            'equipment': '🔬',
            'decor': '🎨',
            'appliance': '⚡',
            'other': '📦'
        }
        return symbols.get(category, '📦')

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
        
        return lines[:2]  # Limit to 2 lines 