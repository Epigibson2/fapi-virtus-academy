from beanie import Document, Link
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PaymentPlanType(str, Enum):
    SINGLE = "single"  # Pago único
    INSTALLMENTS = "installments"  # Parcialidades
    MSI = "msi"  # Meses sin intereses


class InstallmentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    FAILED = "failed"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethod(str, Enum):
    CARD = "card"
    OXXO = "oxxo"
    SPEI = "spei"


class Customer(Document):
    name: str
    email: str
    stripe_customer_id: str
    payment_methods: List[Link["CustomerPaymentMethod"]]
    created_at: datetime = datetime.now(datetime.UTC)
    updated_at: datetime = datetime.now(datetime.UTC)

    class Settings:
        name = "customers"


class CustomerPaymentMethod(Document):
    customer: Link[Customer]
    stripe_payment_method_id: str
    payment_type: PaymentMethod
    last_four: str  # últimos 4 dígitos de la tarjeta
    brand: str  # visa, mastercard, etc.
    is_default: bool = False
    created_at: datetime = datetime.now(datetime.UTC)

    class Settings:
        name = "customer_payment_methods"


class Invoice(Document):
    amount: float
    currency: str = "MXN"
    description: str
    customer: Link["Customer"]
    status: str
    due_date: datetime
    payment_plan: Link["PaymentPlan"]
    payments: List[Link["Payment"]]
    created_at: datetime = datetime.now(datetime.UTC)
    updated_at: datetime = datetime.now(datetime.UTC)

    class Settings:
        name = "invoices"


class PaymentPlan(Document):
    invoice: Link[Invoice]
    plan_type: PaymentPlanType
    total_amount: float
    number_of_installments: int  # número total de pagos
    installment_amount: float  # monto de cada pago
    interest_rate: float = 0.0  # tasa de interés (0 para MSI)
    installments: List[Link["Installment"]]
    start_date: datetime
    created_at: datetime = datetime.now(datetime.UTC)

    class Settings:
        name = "payment_plans"


class Installment(Document):
    payment_plan: Link[PaymentPlan]
    installment_number: int  # número de pago (1, 2, 3...)
    amount: float
    due_date: datetime
    status: InstallmentStatus
    payment: Optional[Link["Payment"]]  # el pago asociado cuando se realice
    created_at: datetime = datetime.now(datetime.UTC)

    class Settings:
        name = "installments"


class Payment(Document):
    invoice: Link[Invoice]
    installment: Optional[Link[Installment]]  # para pagos en parcialidades
    amount: float
    currency: str = "MXN"
    status: PaymentStatus
    payment_method: PaymentMethod
    stripe_payment_intent_id: str
    stripe_payment_method_id: Optional[str]
    stripe_charge_id: Optional[str]
    payment_voucher: Optional[Link["PaymentVoucher"]]
    metadata: dict
    created_at: datetime = datetime.now(datetime.UTC)
    updated_at: datetime = datetime.now(datetime.UTC)

    class Settings:
        name = "payments"


class PaymentVoucher(Document):
    payment: Link[Payment]
    voucher_number: str
    stripe_receipt_url: str
    stripe_receipt_number: str
    generated_date: datetime = datetime.now(datetime.UTC)

    class Settings:
        name = "payment_vouchers"
