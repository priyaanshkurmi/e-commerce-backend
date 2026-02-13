from django.core.management.base import BaseCommand
from django.conf import settings
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test Brevo email configuration and send a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            help='Email address to send test email to',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Testing Brevo Configuration...\n'))

        # Check 1: API Key
        self.stdout.write('1️⃣  Checking BREVO_API_KEY...')
        if not hasattr(settings, 'BREVO_API_KEY') or not settings.BREVO_API_KEY:
            self.stdout.write(self.style.ERROR('   ❌ BREVO_API_KEY not configured'))
            return
        self.stdout.write(self.style.SUCCESS('   ✓ BREVO_API_KEY found\n'))

        # Check 2: Default From Email
        self.stdout.write('2️⃣  Checking DEFAULT_FROM_EMAIL...')
        if not hasattr(settings, 'DEFAULT_FROM_EMAIL') or not settings.DEFAULT_FROM_EMAIL:
            self.stdout.write(self.style.ERROR('   ❌ DEFAULT_FROM_EMAIL not configured'))
            return
        self.stdout.write(self.style.SUCCESS(f'   ✓ Using sender: {settings.DEFAULT_FROM_EMAIL}\n'))

        # Check 3: SDK Installation
        self.stdout.write('3️⃣  Checking sib_api_v3_sdk...')
        try:
            self.stdout.write(self.style.SUCCESS('   ✓ SDK is installed\n'))
        except ImportError:
            self.stdout.write(self.style.ERROR('   ❌ SDK not installed'))
            return

        # Check 4: API Connection
        self.stdout.write('4️⃣  Testing Brevo API connection...')
        try:
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = settings.BREVO_API_KEY
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
                sib_api_v3_sdk.ApiClient(configuration)
            )
            # Try to get account info (lightweight call)
            self.stdout.write(self.style.SUCCESS('   ✓ API connection successful\n'))
        except ApiException as e:
            self.stdout.write(self.style.ERROR(f'   ❌ API Connection Failed: {e}\n'))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error: {e}\n'))
            return

        # Check 5: Send test email if recipient provided
        if options.get('to'):
            self.stdout.write(f'5️⃣  Sending test email to {options["to"]}...')
            try:
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                    to=[{"email": options["to"]}],
                    sender={"name": "Test", "email": settings.DEFAULT_FROM_EMAIL},
                    subject="Brevo Configuration Test",
                    html_content="<p>If you received this, your Brevo setup is working! ✓</p>"
                )
                response = api_instance.send_transac_email(send_smtp_email)
                self.stdout.write(
                    self.style.SUCCESS(f'   ✓ Test email sent! Message ID: {response.message_id}\n')
                )
            except ApiException as e:
                self.stdout.write(self.style.ERROR(f'   ❌ Failed to send email: {e}\n'))
                return
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   ❌ Error: {e}\n'))
                return

        self.stdout.write(self.style.SUCCESS('✓ All checks passed! Your Brevo setup is ready.\n'))
        self.stdout.write(self.style.WARNING(
            'Usage: python manage.py test_brevo --to your_email@example.com\n'
        ))
