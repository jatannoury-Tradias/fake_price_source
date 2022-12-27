import uuid
import datetime

from typing import Optional
from decimal import Decimal

from app.models.counterparty import Counterparty
from app.models.instrument import Instrument
from app.models.currency import Currency

from app.tools.dt_helper import datetime_obj2z_string

class Order:
    def __init__(self,
                 order_id: uuid.UUID,
                 created_at: datetime.datetime,
                 created_by: Counterparty,
                 accepted_by: Counterparty,
                 communication_channel: str,
                 order_status: str,
                 order_instrument: Instrument,
                 order_type: str,
                 order_side: str,
                 amount: float,
                 amount_currency: Currency,
                 request_body: str,
                 response_body: str,
                 client_order_id: Optional[str] = None):
        self.order_id = str(order_id)
        self.created_at = datetime_obj2z_string(created_at)
        self.created_by = created_by
        self.accepted_by = accepted_by
        self.communication_channel = communication_channel
        self.order_status = order_status
        self.order_instrument = order_instrument
        self.order_type = order_type
        self.order_side = order_side
        self.amount = Decimal(str(amount))
        self.amount_currency = amount_currency
        self.request_body = request_body
        self.response_body = response_body
        self.client_order_id = client_order_id
