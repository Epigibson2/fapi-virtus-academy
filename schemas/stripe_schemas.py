from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
from decimal import Decimal


class StripeEventType(str, Enum):
    # Checkout Events
    CHECKOUT_COMPLETED = "checkout.session.completed"
    CHECKOUT_EXPIRED = "checkout.session.expired"

    # Subscription Events
    SUBSCRIPTION_CREATED = "customer.subscription.created"
    SUBSCRIPTION_UPDATED = "customer.subscription.updated"
    SUBSCRIPTION_DELETED = "customer.subscription.deleted"
    SUBSCRIPTION_TRIAL_ENDING = "customer.subscription.trial_will_end"

    # Invoice Events
    INVOICE_PAID = "invoice.paid"
    INVOICE_PAYMENT_FAILED = "invoice.payment_failed"

    # Payment Events
    PAYMENT_SUCCEEDED = "payment_intent.succeeded"
    PAYMENT_FAILED = "payment_intent.payment_failed"

    # Customer Events
    CUSTOMER_CREATED = "customer.created"
    CUSTOMER_UPDATED = "customer.updated"
    CUSTOMER_DELETED = "customer.deleted"

    # Additional Invoice Events
    INVOICE_UPCOMING = "invoice.upcoming"
    INVOICE_FINALIZED = "invoice.finalized"
    INVOICE_VOIDED = "invoice.voided"

    # Additional Price Event
    PRICE_CREATED = "price.created"
    PRICE_UPDATED = "price.updated"

    # Additional Product Events
    PRODUCT_CREATED = "product.created"
    PRODUCT_UPDATED = "product.updated"
    # Additional Payment Events
    PAYMENT_INTENT_CREATED = "payment_intent.created"
    PAYMENT_INTENT_CANCELED = "payment_intent.canceled"
    PAYMENT_INTENT_PROCESSING = "payment_intent.processing"


class StripeCustomer(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    created: datetime


class StripeSubscription(BaseModel):
    id: str
    customer: str
    status: str
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool
    canceled_at: Optional[datetime] = None


class StripePrice(BaseModel):
    id: str
    product: str
    unit_amount: int
    currency: str


class StripeInvoice(BaseModel):
    id: str
    customer: str
    subscription: Optional[str]
    status: str
    amount_paid: int
    currency: str


class StripeWebhookEvent(BaseModel):
    id: str
    type: StripeEventType
    created: datetime
    data: Dict[str, Any]
    livemode: bool = False


class WebhookResponse(BaseModel):
    status: str
    event_id: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    processed_at: datetime = Field(default_factory=datetime.now)


class CheckoutSessionResponse(BaseModel):
    url: str


class ProductCreate(BaseModel):
    """
    Esquema para crear un nuevo producto.

    Attributes:
        name (str): Nombre del producto.
        description (str): Descripción del producto.
        price (Decimal): Precio del producto.
        interval (str): Intervalo de facturación ('month' o 'year').
        currency (str): Moneda del precio (default: 'usd').
    """

    name: str
    description: str
    price: Decimal
    interval: str = "month"
    currency: str = "usd"


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price_id: str
    price: Decimal
    interval: str
    currency: str
    active: bool


class SubscriptionCreate(BaseModel):
    price_id: str
    customer_email: str


class SubscriptionResponse(BaseModel):
    """
    Esquema para la respuesta de una suscripción.

    Attributes:
        id (str): ID de la suscripción en Stripe.
        status (str): Estado actual de la suscripción.
        customer_id (str): ID del cliente en Stripe.
        customer_email (str): Email del cliente.
        product_name (str): Nombre del producto suscrito.
        price_amount (float): Monto del precio.
        currency (str): Moneda del precio.
        interval (str): Intervalo de facturación.
        current_period_end (int): Timestamp del fin del período actual.
        cancel_at_period_end (bool): Si la suscripción se cancelará al final del período.
    """

    id: str
    status: str
    customer_id: str = Field(default="N/A")
    customer_email: str = Field(default="N/A")
    product_name: str = Field(default="N/A")
    price_amount: float = Field(default=0.0)
    currency: str = Field(default="usd")
    interval: str = Field(default="month")
    current_period_end: int
    cancel_at_period_end: bool = Field(default=False)

    class Config:
        from_attributes = True

    # Propiedades calculadas
    @property
    def current_period_end_date(self) -> datetime:
        return datetime.fromtimestamp(self.current_period_end)

    @property
    def formatted_price(self) -> str:
        return f"{self.price_amount} {self.currency.upper()}/{self.interval}"
