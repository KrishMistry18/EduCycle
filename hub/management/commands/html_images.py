from django.core.management.base import BaseCommand
from hub.models import Item
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Create HTML-based images for items'

    def handle(self, *args, **options):
        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'item_images')
        os.makedirs(media_dir, exist_ok=True)
        
        # Get all items
        items = Item.objects.all()
        updated_count = 0
        
        for item in items:
            # Create a unique filename for each item
            filename = f"{item.id}_{item.name.replace(' ', '_').lower()}.html"
            item_image_path = os.path.join(media_dir, filename)
            
            # Create an HTML-based image
            self.create_html_image(item, item_image_path)
            
            # Update the item's image field to point to the HTML file
            item.image1.name = f'item_images/{filename}'
            item.save()
            updated_count += 1
            self.stdout.write(f"Created HTML image for: {item.name}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created HTML images for {updated_count} items!')
        )

    def create_html_image(self, item, filepath):
        """Create an HTML-based image for the item"""
        # Choose background color based on category
        if item.category == 'textbook':
            bg_color = '#e3f2fd'  # Light blue
            accent_color = '#1976d2'
            icon = '📚'
        elif item.category == 'equipment':
            bg_color = '#f3e5f5'  # Light purple
            accent_color = '#7b1fa2'
            icon = '🔬'
        elif item.category == 'appliance':
            bg_color = '#e8f5e8'  # Light green
            accent_color = '#388e3c'
            icon = '⚡'
        elif item.category == 'decor':
            bg_color = '#fff3e0'  # Light orange
            accent_color = '#f57c00'
            icon = '🎨'
        else:
            bg_color = '#fce4ec'  # Light pink
            accent_color = '#c2185b'
            icon = '📦'
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{item.name}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: {bg_color};
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .image-container {{
            width: 400px;
            height: 300px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            border: 3px solid {accent_color};
            position: relative;
            overflow: hidden;
        }}
        .category-icon {{
            font-size: 48px;
            margin-bottom: 15px;
        }}
        .category-label {{
            background: {accent_color};
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 20px;
        }}
        .item-name {{
            font-size: 18px;
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 15px;
            padding: 0 20px;
            line-height: 1.3;
        }}
        .price {{
            font-size: 24px;
            font-weight: bold;
            color: #059669;
            margin-bottom: 10px;
        }}
        .seller {{
            font-size: 14px;
            color: #6b7280;
        }}
        .pattern {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            opacity: 0.1;
            pointer-events: none;
        }}
        .pattern::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: repeating-linear-gradient(
                45deg,
                {accent_color},
                {accent_color} 2px,
                transparent 2px,
                transparent 8px
            );
        }}
    </style>
</head>
<body>
    <div class="image-container">
        <div class="pattern"></div>
        <div class="category-icon">{icon}</div>
        <div class="category-label">{item.get_category_display()}</div>
        <div class="item-name">{item.name}</div>
        <div class="price">₹{item.price if item.price else 'N/A'}</div>
        <div class="seller">By: {item.seller.first_name} {item.seller.last_name}</div>
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content) 