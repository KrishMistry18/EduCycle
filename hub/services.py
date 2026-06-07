from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from .models import Notification, Item, Order, Review
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def send_email_notification(user, subject, message, template_name=None, context=None):
        """Send email notification to user"""
        try:
            if template_name and context:
                message = render_to_string(template_name, context)
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"Email sent to {user.email}: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {user.email}: {str(e)}")
            return False

    @staticmethod
    def create_in_app_notification(user, notification_type, title, message, related_item=None, related_order=None):
        """Create in-app notification"""
        try:
            notification = Notification.objects.create(
                user=user,
                notification_type=notification_type,
                title=title,
                message=message,
                related_item=related_item,
                related_order=related_order
            )
            logger.info(f"In-app notification created for {user.username}: {title}")
            return notification
        except Exception as e:
            logger.error(f"Failed to create notification for {user.username}: {str(e)}")
            return None

    @staticmethod
    def notify_item_added(user, item):
        """Notify when item is added"""
        subject = f"Item '{item.name}' Successfully Added"
        message = f"""
        Hello {user.first_name or user.username},
        
        Your item '{item.name}' has been successfully added to EduCycle!
        
        Item Details:
        - Name: {item.name}
        - Category: {item.get_category_display()}
        - Price: ₹{item.price if item.price else 'Swap only'}
        
        You can view and manage your listing in your profile.
        
        Best regards,
        EduCycle Team
        """
        
        # Send email
        NotificationService.send_email_notification(user, subject, message)
        
        # Create in-app notification
        NotificationService.create_in_app_notification(
            user=user,
            notification_type='item_added',
            title='Item Added Successfully',
            message=f'Your item "{item.name}" has been added to the marketplace.',
            related_item=item
        )

    @staticmethod
    def notify_item_sold(seller, buyer, item, order):
        """Notify seller when item is sold"""
        subject = f"Congratulations! Your item '{item.name}' has been sold!"
        message = f"""
        Hello {seller.first_name or seller.username},
        
        Great news! Your item '{item.name}' has been purchased by {buyer.first_name or buyer.username}.
        
        Order Details:
        - Order ID: {order.id}
        - Item: {item.name}
        - Buyer: {buyer.first_name or buyer.username} ({buyer.email})
        - Total Amount: ₹{order.total_amount}
        
        Please contact the buyer to arrange pickup/delivery.
        
        Best regards,
        EduCycle Team
        """
        
        # Send email to seller
        NotificationService.send_email_notification(seller, subject, message)
        
        # Create in-app notification for seller
        NotificationService.create_in_app_notification(
            user=seller,
            notification_type='item_sold',
            title='Item Sold!',
            message=f'Your item "{item.name}" has been sold to {buyer.first_name or buyer.username}.',
            related_item=item,
            related_order=order
        )

    @staticmethod
    def notify_item_purchased(buyer, seller, item, order):
        """Notify buyer when item is purchased"""
        subject = f"Order Confirmed - '{item.name}'"
        message = f"""
        Hello {buyer.first_name or buyer.username},
        
        Your order has been confirmed!
        
        Order Details:
        - Order ID: {order.id}
        - Item: {item.name}
        - Seller: {seller.first_name or seller.username}
        - Total Amount: ₹{order.total_amount}
        
        Please contact the seller to arrange pickup/delivery.
        
        Best regards,
        EduCycle Team
        """
        
        # Send email to buyer
        NotificationService.send_email_notification(buyer, subject, message)
        
        # Create in-app notification for buyer
        NotificationService.create_in_app_notification(
            user=buyer,
            notification_type='item_purchased',
            title='Order Confirmed!',
            message=f'Your order for "{item.name}" has been confirmed.',
            related_item=item,
            related_order=order
        )

    @staticmethod
    def notify_review_received(item_owner, reviewer, item, review):
        """Notify item owner when they receive a review"""
        subject = f"New Review for '{item.name}'"
        message = f"""
        Hello {item_owner.first_name or item_owner.username},
        
        You have received a new review for your item '{item.name}'.
        
        Review Details:
        - Reviewer: {reviewer.first_name or reviewer.username}
        - Rating: {review.rating}/5 stars
        - Comment: {review.comment[:100]}{'...' if len(review.comment) > 100 else ''}
        
        You can view the full review on your item page.
        
        Best regards,
        EduCycle Team
        """
        
        # Send email to item owner
        NotificationService.send_email_notification(item_owner, subject, message)
        
        # Create in-app notification
        NotificationService.create_in_app_notification(
            user=item_owner,
            notification_type='review_received',
            title='New Review Received',
            message=f'You received a {review.rating}-star review for "{item.name}".',
            related_item=item
        )

    @staticmethod
    def notify_order_status_update(user, order, new_status):
        """Notify user when order status changes"""
        status_display = dict(Order.STATUS_CHOICES)[new_status]
        subject = f"Order Status Update - {status_display}"
        message = f"""
        Hello {user.first_name or user.username},
        
        Your order status has been updated.
        
        Order Details:
        - Order ID: {order.id}
        - New Status: {status_display}
        - Updated: {order.updated_at.strftime('%B %d, %Y at %I:%M %p')}
        
        You can track your order in your orders page.
        
        Best regards,
        EduCycle Team
        """
        
        # Send email
        NotificationService.send_email_notification(user, subject, message)
        
        # Create in-app notification
        NotificationService.create_in_app_notification(
            user=user,
            notification_type='order_status',
            title=f'Order Status: {status_display}',
            message=f'Your order #{order.id} status has been updated to {status_display}.',
            related_order=order
        )

    @staticmethod
    def notify_message_received(receiver, sender, item, message_content):
        """Notify user when they receive a message"""
        subject = f"New Message about '{item.name}'"
        message = f"""
        Hello {receiver.first_name or receiver.username},
        
        You have received a new message from {sender.first_name or sender.username} about your item '{item.name}'.
        
        Message: {message_content[:100]}{'...' if len(message_content) > 100 else ''}
        
        You can view and respond to this message in your inbox.
        
        Best regards,
        EduCycle Team
        """
        
        # Send email
        NotificationService.send_email_notification(receiver, subject, message)
        
        # Create in-app notification
        NotificationService.create_in_app_notification(
            user=receiver,
            notification_type='message_received',
            title='New Message Received',
            message=f'You have a new message from {sender.first_name or sender.username} about "{item.name}".',
            related_item=item
        )

    @staticmethod
    def get_user_notifications(user, unread_only=False):
        """Get notifications for a user"""
        notifications = Notification.objects.filter(user=user)
        if unread_only:
            notifications = notifications.filter(is_read=False)
        return notifications

    @staticmethod
    def mark_notification_read(notification_id, user):
        """Mark a notification as read"""
        try:
            notification = Notification.objects.get(id=notification_id, user=user)
            notification.is_read = True
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False

    @staticmethod
    def mark_all_notifications_read(user):
        """Mark all notifications as read for a user"""
        Notification.objects.filter(user=user, is_read=False).update(is_read=True) 