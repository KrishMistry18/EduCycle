from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes as perm_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import (
    Item, Message, Cart, CartItem, Order, OrderItem,
    SwapProposal, Watchlist, Report, Notification, Review,
    CollegeDomain, MeetupPoint, ItemView, UserProfile
)
from .serializers import (
    UserSerializer, ItemSerializer, ItemCreateSerializer, MessageSerializer,
    CartSerializer, CartItemSerializer, OrderSerializer, SearchSerializer,
    UserProfileSerializer, SwapProposalSerializer, WatchlistSerializer,
    ReportSerializer, NotificationSerializer, ReviewSerializer,
    CollegeDomainSerializer, MeetupPointSerializer
)
import os
import json
import logging

logger = logging.getLogger(__name__)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'seller', 'condition']
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return (
            Item.objects.filter(is_active=True)
            .select_related('seller', 'seller__userprofile')
            .prefetch_related('reviews', 'views')
            .order_by('-created_at')
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return ItemCreateSerializer
        return ItemSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        serializer = SearchSerializer(data=request.query_params)
        if serializer.is_valid():
            queryset = self.get_queryset()
            query = serializer.validated_data.get('query')
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(category__icontains=query)
                )
            category = serializer.validated_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
            min_price = serializer.validated_data.get('min_price')
            max_price = serializer.validated_data.get('max_price')
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
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
        item = self.get_object()
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.create(
            sender=request.user,
            receiver=item.seller,
            item=item,
            content=content
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        item = self.get_object()
        quantity = int(request.data.get('quantity', 1))
        if quantity <= 0:
            return Response({'error': 'Quantity must be > 0'}, status=status.HTTP_400_BAD_REQUEST)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, item=item, defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def track_view(self, request, pk=None):
        """Track item view for analytics (once per session)"""
        item = self.get_object()
        session_id = request.session.session_key or request.META.get('HTTP_X_SESSION_ID', '')
        viewer_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        # Only count once per session per item
        if not ItemView.objects.filter(item=item, session_id=session_id).exists():
            ItemView.objects.create(item=item, viewer_ip=viewer_ip, session_id=session_id)
        return Response({'status': 'ok'})


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver', 'item').order_by('-timestamp')

    @action(detail=False, methods=['get'])
    def received(self, request):
        messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
        page = self.paginate_queryset(messages)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(messages, many=True).data)

    @action(detail=False, methods=['get'])
    def sent(self, request):
        messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
        page = self.paginate_queryset(messages)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(messages, many=True).data)

    @action(detail=False, methods=['get'])
    def unread_notifications_count(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'count': count})


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(self.get_serializer(cart).data)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.select_related('item__seller').all()
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        shipping_address = request.data.get('shipping_address', '')
        payment_method = request.data.get('payment_method', 'cod')

        # Group by seller
        seller_orders = {}
        for cart_item in cart_items:
            seller = cart_item.item.seller
            if seller.id not in seller_orders:
                order = Order.objects.create(
                    buyer=request.user,
                    seller=seller,
                    total_amount=0,
                    shipping_address=shipping_address,
                    payment_method=payment_method,
                )
                seller_orders[seller.id] = {'order': order, 'total': 0}
            oi = OrderItem.objects.create(
                order=seller_orders[seller.id]['order'],
                item=cart_item.item,
                quantity=cart_item.quantity,
                price_at_time=cart_item.item.price or 0,
            )
            seller_orders[seller.id]['total'] += oi.get_total_price()

        for sd in seller_orders.values():
            sd['order'].total_amount = sd['total']
            sd['order'].save()

        cart.cartitem_set.all().delete()
        first_order = list(seller_orders.values())[0]['order']
        return Response(OrderSerializer(first_order).data, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects.filter(buyer=self.request.user)
            .select_related('buyer', 'seller')
            .prefetch_related('orderitem_set__item__seller')
            .order_by('-created_at')
        )

    @action(detail=False, methods=['get'])
    def sold(self, request):
        orders = (
            Order.objects.filter(seller=request.user)
            .select_related('buyer', 'seller')
            .prefetch_related('orderitem_set__item')
            .order_by('-created_at')
        )
        page = self.paginate_queryset(orders)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(orders, many=True).data)

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            return Response(self.get_serializer(order).data)
        return Response({'error': 'Order cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Allow unauthenticated user registration"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password')
            if not password:
                return Response({'password': ['Password is required']}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(
                username=request.data.get('username'),
                email=request.data.get('email', ''),
                password=password,
                first_name=request.data.get('first_name', ''),
                last_name=request.data.get('last_name', ''),
            )
            UserProfile.objects.get_or_create(user=user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def profile(self, request):
        return Response(UserProfileSerializer(request.user).data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_items(self, request):
        items = (
            Item.objects.filter(seller=request.user)
            .select_related('seller')
            .order_by('-created_at')
        )
        page = self.paginate_queryset(items)
        if page is not None:
            return self.get_paginated_response(ItemSerializer(page, many=True, context={'request': request}).data)
        return Response(ItemSerializer(items, many=True, context={'request': request}).data)

    @action(detail=False, methods=['post'])
    def complete_onboarding(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.has_completed_onboarding = True
        profile.save()
        return Response({'status': 'ok'})


class SwapProposalViewSet(viewsets.ModelViewSet):
    serializer_class = SwapProposalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SwapProposal.objects.filter(
            Q(proposer=user) | Q(receiver=user)
        ).select_related('proposer', 'receiver', 'offered_item', 'requested_item').order_by('-created_at')

    @action(detail=False, methods=['get'])
    def received(self, request):
        proposals = SwapProposal.objects.filter(receiver=request.user).order_by('-created_at')
        page = self.paginate_queryset(proposals)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(proposals, many=True).data)

    @action(detail=False, methods=['get'])
    def sent(self, request):
        proposals = SwapProposal.objects.filter(proposer=request.user).order_by('-created_at')
        page = self.paginate_queryset(proposals)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(proposals, many=True).data)

    @action(detail=True, methods=['patch'])
    def respond(self, request, pk=None):
        proposal = self.get_object()
        if proposal.receiver != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        new_status = request.data.get('status')
        if new_status not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        proposal.status = new_status
        proposal.save()
        return Response(self.get_serializer(proposal).data)

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        proposal = self.get_object()
        if proposal.proposer != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        proposal.status = 'cancelled'
        proposal.save()
        return Response(self.get_serializer(proposal).data)


class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user).select_related('item__seller')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Toggle watchlist status for an item"""
        item_id = request.data.get('item_id')
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        existing = Watchlist.objects.filter(user=request.user, item=item).first()
        if existing:
            existing.delete()
            return Response({'status': 'removed', 'watchlisted': False})
        Watchlist.objects.create(user=request.user, item=item)
        return Response({'status': 'added', 'watchlisted': True})


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(reporter=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['patch'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'ok'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'ok'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'count': count})


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.select_related('user', 'item').order_by('-created_at')

    @action(detail=False, methods=['get'])
    def for_seller(self, request):
        seller_id = request.query_params.get('seller_id')
        if not seller_id:
            return Response({'error': 'seller_id required'}, status=status.HTTP_400_BAD_REQUEST)
        reviews = Review.objects.filter(item__seller_id=seller_id).select_related('user', 'item')
        page = self.paginate_queryset(reviews)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(reviews, many=True).data)


class MeetupPointViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MeetupPointSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = MeetupPoint.objects.filter(is_active=True)


class SellerAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.utils import timezone
        from datetime import timedelta
        import random

        user = request.user
        items = Item.objects.filter(seller=user)
        total_views = ItemView.objects.filter(item__seller=user).count()
        total_inquiries = Message.objects.filter(receiver=user).count()

        # Views over last 30 days
        today = timezone.now().date()
        labels = []
        views_data = []
        for i in range(29, -1, -1):
            day = today - timedelta(days=i)
            labels.append(day.strftime('%b %d'))
            count = ItemView.objects.filter(
                item__seller=user,
                timestamp__date=day
            ).count()
            views_data.append(count)

        # Per-item stats
        listings = []
        for item in items:
            item_views = item.views.count()
            item_msgs = Message.objects.filter(item=item).count()
            days_listed = (timezone.now().date() - item.created_at.date()).days
            listings.append({
                'id': item.id,
                'name': item.name,
                'price': str(item.price) if item.price else None,
                'is_active': item.is_active,
                'views': item_views,
                'messages': item_msgs,
                'days_listed': days_listed,
                'image_url': request.build_absolute_uri(item.image1.url) if item.image1 else None,
            })

        top_item = max(listings, key=lambda x: x['views'], default=None) if listings else None

        return Response({
            'total_views': total_views,
            'total_inquiries': total_inquiries,
            'views_over_time': views_data,
            'views_labels': labels,
            'top_item': top_item,
            'listings': listings,
        })


class AIPriceSuggesterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title', '')
        category = request.data.get('category', '')
        condition = request.data.get('condition', 'good')

        # Try OpenAI if key is set
        openai_key = os.environ.get('OPENAI_API_KEY')
        if openai_key:
            try:
                import openai
                client = openai.OpenAI(api_key=openai_key)
                prompt = (
                    f"You are a pricing assistant for an Indian student marketplace. "
                    f"Suggest a fair resale price in INR for: {title}, "
                    f"Category: {category}, Condition: {condition}. "
                    f"Consider typical student budgets in India. "
                    f"Respond with ONLY a JSON: {{\"min\": number, \"max\": number, \"suggested\": number}}"
                )
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                )
                result = json.loads(response.choices[0].message.content.strip())
                return Response(result)
            except Exception as e:
                logger.warning(f"OpenAI price suggestion failed: {e}")

        # Fallback: rule-based pricing
        base_prices = {
            'textbook': 250, 'equipment': 600, 'decor': 200,
            'appliance': 1000, 'other': 350
        }
        condition_multipliers = {
            'new': 1.0, 'like_new': 0.85, 'good': 0.65, 'fair': 0.45
        }
        base = base_prices.get(category, 350)
        mult = condition_multipliers.get(condition, 0.65)
        suggested = round(base * mult / 50) * 50
        return Response({
            'min': round(suggested * 0.8),
            'max': round(suggested * 1.2),
            'suggested': suggested,
        })
