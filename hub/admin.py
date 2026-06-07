from django.contrib import admin
from .models import (
    UserProfile, Item, Message, Cart, CartItem,
    Order, OrderItem, Payment, Notification, Review, ChatMessage,
    SwapProposal, Watchlist, Report, CollegeDomain, ItemView, MeetupPoint
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'department', 'year_of_study', 'is_college_verified']
    list_filter = ['department', 'year_of_study', 'is_college_verified']
    search_fields = ['user__username', 'user__email', 'student_id']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'category', 'condition', 'price', 'is_active', 'created_at']
    list_filter = ['category', 'condition', 'is_active']
    search_fields = ['name', 'description', 'seller__username']
    ordering = ['-created_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'item', 'timestamp']
    search_fields = ['sender__username', 'receiver__username']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'item', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'seller', 'status', 'total_amount', 'created_at']
    list_filter = ['status']
    search_fields = ['buyer__username', 'seller__username']
    ordering = ['-created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'item', 'quantity', 'price_at_time']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'currency', 'status', 'created_at']
    list_filter = ['status', 'currency']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']
    search_fields = ['user__username', 'title']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user__username', 'item__name']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'message_type', 'timestamp']

@admin.register(SwapProposal)
class SwapProposalAdmin(admin.ModelAdmin):
    list_display = ['proposer', 'receiver', 'offered_item', 'requested_item', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['proposer__username', 'receiver__username']

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'price_threshold', 'created_at']
    search_fields = ['user__username', 'item__name']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'item', 'reason', 'status', 'created_at']
    list_filter = ['reason', 'status']
    search_fields = ['reporter__username', 'item__name']

@admin.register(CollegeDomain)
class CollegeDomainAdmin(admin.ModelAdmin):
    list_display = ['college_name', 'domain', 'city', 'is_active']
    list_filter = ['is_active', 'city']
    search_fields = ['college_name', 'domain']

@admin.register(ItemView)
class ItemViewAdmin(admin.ModelAdmin):
    list_display = ['item', 'viewer_ip', 'timestamp']
    ordering = ['-timestamp']

@admin.register(MeetupPoint)
class MeetupPointAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'college']
