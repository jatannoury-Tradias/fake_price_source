import uuid
import datetime

from typing import Optional
from decimal import Decimal

from app.models.trading.order import Order
from app.models.counterparty import Counterparty
from app.models.instrument import Instrument
from app.models.currency import Currency

from app.tools.dt_helper import datetime_obj2z_string

class Trade:
    def __init__(self,
                 order: Order,
                 trade_id: uuid.UUID,
                 executed_at: datetime.datetime,
                 instrument: Instrument,
                 leg_1_amount: float,
                 leg_1_currency: Currency,
                 leg_1_recipient: Counterparty,
                 leg_2_amount: float,
                 leg_2_currency: Currency,
                 leg_2_recipient: Counterparty,
                 fees: float,
                 fees_currency: Optional[Currency],
                 fee_payer: Optional[Counterparty],
                 price: float,
                 prices_at_execution: Optional[str],
                 settlement_details: Optional[dict]):
        self.order = order
        self.trade_id = str(trade_id)
        self.executed_at = datetime_obj2z_string(executed_at)
        self.instrument = instrument
        self.leg_1_amount = Decimal(str(leg_1_amount))
        self.leg_1_currency = leg_1_currency
        self.leg_1_recipient = leg_1_recipient
        self.leg_2_amount = Decimal(str(leg_2_amount))
        self.leg_2_currency = leg_2_currency
        self.leg_2_recipient = leg_2_recipient
        self.fees = Decimal(fees)
        self.fees_currency = fees_currency
        self.fee_payer = fee_payer
        self.price = Decimal(str(price))
        self.prices_at_execution = prices_at_execution
        self.settlement_details = settlement_details
