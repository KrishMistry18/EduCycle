from django.core.management.base import BaseCommand
from hub.models import Item
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Add placeholder images for items'

    def handle(self, *args, **options):
        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'item_images')
        os.makedirs(media_dir, exist_ok=True)
        
        # Create a simple placeholder image file
        placeholder_content = """
        <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="300" height="200" fill="#f0f0f0"/>
            <text x="150" y="100" text-anchor="middle" fill="#666" font-family="Arial" font-size="16">
                Item Image
            </text>
        </svg>
        """
        
        placeholder_path = os.path.join(media_dir, 'placeholder.svg')
        with open(placeholder_path, 'w') as f:
            f.write(placeholder_content)
        
        self.stdout.write(f"Created placeholder image at {placeholder_path}")
        
        # Update items to reference the placeholder image
        items = Item.objects.all()
        updated_count = 0
        
        for item in items:
            # Create a unique filename for each item
            filename = f"{item.id}_{item.name.replace(' ', '_').lower()}.svg"
            item_image_path = os.path.join(media_dir, filename)
            
            # Copy placeholder content to item-specific file
            with open(item_image_path, 'w') as f:
                f.write(placeholder_content)
            
            # Update the item's image field
            if not item.image1:
                item.image1.name = f'item_images/{filename}'
                item.save()
                updated_count += 1
                self.stdout.write(f"Added image for: {item.name}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added placeholder images for {updated_count} items!')
        )
        self.stdout.write(
            self.style.WARNING('Note: These are placeholder SVG images. Replace with actual product photos for production.')
        ) 