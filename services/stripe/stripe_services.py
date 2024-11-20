import stripe
from core.config import settings
from services.stripe.stripe_product_services import StripeProductServices
from services.stripe.stripe_customer_services import StripeCustomerServices
from services.stripe.stripe_webhook_services import StripeWebhookServices
from services.stripe.stripe_payment_services import StripePaymentServices
from services.stripe.stripe_subscription_services import StripeSubscriptionServices


class StripeServices:
    """
    Servicio para manejar las operaciones con Stripe.
    Incluye manejo de productos, suscripciones y webhooks.
    """

    def __init__(self):
        """
        Inicializa el servicio de Stripe con la API key configurada.
        """
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.product_services = StripeProductServices()
        self.customer_services = StripeCustomerServices()
        self.webhook_services = StripeWebhookServices(settings.STRIPE_WEBHOOK_SECRET)
        self.payment_services = StripePaymentServices()
        self.subscription_services = StripeSubscriptionServices()

    async def process_webhook_async(self, *args, **kwargs):
        return await self.webhook_services.process_webhook_async(*args, **kwargs)

    async def webhook_received(self, *args, **kwargs):
        return await self.webhook_services.webhook_received(*args, **kwargs)

    async def handle_checkout_completed(self, *args, **kwargs):
        return await self.webhook_services.handle_checkout_completed(*args, **kwargs)

    async def create_checkout_session(self, *args, **kwargs):
        return await self.payment_services.create_checkout_session(*args, **kwargs)

    async def create_product(self, *args, **kwargs):
        return await self.product_services.create_product(*args, **kwargs)

    async def list_products(self, *args, **kwargs):
        return await self.product_services.list_products(*args, **kwargs)

    async def create_customer(self, *args, **kwargs):
        return await self.customer_services.create_customer(*args, **kwargs)

    async def process_webhook(self, *args, **kwargs):
        return await self.webhook_services.process_webhook(*args, **kwargs)

    async def handle_invoice_paid(self, *args, **kwargs):
        return await self.payment_services.handle_invoice_paid(*args, **kwargs)

    async def handle_payment_failed(self, *args, **kwargs):
        return await self.payment_services.handle_payment_failed(*args, **kwargs)

    async def search_subscription(self, *args, **kwargs):
        return await self.subscription_services.search_subscription(*args, **kwargs)

    async def create_subscription(self, *args, **kwargs):
        return await self.subscription_services.create_subscription(*args, **kwargs)

    async def cancel_subscription(self, *args, **kwargs):
        return await self.subscription_services.cancel_subscription(*args, **kwargs)

    async def update_subscription(self, *args, **kwargs):
        return await self.subscription_services.update_subscription(*args, **kwargs)

    async def get_subscription(self, *args, **kwargs):
        return await self.subscription_services.get_subscription(*args, **kwargs)
