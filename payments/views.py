import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from orders.models import Order
from .models import Payment

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def start_payment(request, order_id):

    order = get_object_or_404(Order, id=order_id)

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




@csrf_exempt
def payment_success(request):

    data = request.POST

    try:
        # Verify the payment signature
        client.utility.verify_payment_signature(data)
    except razorpay.BadRequestError as e:
        logger.error(f"Payment signature verification failed: {str(e)}")
        return render(request, "payments/error.html", {
            "message": "Payment verification failed. Please contact support.",
            "order_id": data.get("razorpay_order_id")
        })
    except Exception as e:
        logger.error(f"Unexpected error during payment verification: {str(e)}")
        return render(request, "payments/error.html", {
            "message": "An unexpected error occurred. Please contact support."
        })

    try:
        payment = Payment.objects.get(
            razorpay_order_id=data["razorpay_order_id"]
        )
    except Payment.DoesNotExist:
        logger.error(f"Payment record not found for order: {data.get('razorpay_order_id')}")
        return render(request, "payments/error.html", {
            "message": "Payment record not found. Please contact support."
        })

    # Update payment details
    payment.razorpay_payment_id = data.get("razorpay_payment_id", "")
    payment.razorpay_signature = data.get("razorpay_signature", "")
    payment.status = "paid"
    payment.save()

    # Update order
    order = payment.order
    order.status = "paid"
    order.save()

    logger.info(f"Payment successful for order {order.id}")

    return render(request, "payments/success.html", {
        "order": order,
        "payment": payment
    })