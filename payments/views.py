import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from orders.models import Order
from .models import Payment

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import logging
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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



@login_required
def payment_success(request):
    return render(request, "payments/success.html")



@csrf_exempt
def verify_payment(request):

    if request.method == "POST":

        if request.POST:

            data = {
                "razorpay_order_id": request.POST.get("razorpay_order_id"),
                "razorpay_payment_id": request.POST.get("razorpay_payment_id"),
                "razorpay_signature": request.POST.get("razorpay_signature"),
            }

        else:
            import json
            data = json.loads(request.body.decode("utf-8"))

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            client.utility.verify_payment_signature(data)

            return redirect("payment_success")

        except:

            return redirect("product_list")
        