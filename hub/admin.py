from django.contrib import admin
from .models import UserProfile, Item, Message

admin.site.register(UserProfile)
admin.site.register(Item)
admin.site.register(Message)
