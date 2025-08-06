from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item, Message, Cart, CartItem, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class ItemSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'price', 'seller', 'is_active', 'created_at', 'updated_at',
            'image1', 'image_url'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image1:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image1.url)
        return None

class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description', 'category', 'price', 'image1', 'image2']
    
    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    item = ItemSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'item', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'item', 'quantity', 'total_price', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_total_price(self, obj):
        return obj.get_total_price()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_items', 'total_amount', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_total_items(self, obj):
        return obj.cartitem_set.count()
    
    def get_total_amount(self, obj):
        return sum(item.get_total_price() for item in obj.cartitem_set.all())

class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'quantity', 'price', 'created_at']
        read_only_fields = ['id', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    buyer = UserSerializer(read_only=True)
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'items', 'total_amount', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_total_amount(self, obj):
        return sum(item.price * item.quantity for item in obj.orderitem_set.all())

class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=200, required=False)
    category = serializers.CharField(max_length=50, required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    sort_by = serializers.ChoiceField(
        choices=['name', 'price', 'created_at', '-name', '-price', '-created_at'],
        required=False
    )

class UserProfileSerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()
    messages_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'items_count', 'messages_count']
        read_only_fields = ['id', 'date_joined']
    
    def get_items_count(self, obj):
        return obj.item_set.filter(is_active=True).count()
    
    def get_messages_count(self, obj):
        return obj.received_messages.count() 