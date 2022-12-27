from decimal import Decimal

# from app.config.database import pools_table
from app.models.instrument import Instrument


class PricingEngine:
    def __init__(self,
                 instrument: Instrument,
                 pool_amount_leg_1_currency: float,
                 pool_amount_leg_2_currency: float):
        self.instrument = instrument
        self.currency_leg_1 = self.instrument.currency_leg_1
        self.currency_leg_2 = self.instrument.currency_leg_2
        self.pool_amount_leg_1_currency = pool_amount_leg_1_currency
        self.pool_amount_leg_2_currency = pool_amount_leg_2_currency
        self.internal_product = None
        self._update_internal_product()

        # create an entry in the database, if the instrument is not yet present.


    def _update_internal_product(self):
        self.internal_product = self.pool_amount_leg_1_currency * self.pool_amount_leg_2_currency

    def _update_currency_1_amount(self, delta_currency_1):
        self.pool_amount_leg_1_currency += delta_currency_1

    def _update_currency_2_amount(self, delta_currency_2):
        self.pool_amount_leg_2_currency += delta_currency_2


    def get_price_currency_1_in_currency_2(self, customer_side, currency_1_amount):
        self._get_pool_numbers_from_db()
        if customer_side == "sell":
            price_per_unit = (self.pool_amount_leg_2_currency / (self.pool_amount_leg_1_currency + currency_1_amount))
            return float(price_per_unit)
        elif customer_side == "buy":
            price_per_unit = (self.pool_amount_leg_2_currency / (self.pool_amount_leg_1_currency - currency_1_amount))
            return float(price_per_unit)

    def trade_currency_1_for_currency_2(self, currency_1_amount, customer_side):
        if customer_side == "buy":
            self._get_pool_numbers_from_db()
            currency_2_amount = self.pool_amount_leg_2_currency * (1 / ((self.pool_amount_leg_1_currency / currency_1_amount) - 1))
            self._update_currency_1_amount(-currency_1_amount)
            self._update_currency_2_amount(currency_2_amount)
            self._update_pool_numbers_in_db()
            return float(currency_2_amount)
        elif customer_side == "sell":
            self._get_pool_numbers_from_db()
            currency_2_amount = self.pool_amount_leg_2_currency * (1 / ((self.pool_amount_leg_1_currency / currency_1_amount) + 1))
            self._update_currency_1_amount(currency_1_amount)
            self._update_currency_2_amount(-currency_2_amount)
            self._update_pool_numbers_in_db()
            return float(currency_2_amount)

    def mid_price(self):
        return self.pool_amount_leg_2_currency/self.pool_amount_leg_1_currency