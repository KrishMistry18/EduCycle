from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from .models import (
    Item, Message, Cart, CartItem, Order, OrderItem,
    SwapProposal, Watchlist, Report, Notification, Review,
    CollegeDomain, MeetupPoint, ItemView, UserProfile
)


class UserSerializer(serializers.ModelSerializer):
    is_college_verified = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_joined', 'is_college_verified', 'avg_rating', 'review_count'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_is_college_verified(self, obj):
        try:
            return obj.userprofile.is_college_verified
        except Exception:
            return False

    def get_avg_rating(self, obj):
        result = Review.objects.filter(item__seller=obj).aggregate(avg=Avg('rating'))
        avg = result.get('avg')
        return round(avg, 1) if avg else None

    def get_review_count(self, obj):
        return Review.objects.filter(item__seller=obj).count()


class ItemSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)
    image_url = serializers.SerializerMethodField()
    image2_url = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'condition', 'condition_display', 'price', 'desired_swap_item',
            'seller', 'is_active', 'created_at', 'updated_at',
            'image1', 'image_url', 'image2', 'image2_url', 'view_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image1:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image1.url)
        return None

    def get_image2_url(self, obj):
        if obj.image2:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image2.url)
        return None

    def get_view_count(self, obj):
        return obj.views.count()


class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description', 'category', 'condition', 'price', 'desired_swap_item', 'image1', 'image2']

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
        fields = ['id', 'item', 'quantity', 'total_price', 'added_at']
        read_only_fields = ['id', 'added_at']

    def get_total_price(self, obj):
        return obj.get_total_price()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_items', 'total_amount', 'total_price', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_total_items(self, obj):
        return obj.cartitem_set.count()

    def get_total_amount(self, obj):
        return sum(item.get_total_price() for item in obj.cartitem_set.all())

    def get_total_price(self, obj):
        return self.get_total_amount(obj)


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'quantity', 'price_at_time']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'buyer', 'seller', 'items', 'total_amount',
            'status', 'shipping_address', 'payment_method', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


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
    is_college_verified = serializers.SerializerMethodField()
    has_completed_onboarding = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_joined', 'items_count', 'messages_count',
            'is_college_verified', 'has_completed_onboarding'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_items_count(self, obj):
        return obj.item_set.filter(is_active=True).count()

    def get_messages_count(self, obj):
        return obj.received_messages.count()

    def get_is_college_verified(self, obj):
        try:
            return obj.userprofile.is_college_verified
        except Exception:
            return False

    def get_has_completed_onboarding(self, obj):
        try:
            return obj.userprofile.has_completed_onboarding
        except Exception:
            return False


class SwapProposalSerializer(serializers.ModelSerializer):
    proposer = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    offered_item = ItemSerializer(read_only=True)
    requested_item = ItemSerializer(read_only=True)
    offered_item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='offered_item', write_only=True
    )
    requested_item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='requested_item', write_only=True
    )

    class Meta:
        model = SwapProposal
        fields = [
            'id', 'proposer', 'receiver', 'offered_item', 'requested_item',
            'offered_item_id', 'requested_item_id', 'message', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'proposer', 'receiver', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['proposer'] = self.context['request'].user
        validated_data['receiver'] = validated_data['requested_item'].seller
        return super().create(validated_data)


class WatchlistSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='item', write_only=True
    )

    class Meta:
        model = Watchlist
        fields = ['id', 'item', 'item_id', 'price_threshold', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'item', 'reason', 'description', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    related_item = ItemSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message',
            'related_item', 'related_order', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    item = ItemSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'item', 'user', 'rating', 'title', 'comment',
            'is_verified_purchase', 'helpful_votes', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'is_verified_purchase', 'helpful_votes', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CollegeDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeDomain
        fields = ['id', 'college_name', 'domain', 'city']


class MeetupPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetupPoint
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'college']
