import asyncio
import stripe
from core.config import settings
from schemas.stripe_schemas import StripeWebhookEvent
from utils.exceptions import PaymentError
from utils.logger import logger
from fastapi import HTTPException, Request

from utils.stripe_helpers import process_successful_checkout


class StripePaymentServices:
    def __init__(self):
        self.stripe = stripe

    async def create_checkout_session(self, price_id: str) -> stripe.checkout.Session:
        """
        Crea una sesión de checkout para una suscripción.

        Args:
            price_id: ID del precio de Stripe

        Returns:
            Session: Sesión de checkout de Stripe
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                mode="subscription",
                success_url=f"{settings.FRONTEND_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.FRONTEND_URL}/cancel",
                # Opcional: Pasar metadata adicional
                metadata={"price_id": price_id},
            )
            return session
        except stripe.error.StripeError as e:
            logger.error(
                {
                    "message": "Error creating checkout session",
                    "error": str(e),
                    "price_id": price_id,
                }
            )
            raise PaymentError(str(e))

    async def create_checkout_session(self, request: Request):
        """Crea una sesión de checkout"""
        try:
            # Obtener el priceId del request
            data = await request.json()
            price_id = data.get("priceId")

            # Mapeo de precios
            price_mapping = {
                "price_basic": {
                    "amount": 1900,  # $19.00
                    "name": "Plan Básico",
                    "description": "Acceso a cursos básicos",
                },
                "price_premium": {
                    "amount": 3900,  # $39.00
                    "name": "Plan Premium",
                    "description": "Acceso a todos los cursos",
                },
            }

            price_data = price_mapping.get(price_id)
            if not price_data:
                raise PaymentError("Invalid price ID")

            # Primero crear el producto
            product = stripe.Product.create(
                name=price_data["name"], description=price_data["description"]
            )

            # Luego crear el precio asociado al producto
            price = stripe.Price.create(
                unit_amount=price_data["amount"],
                currency="usd",
                recurring={"interval": "month"},
                product=product.id,  # Usar el ID del producto creado
            )

            # Crear la sesión de checkout
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price.id,
                        "quantity": 1,
                    }
                ],
                mode="subscription",
                success_url=f"{settings.FRONTEND_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.FRONTEND_URL}/cancel",
                metadata={"price_id": price_id, "plan_name": price_data["name"]},
            )

            logger.info(
                {
                    "message": "Checkout session created",
                    "session_id": checkout_session.id,
                    "price_id": price.id,
                    "product_id": product.id,
                }
            )

            return {"url": checkout_session.url}

        except stripe.error.StripeError as e:
            logger.error(
                {
                    "message": "Stripe error",
                    "error": str(e),
                    "error_type": type(e).__name__,
                }
            )
            raise PaymentError(str(e))
        except Exception as e:
            logger.error(
                {
                    "message": "Error creating checkout session",
                    "error": str(e),
                    "error_type": type(e).__name__,
                }
            )
            raise PaymentError("Error creating checkout session")

    async def handle_payment_failed(self, event: StripeWebhookEvent):
        """
        Maneja eventos de pago fallido.

        Args:
            event (StripeWebhookEvent): Evento de pago fallido.

        Raises:
            Exception: Si hay un error al procesar el fallo del pago.
        """
        try:
            invoice = event.data.object
            customer_email = invoice.get("customer_email")

            logger.info(
                {
                    "message": "Payment failed",
                    "invoice_id": invoice.get("id"),
                    "customer_email": customer_email,
                }
            )

            # Aquí podrías agregar lógica para notificar al cliente

            return {
                "status": "failed",
                "message": "Payment failed",
                "invoice_id": invoice.get("id"),
            }
        except Exception as e:
            logger.error(
                {
                    "message": "Error processing payment failure",
                    "error": str(e),
                    "event_id": event.id,
                }
            )
            raise PaymentError(str(e))

    async def handle_invoice_paid(self, event: StripeWebhookEvent):
        """
        Maneja eventos de factura pagada.

        Args:
            event (StripeWebhookEvent): Evento de factura pagada.

        Raises:
            Exception: Si hay un error al procesar el pago de la factura.
        """
        try:
            invoice = event.data.object

            logger.info(
                {
                    "message": "Invoice paid",
                    "invoice_id": invoice.get("id"),
                    "customer_id": invoice.get("customer"),
                }
            )

            return {
                "status": "success",
                "message": "Invoice paid successfully",
                "invoice_id": invoice.get("id"),
            }
        except Exception as e:
            logger.error(
                {
                    "message": "Error processing invoice payment",
                    "error": str(e),
                    "event_id": event.id,
                }
            )
            raise PaymentError(str(e))
