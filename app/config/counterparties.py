from app.config.customers import customers
from app.models.counterparty import Counterparty


counterparties = [
    Counterparty(is_customer=False,
                 identifier="AMM"),
    *[Counterparty(is_customer=True,
                   identifier=customer.customer_name,
                   customer=customer) for customer in customers]
]

counterparties_dict = {counterparty.identifier: counterparty for counterparty in counterparties}