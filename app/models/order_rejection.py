from typing import Optional
import datetime
import uuid
import json

from app.models.counterparty import Customer

from app.tools.dt_helper import datetime_obj2z_string


class OrderRejection:
    def __init__(self,
                 customer: Customer,
                 order_id: uuid.UUID,
                 rejection_message: str,
                 request_body: str,
                 timestamp: datetime.datetime,
                 error_message: Optional[str] = None):
        self.customer = customer
        self.order_id = str(order_id)
        self.rejection_message = rejection_message
        self.request_body = json.dumps(request_body)
        self.timestamp = timestamp if isinstance(timestamp, str) else datetime_obj2z_string(timestamp)
        self.error = error_message
