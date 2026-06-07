from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .api_views import (
    ItemViewSet, MessageViewSet, CartViewSet,
    OrderViewSet, UserViewSet, SwapProposalViewSet,
    WatchlistViewSet, ReportViewSet, NotificationViewSet,
    ReviewViewSet, MeetupPointViewSet,
    SellerAnalyticsView, AIPriceSuggesterView,
)

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'users', UserViewSet, basename='user')
router.register(r'swaps', SwapProposalViewSet, basename='swap')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'meetup-points', MeetupPointViewSet, basename='meetuppoint')

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Router URLs
    path('', include(router.urls)),

    # Custom shortcuts
    path('search/', ItemViewSet.as_view({'get': 'search'}), name='api_search'),
    path('profile/', UserViewSet.as_view({'get': 'profile'}), name='api_profile'),
    path('profile/update/', UserViewSet.as_view({'put': 'update_profile', 'patch': 'update_profile'}), name='api_profile_update'),
    path('profile/complete-onboarding/', UserViewSet.as_view({'post': 'complete_onboarding'}), name='api_complete_onboarding'),
    path('my-items/', UserViewSet.as_view({'get': 'my_items'}), name='api_my_items'),
    path('my-cart/', CartViewSet.as_view({'get': 'my_cart'}), name='api_my_cart'),
    path('cart/checkout/', CartViewSet.as_view({'post': 'checkout'}), name='api_checkout'),
    path('messages/received/', MessageViewSet.as_view({'get': 'received'}), name='api_messages_received'),
    path('messages/sent/', MessageViewSet.as_view({'get': 'sent'}), name='api_messages_sent'),
    path('notifications/unread-count/', NotificationViewSet.as_view({'get': 'unread_count'}), name='api_unread_count'),
    path('notifications/mark-all-read/', NotificationViewSet.as_view({'post': 'mark_all_read'}), name='api_mark_all_read'),
    path('orders/sold/', OrderViewSet.as_view({'get': 'sold'}), name='api_orders_sold'),
    path('swaps/received/', SwapProposalViewSet.as_view({'get': 'received'}), name='api_swaps_received'),
    path('swaps/sent/', SwapProposalViewSet.as_view({'get': 'sent'}), name='api_swaps_sent'),
    path('watchlist/toggle/', WatchlistViewSet.as_view({'post': 'toggle'}), name='api_watchlist_toggle'),

    # Analytics & AI
    path('analytics/seller/', SellerAnalyticsView.as_view(), name='api_seller_analytics'),
    path('ai/suggest-price/', AIPriceSuggesterView.as_view(), name='api_suggest_price'),
]
