import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

# Validate configuration on module import
if not hasattr(settings, 'BREVO_API_KEY') or not settings.BREVO_API_KEY:
    logger.warning("⚠️ BREVO_API_KEY is not configured. Email sending will fail.")
    logger.warning("Please set BREVO_API_KEY in your .env file")
else:
    logger.info("✓ BREVO_API_KEY is configured")

if not hasattr(settings, 'DEFAULT_FROM_EMAIL') or not settings.DEFAULT_FROM_EMAIL:
    logger.warning("⚠️ DEFAULT_FROM_EMAIL is not configured")
else:
    logger.info(f"✓ Using sender email: {settings.DEFAULT_FROM_EMAIL}")


def get_brevo_client():
    if not settings.BREVO_API_KEY:
        logger.error("BREVO_API_KEY is not configured in settings")
        raise ValueError("BREVO_API_KEY environment variable is missing")
    
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY
    return sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )


def send_order_confirmation_email(order):
    try:
        api_instance = get_brevo_client()

        subject = f"Order Confirmation #{order.id}"

        context = {
            "order": order,
            "user": order.user,
        }

        html_content = render_to_string(
            "emails/order_confirmation.html",
            context
        )

        text_content = strip_tags(html_content)

        sender = {
            "name": "Ecommerce Support",
            "email": "priyanshkurmi2004@gmail.com"
        }

        to = [{
            "email": order.user.email,
            "name": order.user.username
        }]

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            sender=sender,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

        api_instance.send_transac_email(send_smtp_email)

        logger.info(f"Order email sent for order {order.id}")
        return True

    except ApiException as e:
        logger.error(f"Brevo API error: {e.status} - {e.reason} - {e.body}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending order email: {type(e).__name__} - {str(e)}", exc_info=True)
        return False


def send_payment_confirmation_email(payment):
    order = payment.order

    try:
        api_instance = get_brevo_client()

        subject = f"Payment Confirmed #{order.id}"

        context = {
            "order": order,
            "payment": payment,
            "user": order.user,
        }

        html_content = render_to_string(
            "emails/payment_confirmation.html",
            context
        )

        text_content = strip_tags(html_content)

        sender = {
            "name": "Ecommerce Support",
            "email": "priyanshkurmi2004@gmail.com"
        }

        to = [{
            "email": order.user.email,
            "name": order.user.username
        }]

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            sender=sender,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

        api_instance.send_transac_email(send_smtp_email)

        logger.info(f"Payment email sent for payment {payment.id}")
        return True

    except ApiException as e:
        logger.error(f"Brevo API error: {e.status} - {e.reason} - {e.body}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending payment email: {type(e).__name__} - {str(e)}", exc_info=True)
        return False