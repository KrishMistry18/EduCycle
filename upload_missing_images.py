import os
import django
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EduCycle.settings')
os.environ['USE_FIREBASE_STORAGE'] = 'True'
django.setup()

media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'item_images')

for filename in os.listdir(media_dir):
    if filename.endswith('.png'):
        filepath = os.path.join(media_dir, filename)
        storage_path = f"item_images/{filename}"
        
        with open(filepath, 'rb') as f:
            content = f.read()
            
            if not default_storage.exists(storage_path):
                default_storage.save(storage_path, ContentFile(content))
                print(f"Uploaded {filename} to Firebase Storage.")
            else:
                print(f"{filename} already exists in Firebase Storage.")

print("All missing images uploaded!")
