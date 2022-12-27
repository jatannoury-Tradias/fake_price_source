import datetime

from app.models.instrument import Instrument
from app.models.price_update.price_level import PriceLevel


class PriceUpdate:
    def __init__(self,
                 instrument: Instrument,
                 buy_levels: list[PriceLevel],
                 sell_levels: list[PriceLevel],
                 timestamp: datetime.datetime):
        self.instrument = instrument
        self.buy_levels = buy_levels
        self.sell_levels = sell_levels
        self.timestamp = timestamp
