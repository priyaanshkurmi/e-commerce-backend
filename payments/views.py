import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404

from orders.models import Order
from .models import Payment

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def start_payment(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    amount = int(order.total_price * 100)  # paise

    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
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

    client.utility.verify_payment_signature(data)

    payment = Payment.objects.get(
        razorpay_order_id=data["razorpay_order_id"]
    )

    payment.razorpay_payment_id = data["razorpay_payment_id"]
    payment.razorpay_signature = data["razorpay_signature"]
    payment.status = "paid"
    payment.save()

    # Update order
    order = payment.order
    order.status = "paid"
    order.save()

    return HttpResponse("Payment Successful")