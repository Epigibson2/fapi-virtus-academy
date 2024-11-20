from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status,
    BackgroundTasks,
    Depends,
)
from core.config import settings
from schemas.stripe_schemas import (
    WebhookResponse,
    ProductCreate,
    ProductResponse,
    SubscriptionCreate,
    SubscriptionResponse,
)
from services.stripe.stripe_services import StripeServices
from utils.exceptions import StripeError, WebhookError
from utils.logger import logger
from typing import List


stripe_router = APIRouter()


@stripe_router.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    """
    Crea una sesión de checkout general.

    Args:
        request (Request): Objeto Request de FastAPI con los datos necesarios.

    Returns:
        dict: URL de la sesión de checkout.

    Raises:
        HTTPException: Si hay un error al crear la sesión.
    """
    try:
        stripe_service = StripeServices()
        checkout_url = await stripe_service.create_checkout_session(request)
        return {"url": checkout_url}
    except Exception as e:
        logger.error({"message": "Error creating checkout session", "error": str(e)})
        raise HTTPException(status_code=400, detail=str(e))


@stripe_router.post("/webhook", response_model=WebhookResponse)
async def webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    stripe_service: StripeServices = Depends(),
):
    """
    Endpoint para recibir webhooks de Stripe.

    Args:
        request (Request): Objeto Request con los datos del webhook.
        background_tasks (BackgroundTasks): Objeto para procesar tareas en segundo plano.
        stripe_service (StripeServices): Servicio de Stripe inyectado.

    Returns:
        WebhookResponse: Respuesta confirmando la recepción del webhook.

    Raises:
        HTTPException: Si hay un error en la verificación o procesamiento del webhook.
    """
    try:
        result = await stripe_service.webhook_received(request, background_tasks)
        return WebhookResponse(
            status=result["status"],
            event_id=result["event_id"],
            message=result["message"],
        )
    except WebhookError as e:
        logger.error({"message": "Webhook error in handler", "error": str(e)})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@stripe_router.get("/webhook-config")
async def get_webhook_config():
    """
    Verifica la configuración actual del webhook.

    Returns:
        dict: Estado de la configuración del webhook incluyendo:
            - webhook_secret_configured (bool): Si el secret está configurado
            - webhook_secret_length (int): Longitud del secret
            - webhook_secret_prefix (str): Primeros caracteres del secret
    """
    return {
        "webhook_secret_configured": bool(settings.STRIPE_WEBHOOK_SECRET),
        "webhook_secret_length": (
            len(settings.STRIPE_WEBHOOK_SECRET) if settings.STRIPE_WEBHOOK_SECRET else 0
        ),
        "webhook_secret_prefix": (
            settings.STRIPE_WEBHOOK_SECRET[:4] + "..."
            if settings.STRIPE_WEBHOOK_SECRET
            else None
        ),
    }


@stripe_router.post("/products", response_model=ProductResponse)
async def create_product(
    product: ProductCreate, stripe_service: StripeServices = Depends()
):
    """
    Crea un nuevo producto con su precio asociado.

    Args:
        product (ProductCreate): Datos del producto a crear.
        stripe_service (StripeServices): Servicio de Stripe inyectado.

    Returns:
        ProductResponse: Datos del producto creado.

    Raises:
        HTTPException: Si hay un error al crear el producto.
    """
    return await stripe_service.create_product(product)


@stripe_router.get("/products", response_model=List[ProductResponse])
async def list_products(stripe_service: StripeServices = Depends()):
    """
    Lista todos los productos activos.

    Args:
        stripe_service (StripeServices): Servicio de Stripe inyectado.

    Returns:
        List[ProductResponse]: Lista de productos con sus precios.

    Raises:
        HTTPException: Si hay un error al obtener los productos.
    """
    return await stripe_service.list_products()


@stripe_router.post("/subscriptions", response_model=list[SubscriptionResponse])
async def create_subscription(
    subscription: SubscriptionCreate, stripe_service: StripeServices = Depends()
):
    """
    Crea una nueva suscripción.

    Args:
        subscription (SubscriptionCreate): Datos de la suscripción a crear.
        stripe_service (StripeServices): Servicio de Stripe inyectado.

    Returns:
        list[SubscriptionResponse]: Lista con la suscripción creada.

    Raises:
        HTTPException: Si hay un error al crear la suscripción.
    """
    return await stripe_service.create_subscription(subscription)


@stripe_router.get("/subscriptions", response_model=list[SubscriptionResponse])
async def get_subscriptions(stripe_service: StripeServices = Depends()):
    """
    Lista todas las suscripciones activas.

    Args:
        stripe_service (StripeServices): Servicio de Stripe inyectado.

    Returns:
        list[SubscriptionResponse]: Lista de suscripciones activas.

    Raises:
        HTTPException: Si hay un error al obtener las suscripciones.
    """
    return await stripe_service.get_subscriptions()


@stripe_router.get("/subscriptions/search")
async def search_subscription(
    status: str, order_id: str, stripe_service: StripeServices = Depends()
):
    """
    Busca una suscripción por estado y ID de pedido.

    Args:
        status (str): Estado de la suscripción.
        order_id (str): ID del pedido.
        stripe_service (StripeServices): Servicio de Stripe inyectado.

    Returns:
        dict: Detalles de la suscripción encontrada.

    Raises:
        HTTPException: Si hay un error al buscar la suscripción.
    """
    return await stripe_service.search_subscriptions(status, order_id)


@stripe_router.delete("/subscriptions/{subscription_id}")
async def cancel_subscription(
    subscription_id: str, stripe_service: StripeServices = Depends()
):
    """
    Cancela una suscripción.

    Args:
        subscription_id (str): ID de la suscripción a cancelar.
        stripe_service (StripeServices): Servicio de Stripe inyectado.

    Returns:
        dict: Detalles de la suscripción cancelada.

    Raises:
        HTTPException: Si hay un error al cancelar la suscripción.
    """
    return await stripe_service.cancel_subscription(subscription_id)


@stripe_router.post("/resume-subscription/{subscription_id}")
async def resume_subscription(
    subscription_id: str, stripe_service: StripeServices = Depends()
):
    """
    Reanuda una suscripción.

    Args:
        subscription_id (str): ID de la suscripción a reanudar.
        stripe_service (StripeServices): Servicio de Stripe inyectado.

    Returns:
        dict: Detalles de la suscripción reanudada.

    Raises:
        HTTPException: Si hay un error al reanudar la suscripción.
    """
    return await stripe_service.resume_subscription(subscription_id)


@stripe_router.post("/create-checkout-session/{price_id}")
async def create_checkout_session(
    price_id: str, stripe_service: StripeServices = Depends()
):
    """
    Crea una sesión de checkout para un precio específico.

    Args:
        price_id (str): ID del precio en Stripe.
        stripe_service (StripeServices): Servicio de Stripe inyectado.

    Returns:
        dict: URL de la sesión de checkout.

    Raises:
        HTTPException: Si hay un error al crear la sesión.
    """
    return await stripe_service.create_checkout_session(price_id)
