import asyncio
from typing import Dict, Any, Callable, Optional
import stripe
from schemas.stripe_schemas import StripeWebhookEvent
from utils.exceptions import PaymentError, WebhookError
from fastapi import Request, BackgroundTasks
from utils.logger import logger
from schemas.stripe_schemas import StripeEventType
from utils.stripe_helpers import process_successful_checkout


class StripeWebhookServices:
    """Servicio para manejar webhooks de Stripe"""

    def __init__(self, webhook_secret: str):
        """
        Inicializa el servicio de webhooks.

        Args:
            webhook_secret (str): Secret para verificar webhooks de Stripe
        """
        self.webhook_secret = webhook_secret
        self.stripe = stripe
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Configura el mapeo de eventos a handlers"""
        self._handlers = {
            StripeEventType.CHECKOUT_COMPLETED: self.handle_checkout_completed,
            StripeEventType.SUBSCRIPTION_CREATED: self.handle_subscription_created,
            StripeEventType.SUBSCRIPTION_UPDATED: self.handle_subscription_updated,
            StripeEventType.SUBSCRIPTION_DELETED: self.handle_subscription_deleted,
            StripeEventType.INVOICE_PAID: self.handle_invoice_paid,
            StripeEventType.INVOICE_PAYMENT_FAILED: self.handle_payment_failed,
        }

    def get_event_handler(self, event_type: StripeEventType) -> Optional[Callable]:
        """
        Obtiene el handler para un tipo de evento específico.

        Args:
            event_type (StripeEventType): Tipo de evento a manejar

        Returns:
            Optional[Callable]: Handler para el evento o None si no existe
        """
        return self._handlers.get(event_type)

    async def webhook_received(
        self, request: Request, background_tasks: BackgroundTasks
    ) -> dict:
        """Punto de entrada principal para webhooks"""
        try:
            event = await self._verify_webhook(request)
            return await self._process_webhook(event, background_tasks)
        except Exception as e:
            self._handle_webhook_error(e)

    async def _verify_webhook(self, request: Request) -> stripe.Event:
        """
        Verifica la firma del webhook y construye el evento.

        Args:
            request (Request): Request entrante con el webhook

        Returns:
            stripe.Event: Evento verificado de Stripe

        Raises:
            WebhookError: Si hay problemas con la verificación
        """
        stripe_signature = request.headers.get("stripe-signature")
        if not stripe_signature:
            raise WebhookError("No stripe-signature in headers")

        payload = await request.body()

        try:
            return stripe.Webhook.construct_event(
                payload=payload, sig_header=stripe_signature, secret=self.webhook_secret
            )
        except stripe.error.SignatureVerificationError as e:
            logger.error(
                {
                    "message": "Invalid webhook signature",
                    "error": str(e),
                    "signature_prefix": (
                        stripe_signature[:30] + "..." if stripe_signature else None
                    ),
                }
            )
            raise WebhookError("Invalid webhook signature")

    async def process_webhook_async(self, event: stripe.Event) -> Dict[str, Any]:
        """
        Procesa eventos de webhook de manera asíncrona.
        """
        try:
            logger.info(
                {
                    "message": "Processing webhook event",
                    "event_type": event.type,
                    "event_id": event.id,
                }
            )

            # Si el evento no está en nuestros handlers, lo registramos pero no lo tratamos como error
            if event.type not in self._handlers:
                logger.info(
                    {
                        "message": "Unhandled event type - skipping",
                        "event_type": event.type,
                        "event_id": event.id,
                    }
                )
                return {
                    "status": "skipped",
                    "message": f"Event type {event.type} is not handled",
                }

            handler = self._handlers[event.type]
            result = await handler(event)

            logger.info(
                {
                    "message": "Webhook processed successfully",
                    "event_type": event.type,
                    "event_id": event.id,
                }
            )

            return result

        except Exception as e:
            logger.error(
                {
                    "message": "Error processing webhook",
                    "event_type": event.type,
                    "error": str(e),
                }
            )
            # No lanzamos el error, solo lo registramos
            return {"status": "error", "message": f"Error processing webhook: {str(e)}"}

    async def _process_webhook(
        self, event: stripe.Event, background_tasks: BackgroundTasks
    ) -> dict:
        """Procesa el webhook verificado"""
        logger.info(
            {
                "message": "Processing webhook",
                "event_id": event.id,
                "event_type": event.type,
            }
        )

        background_tasks.add_task(self.process_webhook_async, event)

        return {
            "status": "accepted",
            "event_id": event.id,
            "message": f"Webhook accepted: {event.id}",
        }

    @staticmethod
    def _handle_webhook_error(error: Exception) -> None:
        """Maneja errores de webhook de manera centralizada"""
        logger.error(
            {
                "message": "Webhook processing failed",
                "error": str(error),
                "error_type": type(error).__name__,
            }
        )
        raise WebhookError(str(error))

    async def handle_checkout_completed(
        self, event: StripeWebhookEvent
    ) -> Dict[str, Any]:
        """Maneja eventos de checkout completado con reintentos"""
        max_retries = 3
        base_delay = 2  # segundos

        for attempt in range(max_retries):
            try:
                session = event.data.object
                customer_details = session.get("customer_details", {})

                await process_successful_checkout(
                    customer_email=customer_details.get("email"),
                    subscription_id=session.get("subscription"),
                )

                logger.info(
                    {
                        "message": "Checkout processed successfully",
                        "event_id": event.id,
                        "customer_email": customer_details.get("email"),
                    }
                )

                return {
                    "status": "success",
                    "message": f"Checkout completed for {customer_details.get('email')}",
                }

            except Exception as e:
                delay = base_delay * (2**attempt)  # Exponential backoff
                if attempt == max_retries - 1:  # Último intento
                    logger.error(
                        {
                            "message": "Max retries reached for checkout processing",
                            "error": str(e),
                            "event_id": event.id,
                            "attempts": max_retries,
                        }
                    )
                    raise PaymentError(f"Failed to process checkout: {str(e)}")

                logger.warning(
                    {
                        "message": f"Retry {attempt + 1}/{max_retries} for checkout processing",
                        "event_id": event.id,
                        "next_retry_in": f"{delay}s",
                    }
                )
                await asyncio.sleep(delay)

    async def handle_subscription_created(
        self, event: StripeWebhookEvent
    ) -> Dict[str, Any]:
        """Maneja eventos de suscripción creada"""
        try:
            subscription = event.data.object
            customer_id = subscription.get("customer")
            subscription_id = subscription.get("id")

            # Aquí deberías actualizar tu base de datos con la nueva suscripción
            # await update_user_subscription(customer_id, subscription_id)

            return {
                "status": "success",
                "message": f"Subscription created: {subscription_id}",
                "customer_id": customer_id,
            }
        except Exception as e:
            logger.error(
                {
                    "message": "Error processing subscription creation",
                    "error": str(e),
                    "event_id": event.id,
                }
            )
            raise PaymentError(f"Failed to process subscription creation: {str(e)}")

    async def handle_subscription_updated(
        self, event: StripeWebhookEvent
    ) -> Dict[str, Any]:
        """Maneja eventos de suscripción actualizada"""
        # Implementar lógica específica
        pass

    async def handle_subscription_deleted(
        self, event: StripeWebhookEvent
    ) -> Dict[str, Any]:
        """Maneja eventos de suscripción eliminada"""
        try:
            subscription = event.data.object
            customer_id = subscription.get("customer")

            # Aquí deberías actualizar tu base de datos para marcar la suscripción como cancelada
            # await cancel_user_subscription(customer_id)

            return {
                "status": "success",
                "message": f"Subscription cancelled for customer: {customer_id}",
            }
        except Exception as e:
            logger.error(
                {
                    "message": "Error processing subscription cancellation",
                    "error": str(e),
                    "event_id": event.id,
                }
            )
            raise PaymentError(f"Failed to process subscription cancellation: {str(e)}")

    async def handle_invoice_paid(self, event: StripeWebhookEvent) -> Dict[str, Any]:
        """Maneja eventos de factura pagada"""
        # Implementar lógica específica
        pass

    async def handle_payment_failed(self, event: StripeWebhookEvent) -> Dict[str, Any]:
        """Maneja eventos de pago fallido"""
        try:
            invoice = event.data.object
            customer_id = invoice.get("customer")
            attempt_count = invoice.get("attempt_count", 1)

            # Aquí podrías notificar al usuario sobre el fallo del pago
            # await notify_payment_failure(customer_id, attempt_count)

            return {
                "status": "processed",
                "message": f"Payment failed for customer: {customer_id}, attempt: {attempt_count}",
            }
        except Exception as e:
            logger.error(
                {
                    "message": "Error processing payment failure",
                    "error": str(e),
                    "event_id": event.id,
                }
            )
            return {
                "status": "error",
                "message": f"Error processing payment failure: {str(e)}",
            }
