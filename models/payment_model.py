from datetime import datetime

from beanie import Document, Link
from pydantic import Field
from models.user_model import User


class Payment(Document):
    subtotal: float = Field()
    discount: float = Field()
    total: float = Field()
    status: str = Field()
    payment_method: str = Field()
    service: str = Field()
    concept: str = Field()
    person_type: str = Field()
    owner: Link[User] = Field()
    paid_date: datetime = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Settings:
        name = "payments"
        use_state_management = True
