from utils.logger import logger
from utils.exceptions import PaymentError
from typing import List
from schemas.stripe_schemas import SubscriptionCreate, SubscriptionResponse
import stripe
from fastapi import HTTPException


class StripeSubscriptionServices:
    def __init__(self):
        self.stripe = stripe

    async def create_subscription(
        self, subscription: SubscriptionCreate
    ) -> SubscriptionResponse:
        try:
            subscription = await self.stripe.Subscription.create(
                customer=subscription.customer_id,
                items=[{"price": subscription.price_id}],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
            )
            return subscription
        except stripe.error.StripeError as e:
            logger.error({"message": "Error creating subscription", "error": str(e)})
            raise HTTPException(status_code=400, detail=str(e))

    async def get_subscriptions(self) -> List[SubscriptionResponse]:
        """
        Obtiene todas las suscripciones activas.

        Returns:
            List[SubscriptionResponse]: Lista de suscripciones activas con detalles del cliente y producto.

        Raises:
            HTTPException: Si hay un error al obtener las suscripciones de Stripe.
        """
        try:
            # Obtener suscripciones con expansión limitada
            subscriptions_list = self.stripe.Subscription.list(
                status="active", expand=["data.customer", "data.items.data.price"]
            )

            subscription_responses = []
            for sub in subscriptions_list.data:
                try:
                    # Obtener el primer item de la suscripción
                    item = sub.items.data[0] if sub.items.data else None
                    if not item:
                        continue

                    # Obtener el producto separadamente si es necesario
                    product = None
                    if item and item.price and item.price.product:
                        product = self.stripe.Product.retrieve(item.price.product)

                    subscription_responses.append(
                        SubscriptionResponse(
                            id=sub.id,
                            status=sub.status,
                            customer_id=sub.customer.id if sub.customer else "N/A",
                            customer_email=(
                                sub.customer.email if sub.customer else "N/A"
                            ),
                            product_name=product.name if product else "N/A",
                            price_amount=(
                                item.price.unit_amount / 100 if item.price else 0
                            ),
                            currency=item.price.currency if item.price else "usd",
                            interval=(
                                item.price.recurring.interval
                                if item.price and item.price.recurring
                                else "month"
                            ),
                            current_period_end=sub.current_period_end,
                            cancel_at_period_end=sub.cancel_at_period_end,
                        )
                    )

                    logger.info(
                        {
                            "message": "Subscription processed",
                            "subscription_id": sub.id,
                            "customer_email": (
                                sub.customer.email if sub.customer else "N/A"
                            ),
                        }
                    )

                except Exception as e:
                    logger.error(
                        {
                            "message": "Error processing subscription",
                            "subscription_id": sub.id,
                            "error": str(e),
                        }
                    )
                    continue

            logger.info(
                {
                    "message": "Subscriptions retrieved successfully",
                    "count": len(subscription_responses),
                }
            )

            return subscription_responses

        except stripe.error.StripeError as e:
            logger.error({"message": "Error retrieving subscriptions", "error": str(e)})
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error({"message": "Unexpected error", "error": str(e)})
            raise HTTPException(status_code=500, detail="Error interno del servidor")

    async def cancel_subscription(self, subscription_id: str) -> dict:
        """
        Cancela una suscripción

        Args:
            subscription_id (str): ID de la suscripción a cancelar.

        Returns:
            dict: Detalles de la suscripción cancelada.
        """
        try:
            subscription = await self.stripe.Subscription.delete(subscription_id)
            return subscription
        except stripe.error.StripeError as e:
            logger.error({"message": "Error canceling subscription", "error": str(e)})
            raise PaymentError(str(e))

    async def resume_subscription(self, subscription_id: str) -> dict:
        """
        Reanuda una suscripción

        Args:
            subscription_id (str): ID de la suscripción a reanudar.

        Returns:
            dict: Detalles de la suscripción reanudada.

        Raises:
            PaymentError: Si hay un error al reanudar la suscripción.
        """
        try:
            subscription = await self.stripe.Subscription.resume(
                subscription_id, billing_cycle_anchor="now"
            )
            return subscription
        except stripe.error.StripeError as e:
            logger.error({"message": "Error resuming subscription", "error": str(e)})
            raise PaymentError(str(e))

    async def search_subscriptions(self, status: str, order_id: str) -> dict:
        """
        Busca una suscripción por ID

        Args:
            status (str): Estado de la suscripción.
            order_id (str): ID del pedido.

        Returns:
            dict: Detalles de la suscripción encontrada.
        """
        try:
            subscription = await self.stripe.Subscription.search(
                query=f"status:'{status}' AND metadata['order_id']:'{order_id}'"
            )
            return subscription
        except stripe.error.StripeError as e:
            logger.error({"message": "Error searching subscription", "error": str(e)})
            raise PaymentError(str(e))
