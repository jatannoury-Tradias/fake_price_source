from typing import Optional
from app.models.customer import Customer


class Counterparty:
    def __init__(self,
                 is_customer: bool,
                 identifier: str,
                 customer: Optional[Customer] = None):
        self.is_customer = is_customer
        self.identifier = identifier
        self.customer = customer
