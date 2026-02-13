import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from orders.models import Order
from .models import Payment
from .email import send_payment_confirmation_email, send_order_confirmation_email

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import logging
from django.contrib.auth.decorators import login_required
from django.utils import timezone

logger = logging.getLogger(__name__)

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def start_payment(request, order_id):
    """Initiate Razorpay payment"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    amount = int(order.total_price * 100)  # paise

    try:
        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })
        
    except Exception as e:
        logger.error(f"Error creating Razorpay order: {str(e)}")
        return render(request, "payments/error.html", {
            "message": "Failed to initiate payment. Please try again."
        })

    # Store razorpay_order_id in Order model
    order.razorpay_order_id = razorpay_order["id"]
    order.save()

    # Create Payment record
    payment = Payment.objects.create(
        order=order,
        razorpay_order_id=razorpay_order["id"]
    )

    return render(request, "payments/pay.html", {
        "order": order,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "razorpay_order_id": razorpay_order["id"],
    })


@login_required
def payment_success(request):
    """Show payment success page"""
    # Get the last paid order for the user
    order = Order.objects.filter(user=request.user, is_paid=True).order_by('-paid_at').first()
    
    if order and order.payment:
        return render(request, "payments/success.html", {
            "order": order,
            "payment": order.payment
        })
    
    return redirect('product_list')


@csrf_exempt
def verify_payment(request):
    """Verify Razorpay payment signature and update order/payment records"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        # Extract payment data
        if request.POST:
            data = {
                "razorpay_order_id": request.POST.get("razorpay_order_id"),
                "razorpay_payment_id": request.POST.get("razorpay_payment_id"),
                "razorpay_signature": request.POST.get("razorpay_signature"),
            }
        else:
            import json
            body = json.loads(request.body.decode("utf-8"))
            data = {
                "razorpay_order_id": body.get("razorpay_order_id"),
                "razorpay_payment_id": body.get("razorpay_payment_id"),
                "razorpay_signature": body.get("razorpay_signature"),
            }

        # Verify Razorpay signature
        try:
            client.utility.verify_payment_signature(data)
            logger.info(f"Payment signature verified for order: {data['razorpay_order_id']}")
        except razorpay.BadRequestError as e:
            logger.error(f"Payment signature verification failed: {str(e)}")
            return JsonResponse({"error": "Payment verification failed"}, status=400)

        # Get the order using razorpay_order_id
        try:
            order = Order.objects.get(razorpay_order_id=data["razorpay_order_id"])
        except Order.DoesNotExist:
            logger.error(f"Order not found for razorpay_order_id: {data['razorpay_order_id']}")
            return JsonResponse({"error": "Order not found"}, status=404)

        # Update Order model
        order.is_paid = True
        order.status = "paid"
        order.payment_id = data["razorpay_payment_id"]
        order.paid_at = timezone.now()
        order.save()
        logger.info(f"Order {order.id} marked as paid")

        # Update Payment record
        try:
            payment = Payment.objects.get(razorpay_order_id=data["razorpay_order_id"])
            payment.razorpay_payment_id = data["razorpay_payment_id"]
            payment.razorpay_signature = data["razorpay_signature"]
            payment.status = "paid"
            payment.paid_at = timezone.now()
            payment.save()
            logger.info(f"Payment record updated for order {order.id}")
        except Payment.DoesNotExist:
            logger.warning(f"Payment record not found for order {order.id}, creating new one")
            payment = Payment.objects.create(
                order=order,
                razorpay_order_id=data["razorpay_order_id"],
                razorpay_payment_id=data["razorpay_payment_id"],
                razorpay_signature=data["razorpay_signature"],
                status="paid",
                paid_at=timezone.now()
            )

        # Send confirmation emails
        try:
            send_payment_confirmation_email(payment)
        except Exception as e:
            logger.error(f"Failed to send payment confirmation email: {e}")
        send_order_confirmation_email(order)
        logger.info(f"Confirmation emails sent for order {order.id}")

        return redirect("payment_success")

    except Exception as e:
        logger.error(f"Unexpected error during payment verification: {str(e)}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)