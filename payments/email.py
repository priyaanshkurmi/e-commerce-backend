from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


def send_order_confirmation_email(order):
    """Send order confirmation email after successful payment"""
    
    try:
        subject = f"Order Confirmation #{order.id} - Thank you for your purchase!"
        
        # Context for email template
        context = {
            'order': order,
            'customer_name': order.user.get_full_name() or order.user.username,
            'order_date': order.created_at.strftime("%B %d, %Y"),
            'order_id': order.id,
            'order_total': order.total_price,
            'items_count': order.items.count(),
        }
        
        # Render HTML email
        html_message = render_to_string(
            'emails/order_confirmation.html',
            context
        )
        
        # Create plain text version
        text_message = strip_tags(html_message)
        
        # Create email with both plain text and HTML
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.user.email]
        )
        
        email.attach_alternative(html_message, "text/html")
        
        # Send email
        email.send(fail_silently=False)
        
        logger.info(f"Order confirmation email sent to {order.user.email} for order {order.id}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error sending order confirmation email for order {order.id}: {str(e)}")
        return False


def send_payment_confirmation_email(payment):
    """Send payment confirmation email after successful payment"""
    
    order = payment.order
    
    try:
        subject = f"Payment Confirmed - Order #{order.id}"
        
        context = {
            'order': order,
            'payment': payment,
            'customer_name': order.user.get_full_name() or order.user.username,
            'payment_id': payment.razorpay_payment_id,
            'paid_amount': order.total_price,
            'payment_date': payment.paid_at.strftime("%B %d, %Y %I:%M %p") if payment.paid_at else "N/A",
        }
        
        html_message = render_to_string(
            'emails/payment_confirmation.html',
            context
        )
        
        text_message = strip_tags(html_message)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.user.email]
        )
        
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"Payment confirmation email sent to {order.user.email} for payment {payment.id}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error sending payment confirmation email for payment {payment.id}: {str(e)}")
        return False
