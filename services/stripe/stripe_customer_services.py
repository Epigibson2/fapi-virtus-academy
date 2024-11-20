import stripe


class StripeCustomerServices:
    def __init__(self):
        self.stripe = stripe

    def create_customer(self, email: str, payment_method_id: str = None):
        try:
            customer_data = {
                "email": email,
            }
            if payment_method_id:
                customer_data["payment_method"] = payment_method_id

            customer = self.stripe.Customer.create(**customer_data)
            return customer
        except Exception as e:
            raise e
