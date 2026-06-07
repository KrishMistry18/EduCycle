from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, ItemForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Item, Message, Cart, CartItem, Order, OrderItem, Notification, Review, ChatMessage
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
from .services import NotificationService
from .chatbot import EduCycleChatbot
import uuid

# Create your views here.

def home(request):
    items = Item.objects.filter(is_active=True).order_by('-created_at')
    query = request.GET.get('q')
    category = request.GET.get('category')
    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
    if category:
        items = items.filter(category=category)
    return render(request, 'hub/item_list.html', {'items': items})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, 'Registration successful! Please log in with your credentials.')
                return redirect('user_login')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'hub/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            # Try to authenticate with username or email
            user = authenticate(request, username=username, password=password)
            if user is None:
                # Try with email if username didn't work
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username/email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserLoginForm()
    return render(request, 'hub/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('user_login')

def item_list(request):
    items = Item.objects.filter(is_active=True)
    
    # Handle search
    search_query = request.GET.get('search', '').strip()
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # Handle category filter
    category_filter = request.GET.get('category', '').strip()
    if category_filter:
        items = items.filter(category=category_filter)
    
    # Order by creation date
    items = items.order_by('-created_at')
    
    return render(request, 'hub/item_list.html', {
        'items': items,
        'search_query': search_query,
        'category_filter': category_filter
    })

def search_suggestions(request):
    """AJAX endpoint for search suggestions"""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Get suggestions from item names and categories
    suggestions = []
    
    # Search in item names
    items = Item.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__icontains=query)
    ).values('name', 'category').distinct()[:10]
    
    for item in items:
        suggestions.append({
            'text': item['name'],
            'category': item['category']
        })
    
    # Add category suggestions
    categories = Item.objects.filter(
        category__icontains=query
    ).values_list('category', flat=True).distinct()[:5]
    
    for category in categories:
        suggestions.append({
            'text': f"Category: {category}",
            'category': category
        })
    
    return JsonResponse({'suggestions': suggestions})

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                item = form.save(commit=False)
                item.seller = request.user
                item.save()
                
                # Send notification for item added
                NotificationService.notify_item_added(request.user, item)
                
                messages.success(request, 'Item created successfully! You will receive a confirmation email.')
                return redirect('item_list')
            except Exception as e:
                messages.error(request, f'Failed to create item: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ItemForm()
    return render(request, 'hub/item_form.html', {'form': form})

def item_detail(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        # Get related items from the same category
        related_items = Item.objects.filter(
            category=item.category,
            is_active=True
        ).exclude(id=item.id).order_by('-created_at')[:3]
        return render(request, 'hub/item_detail.html', {
            'item': item,
            'items': related_items
        })
    except Item.DoesNotExist:
        messages.error(request, 'Item not found.')
        return redirect('item_list')

@login_required
def send_message(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        if request.method == 'POST':
            content = request.POST.get('content')
            if content and len(content.strip()) > 0:
                message_obj = Message.objects.create(
                    sender=request.user,
                    receiver=item.seller,
                    item=item,
                    content=content.strip()
                )
                
                # Send notification to seller
                NotificationService.notify_message_received(
                    receiver=item.seller,
                    sender=request.user,
                    item=item,
                    message_content=content.strip()
                )
                
                messages.success(request, 'Message sent to the seller!')
                return redirect('item_detail', item_id=item.id)
            else:
                messages.error(request, 'Message content cannot be empty.')
        return render(request, 'hub/send_message.html', {'item': item})
    except Item.DoesNotExist:
        messages.error(request, 'Item not found.')
        return redirect('item_list')

@login_required
def profile(request):
    user_items = Item.objects.filter(seller=request.user).order_by('-created_at')
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'hub/profile.html', {'user_items': user_items, 'received_messages': received_messages})

@login_required
def item_edit(request, item_id):
    try:
        item = Item.objects.get(id=item_id, seller=request.user)
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                form.save()
                messages.success(request, 'Item updated successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = ItemForm(instance=item)
        return render(request, 'hub/item_form.html', {'form': form, 'edit_mode': True})
    except Item.DoesNotExist:
        messages.error(request, 'Item not found or you do not have permission to edit it.')
        return redirect('profile')

@login_required
def item_delete(request, item_id):
    try:
        item = Item.objects.get(id=item_id, seller=request.user)
        if request.method == 'POST':
            item.delete()
            messages.success(request, 'Item deleted successfully!')
            return redirect('profile')
        return render(request, 'hub/item_confirm_delete.html', {'item': item})
    except Item.DoesNotExist:
        messages.error(request, 'Item not found or you do not have permission to delete it.')
        return redirect('profile')

# Cart functionality
@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'hub/cart.html', {
        'cart': cart,
        'cart_items': cart_items
    })

@login_required
def add_to_cart(request, item_id):
    try:
        item = Item.objects.get(id=item_id, is_active=True)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if item is already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            item=item,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        messages.success(request, f'{item.name} added to cart!')
        return redirect('cart')
    except Item.DoesNotExist:
        messages.error(request, 'Item not found.')
        return redirect('item_list')

@login_required
def remove_from_cart(request, cart_id):
    try:
        cart_item = CartItem.objects.get(id=cart_id, cart__user=request.user)
        item_name = cart_item.item.name
        cart_item.delete()
        messages.success(request, f'{item_name} removed from cart!')
    except CartItem.DoesNotExist:
        messages.error(request, 'Cart item not found.')
    
    return redirect('cart')

@login_required
def update_cart_quantity(request, cart_id):
    try:
        cart_item = CartItem.objects.get(id=cart_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    except (CartItem.DoesNotExist, ValueError):
        messages.error(request, 'Invalid request.')
    
    return redirect('cart')

# Checkout and Order functionality
@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')
    
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        
        if not shipping_address:
            messages.error(request, 'Please provide a shipping address.')
            total = sum(cart_item.get_total_price() for cart_item in cart_items)
            return render(request, 'hub/checkout.html', {
                'cart': cart,
                'cart_items': cart_items,
                'total': total
            })
        
        try:
            # Create orders for each seller
            seller_orders = {}
            
            for cart_item in cart_items:
                seller = cart_item.item.seller
                if seller not in seller_orders:
                    seller_orders[seller] = {
                        'order': Order.objects.create(
                            buyer=request.user,
                            seller=seller,
                            total_amount=0,
                            shipping_address=shipping_address,
                            payment_method=payment_method
                        ),
                        'items': []
                    }
                
                # Create order item
                order_item = OrderItem.objects.create(
                    order=seller_orders[seller]['order'],
                    item=cart_item.item,
                    quantity=cart_item.quantity,
                    price_at_time=cart_item.item.price or 0
                )
                
                seller_orders[seller]['items'].append(order_item)
                seller_orders[seller]['order'].total_amount += order_item.get_total_price()
                seller_orders[seller]['order'].save()
            
                            # Clear the cart
                cart.cartitem_set.all().delete()
                
                # Send notifications for each order
                for order_data in seller_orders.values():
                    order = order_data['order']
                    for order_item in order.orderitem_set.all():
                        # Notify seller
                        NotificationService.notify_item_sold(
                            seller=order_item.item.seller,
                            buyer=request.user,
                            item=order_item.item,
                            order=order
                        )
                        
                        # Notify buyer
                        NotificationService.notify_item_purchased(
                            buyer=request.user,
                            seller=order_item.item.seller,
                            item=order_item.item,
                            order=order
                        )
                
                # Redirect to payment for the first order
                if seller_orders:
                    first_order = list(seller_orders.values())[0]['order']
                    return redirect('payment_page', order_id=first_order.id)
                else:
                    messages.success(request, 'Order placed successfully! You will receive confirmation emails.')
                    return redirect('orders')
            
        except Exception as e:
            messages.error(request, f'Error processing order: {str(e)}')
    
    total = sum(cart_item.get_total_price() for cart_item in cart_items)
    return render(request, 'hub/checkout.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total': total
    })

@login_required
def orders(request):
    # Get orders where user is buyer
    buyer_orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    # Get orders where user is seller
    seller_orders = Order.objects.filter(seller=request.user).order_by('-created_at')
    
    
    
    return render(request, 'hub/orders.html', {
        'bought_orders': buyer_orders,
        'sold_orders': seller_orders
    })

@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        # Check if user is buyer or seller
        if order.buyer != request.user and order.seller != request.user:
            messages.error(request, 'You do not have permission to view this order.')
            return redirect('orders')
        
        order_items = order.orderitem_set.all()
        
        return render(request, 'hub/order_detail.html', {
            'order': order,
            'order_items': order_items
        })
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('orders')



@login_required
def payment_page(request, order_id):
    """Display payment page for an order"""
    try:
        order = Order.objects.get(id=order_id, buyer=request.user)
        total_amount = sum(item.get_total_price() for item in order.orderitem_set.all())
        
        return render(request, 'hub/payment.html', {
            'order': order,
            'total_amount': total_amount,
            'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
        })
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('orders')

def about_us(request):
    """About Us page"""
    return render(request, 'hub/about_us.html')

def contact_us(request):
    """Contact Us page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save to database
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact_us')
    
    return render(request, 'hub/contact_us.html')

def report_bug(request):
    """Report a Bug page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        bug_type = request.POST.get('bug_type')
        description = request.POST.get('description')
        steps = request.POST.get('steps')
        
        # Here you would typically save to database or send to support
        messages.success(request, 'Thank you for reporting this issue! Our team will investigate.')
        return redirect('report_bug')
    
    return render(request, 'hub/report_bug.html')

def help_center(request):
    """Help Center page"""
    return render(request, 'hub/help_center.html')

# Review System Views
@login_required
def add_review(request, item_id):
    """Add a review for an item"""
    item = get_object_or_404(Item, id=item_id)
    
    # Check if user has already reviewed this item
    existing_review = Review.objects.filter(item=item, user=request.user).first()
    if existing_review:
        messages.error(request, 'You have already reviewed this item.')
        return redirect('item_detail', item_id=item_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        
        if rating and title and comment:
            try:
                review = Review.objects.create(
                    item=item,
                    user=request.user,
                    rating=int(rating),
                    title=title,
                    comment=comment,
                    is_verified_purchase=True  # Assuming they can only review if they bought it
                )
                
                # Send notification to item owner
                NotificationService.notify_review_received(item.seller, request.user, item, review)
                
                messages.success(request, 'Review added successfully!')
                return redirect('item_detail', item_id=item_id)
            except Exception as e:
                messages.error(request, f'Failed to add review: {str(e)}')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'hub/add_review.html', {'item': item})

@login_required
def edit_review(request, review_id):
    """Edit a review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        
        if rating and title and comment:
            try:
                review.rating = int(rating)
                review.title = title
                review.comment = comment
                review.save()
                messages.success(request, 'Review updated successfully!')
                return redirect('item_detail', item_id=review.item.id)
            except Exception as e:
                messages.error(request, f'Failed to update review: {str(e)}')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'hub/edit_review.html', {'review': review})

@login_required
def delete_review(request, review_id):
    """Delete a review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        item_id = review.item.id
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('item_detail', item_id=item_id)
    
    return render(request, 'hub/delete_review.html', {'review': review})

# Notification Views
@login_required
def notifications(request):
    """View user notifications"""
    notifications = NotificationService.get_user_notifications(request.user)
    return render(request, 'hub/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    if NotificationService.mark_notification_read(notification_id, request.user):
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    NotificationService.mark_all_notifications_read(request.user)
    return JsonResponse({'success': True})

# Chatbot Views
def chatbot(request):
    """Enhanced chatbot interface"""
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        session_id = request.POST.get('session_id', str(uuid.uuid4()))
        
        if message:
            try:
                chatbot = EduCycleChatbot()
                response = chatbot.get_response(message, session_id)
                return JsonResponse({
                    'response': response,
                    'session_id': session_id,
                    'success': True
                })
            except Exception as e:
                return JsonResponse({
                    'response': "I'm sorry, I encountered an error. Please try again or contact support if the problem persists.",
                    'session_id': session_id,
                    'success': False,
                    'error': str(e)
                })
        else:
            return JsonResponse({
                'response': "Please enter a message to get help.",
                'session_id': session_id,
                'success': False
            })
    
    # For GET request, return the chatbot page
    try:
        chatbot = EduCycleChatbot()
        suggested_questions = chatbot.get_suggested_questions()
        welcome_message = chatbot.get_welcome_message()
        quick_stats = chatbot.get_quick_stats()
        
        return render(request, 'hub/chatbot.html', {
            'suggested_questions': suggested_questions,
            'welcome_message': welcome_message,
            'quick_stats': quick_stats
        })
    except Exception as e:
        # Fallback if chatbot fails to load
        return render(request, 'hub/chatbot.html', {
            'suggested_questions': [
                "How do I buy items?",
                "How do I sell items?",
                "How do I create an account?",
                "Is it safe to meet sellers?"
            ],
            'welcome_message': "Welcome to EduCycle! I'm here to help you with buying, selling, and using our platform.",
            'quick_stats': "Join our growing community of students!"
        })

def get_chat_history(request, session_id):
    """Get chat history for a session"""
    chatbot = EduCycleChatbot()
    history = chatbot.get_conversation_history(session_id)
    
    messages = []
    for msg in history:
        messages.append({
            'type': msg.message_type,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%H:%M')
        })
    
    return JsonResponse({'messages': messages})


