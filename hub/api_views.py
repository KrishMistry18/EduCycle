from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Item, Message, Cart, CartItem, Order, OrderItem
from .serializers import (
    UserSerializer, ItemSerializer, ItemCreateSerializer, MessageSerializer,
    CartSerializer, CartItemSerializer, OrderSerializer, SearchSerializer,
    UserProfileSerializer
)
# from django_ratelimit.decorators import ratelimit
# from django.utils.decorators import method_decorator

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'seller']
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return ItemCreateSerializer
        return ItemSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search with multiple filters"""
        serializer = SearchSerializer(data=request.query_params)
        if serializer.is_valid():
            queryset = self.get_queryset()
            
            # Apply search query
            query = serializer.validated_data.get('query')
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(category__icontains=query)
                )
            
            # Apply category filter
            category = serializer.validated_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
            
            # Apply price range filter
            min_price = serializer.validated_data.get('min_price')
            max_price = serializer.validated_data.get('max_price')
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            
            # Apply sorting
            sort_by = serializer.validated_data.get('sort_by', '-created_at')
            queryset = queryset.order_by(sort_by)
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def contact_seller(self, request, pk=None):
        """Send a message to the item seller"""
        try:
            item = self.get_object()
            content = request.data.get('content')
            
            if not content:
                return Response(
                    {'error': 'Message content is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            message = Message.objects.create(
                sender=request.user,
                receiver=item.seller,
                item=item,
                content=content
            )
            
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        """Add item to user's cart"""
        try:
            item = self.get_object()
            quantity = int(request.data.get('quantity', 1))
            
            if quantity <= 0:
                return Response(
                    {'error': 'Quantity must be greater than 0'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item=item,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-timestamp')

    @action(detail=False, methods=['get'])
    def received(self, request):
        """Get messages received by the user"""
        messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Get messages sent by the user"""
        messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread_notifications_count(self, request):
        """Get count of unread notifications for the current user"""
        from .models import Notification
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'count': unread_count})

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """Get current user's cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        """Checkout cart and create order"""
        try:
            cart = self.get_object()
            cart_items = cart.cartitem_set.all()
            
            if not cart_items.exists():
                return Response(
                    {'error': 'Cart is empty'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create order
            order = Order.objects.create(
                buyer=request.user,
                status='pending'
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    item=cart_item.item,
                    quantity=cart_item.quantity,
                    price=cart_item.item.price
                )
            
            # Clear cart
            cart_items.delete()
            
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        """Cancel an order"""
        try:
            order = self.get_object()
            if order.status == 'pending':
                order.status = 'cancelled'
                order.save()
                serializer = self.get_serializer(order)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Order cannot be cancelled'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user's profile"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user's profile"""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_items(self, request):
        """Get current user's items"""
        items = Item.objects.filter(seller=request.user, is_active=True).order_by('-created_at')
        page = self.paginate_queryset(items)
        if page is not None:
            serializer = ItemSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data) 