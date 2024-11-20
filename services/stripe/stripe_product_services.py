from utils.logger import logger
from typing import List
from schemas.stripe_schemas import ProductCreate, ProductResponse
import stripe
from fastapi import HTTPException


class StripeProductServices:
    def __init__(self):
        self.stripe = stripe

    async def create_product(self, product: ProductCreate) -> ProductResponse:
        """
        Crea un nuevo producto en Stripe con su precio asociado.

        Args:
            product (ProductCreate): Datos del producto a crear incluyendo nombre, descripción y precio.

        Returns:
            ProductResponse: Datos del producto creado incluyendo IDs de Stripe.

        Raises:
            HTTPException: Si hay un error al crear el producto en Stripe.
        """
        try:
            # Crear el producto
            stripe_product = stripe.Product.create(
                name=product.name,
                description=product.description,
                active=True,
            )

            # Crear el precio
            price = stripe.Price.create(
                product=stripe_product.id,
                unit_amount=int(product.price * 100),  # Convertir a centavos
                currency=product.currency,
                recurring={"interval": product.interval},
            )

            return ProductResponse(
                id=stripe_product.id,
                name=product.name,
                description=product.description,
                price_id=price.id,
                price=product.price,
                interval=product.interval,
                currency=product.currency,
                active=True,
            )

        except stripe.error.StripeError as e:
            logger.error({"message": "Error creating product", "error": str(e)})
            raise HTTPException(status_code=400, detail=str(e))

    async def list_products(self) -> List[ProductResponse]:
        """
        Obtiene la lista de todos los productos activos en Stripe.

        Returns:
            List[ProductResponse]: Lista de productos con sus precios asociados.

        Raises:
            HTTPException: Si hay un error al obtener los productos de Stripe.
        """
        try:
            products = stripe.Product.list(active=True)
            prices = stripe.Price.list(active=True)

            # Crear un diccionario de precios por producto
            price_map = {price.product: price for price in prices.data}

            return [
                ProductResponse(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    price_id=price_map[product.id].id,
                    price=price_map[product.id].unit_amount / 100,
                    interval=price_map[product.id].recurring.interval,
                    currency=price_map[product.id].currency,
                    active=product.active,
                )
                for product in products.data
                if product.id in price_map
            ]

        except stripe.error.StripeError as e:
            logger.error({"message": "Error listing products", "error": str(e)})
            raise HTTPException(status_code=400, detail=str(e))
