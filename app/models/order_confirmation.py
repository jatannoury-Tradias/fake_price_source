import datetime
import uuid

from app.models.counterparty import Counterparty
from app.models.instrument import Instrument


class OrderConfirmation:
    def __init__(self,
                 customer: Counterparty,
                 order_id: uuid.UUID,
                 trade_id: uuid.UUID,
                 order_side: str,
                 order_amount: float,
                 order_instrument: Instrument,
                 confirmed_price: float,
                 total_amount: float,
                 executed_at: datetime.datetime,
                 client_order_id: str):
        self.customer = customer
        self.order_id = order_id
        self.trade_id = trade_id
        self.order_side = order_side
        self.order_amount = float(order_amount)
        self.order_instrument = order_instrument
        self.confirmed_price = float(confirmed_price)
        self.total_amount = float(total_amount)
        self.executed_at = executed_at
        self.client_order_id = client_order_id
