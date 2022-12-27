from app.models.currency import Currency


class Instrument:
    def __init__(self,
                 currency_leg_1: Currency,
                 currency_leg_2: Currency,
                 instrument_precision: int):
        self.currency_leg_1 = currency_leg_1
        self.currency_leg_2 = currency_leg_2
        self.instrument_precision = instrument_precision
        self.instrument_code = currency_leg_1.currency_code + "-" + currency_leg_2.currency_code
