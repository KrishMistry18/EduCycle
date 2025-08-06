from django.core.management.base import BaseCommand
from hub.models import Item
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Create simple PNG images for items'

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
            
            # Create a simple PNG image using a basic approach
            self.create_simple_image(item, item_image_path)
            
            # Update the item's image field
            item.image1.name = f'item_images/{filename}'
            item.save()
            updated_count += 1
            self.stdout.write(f"Created image for: {item.name}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created images for {updated_count} items!')
        )

    def create_simple_image(self, item, filepath):
        """Create a simple image using basic Python"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a 400x300 image
            width, height = 400, 300
            
            # Choose background color based on category
            if item.category == 'textbook':
                bg_color = (227, 242, 253)  # Light blue
                accent_color = (25, 118, 210)
            elif item.category == 'equipment':
                bg_color = (243, 229, 245)  # Light purple
                accent_color = (123, 31, 162)
            elif item.category == 'appliance':
                bg_color = (232, 245, 232)  # Light green
                accent_color = (56, 142, 60)
            elif item.category == 'decor':
                bg_color = (255, 243, 224)  # Light orange
                accent_color = (245, 124, 0)
            else:
                bg_color = (252, 228, 236)  # Light pink
                accent_color = (194, 24, 91)
            
            # Create image
            image = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(image)
            
            # Add border
            draw.rectangle([0, 0, width-1, height-1], outline=(209, 213, 219), width=3)
            
            # Add category text
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            category_text = item.get_category_display().upper()
            text_bbox = draw.textbbox((0, 0), category_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            text_y = 20
            draw.text((text_x, text_y), category_text, fill=accent_color, font=font)
            
            # Add item name
            name_lines = self.wrap_text(item.name, 25)
            name_y = 80
            
            for line in name_lines:
                text_bbox = draw.textbbox((0, 0), line, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = (width - text_width) // 2
                draw.text((text_x, name_y), line, fill=(31, 41, 55), font=font)
                name_y += 30
            
            # Add price if available
            if item.price:
                price_text = f"₹{item.price}"
                text_bbox = draw.textbbox((0, 0), price_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = (width - text_width) // 2
                text_y = height - 60
                draw.text((text_x, text_y), price_text, fill=(5, 150, 105), font=font)
            
            # Add seller info
            seller_text = f"By: {item.seller.first_name}"
            text_bbox = draw.textbbox((0, 0), seller_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            text_y = height - 30
            draw.text((text_x, text_y), seller_text, fill=(107, 114, 128), font=font)
            
            # Save the image
            image.save(filepath, 'PNG')
            
        except ImportError:
            # Fallback: create a simple text file as image placeholder
            with open(filepath, 'w') as f:
                f.write(f"Image for: {item.name}\nCategory: {item.get_category_display()}\nPrice: ₹{item.price if item.price else 'N/A'}")
            self.stdout.write(f"Created text placeholder for: {item.name}")

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