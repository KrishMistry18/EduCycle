from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .api_views import (
    ItemViewSet, MessageViewSet, CartViewSet, 
    OrderViewSet, UserViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # API endpoints
    path('', include(router.urls)),
    
    # Additional endpoints
    path('search/', ItemViewSet.as_view({'get': 'search'}), name='api_search'),
    path('profile/', UserViewSet.as_view({'get': 'profile'}), name='api_profile'),
    path('profile/update/', UserViewSet.as_view({'put': 'update_profile', 'patch': 'update_profile'}), name='api_profile_update'),
    path('my-items/', UserViewSet.as_view({'get': 'my_items'}), name='api_my_items'),
    path('my-cart/', CartViewSet.as_view({'get': 'my_cart'}), name='api_my_cart'),
    path('messages/received/', MessageViewSet.as_view({'get': 'received'}), name='api_messages_received'),
    path('messages/sent/', MessageViewSet.as_view({'get': 'sent'}), name='api_messages_sent'),
    path('notifications/unread-count/', MessageViewSet.as_view({'get': 'unread_notifications_count'}), name='api_unread_notifications_count'),
] 