from fastapi import HTTPException, status


class StripeError(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class WebhookError(StripeError):
    pass


class SubscriptionError(StripeError):
    pass


class PaymentError(StripeError):
    pass
