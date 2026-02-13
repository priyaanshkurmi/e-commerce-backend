import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def get_brevo_client():
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY
    return sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )


def send_order_confirmation_email(order):

    try:
        api_instance = get_brevo_client()

        subject = f"Order Confirmation #{order.id}"

        html_content = f"""
        <h2>Thank you for your order!</h2>
        <p>Order ID: {order.id}</p>
        <p>Total: ₹{order.total_price}</p>
        <p>Status: {order.status}</p>
        """

        sender = {
            "name": "Ecommerce Support",
            "email": "support@yourdomain.com"
        }

        to = [{
            "email": order.user.email,
            "name": order.user.username
        }]

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            sender=sender,
            subject=subject,
            html_content=html_content
        )

        api_instance.send_transac_email(send_smtp_email)

        logger.info(f"Order email sent for order {order.id}")
        return True

    except ApiException as e:
        logger.error(f"Brevo error: {e}")
        return False


def send_payment_confirmation_email(payment):

    order = payment.order

    try:
        api_instance = get_brevo_client()

        subject = f"Payment Confirmed #{order.id}"

        html_content = f"""
        <h2>Payment Successful</h2>
        <p>Order: {order.id}</p>
        <p>Payment ID: {payment.razorpay_payment_id}</p>
        <p>Amount: ₹{order.total_price}</p>
        """

        sender = {
            "name": "Ecommerce Support",
            "email": "support@yourdomain.com"
        }

        to = [{
            "email": order.user.email,
            "name": order.user.username
        }]

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            sender=sender,
            subject=subject,
            html_content=html_content
        )

        api_instance.send_transac_email(send_smtp_email)

        logger.info(f"Payment email sent for payment {payment.id}")
        return True

    except ApiException as e:
        logger.error(f"Brevo error: {e}")
        return False