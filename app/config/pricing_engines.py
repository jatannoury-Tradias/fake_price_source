from app.config.instruments import instruments_dict

from app.models.pricing_engine.pricing_engine import PricingEngine

pricing_engines = [
    PricingEngine(instrument=instruments_dict["TKN-EUR"],
                  pool_amount_leg_1_currency=100,
                  pool_amount_leg_2_currency=100)
]

pricing_engines_dict = {pricing_engine.instrument.instrument_code: pricing_engine for pricing_engine in pricing_engines}
