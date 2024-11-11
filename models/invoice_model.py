from beanie import Document, Link
from pydantic import Field
from datetime import datetime
from models.files_model import File
from models.payment_model import Payment
from models.user_model import User


class Invoice(Document):
    owner: Link[User] = Field()
    file: Link[File] = Field()
    amount: float = Field()
    status: str = Field()
    due_date: datetime = Field()
    paid_date: datetime = Field()
    payment: Link[Payment] = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    class Settings:
        name = "invoices"
        use_state_management = True


# RECIBO
# PAGO, SI EL PAGO SE REALIZA, GENERA UN COMPROBANTE DE PAGO (TICKET)
# COMPROBANTE DE PAGO
