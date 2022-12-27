import datetime

from app.tools.dt_helper import datetime_obj2z_string

from app.models.instrument import Instrument
from app.models.price_update.price_update import PriceUpdate
from app.models.price_update.price_level import PriceLevel

from app.config.pricing_engines import pricing_engines_dict


def get_price(instrument: Instrument,
              side: str,
              quantity: float) -> float:
    pricing_engine = pricing_engines_dict[instrument.instrument_code]
    return pricing_engine.get_price_currency_1_in_currency_2(side, quantity)


def get_price_update(instrument: Instrument,
                     buy_quantities: list[float],
                     sell_quantities: list[float]) -> PriceUpdate:
    buy_levels = [PriceLevel(quantity=buy_quantity,
                             price=get_price(instrument, "buy", buy_quantity)) for buy_quantity in buy_quantities]
    sell_levels = [PriceLevel(quantity=sell_quantity,
                              price=get_price(instrument, "sell", sell_quantity)) for sell_quantity in sell_quantities]
    price_update = PriceUpdate(instrument=instrument,
                               buy_levels=buy_levels,
                               sell_levels=sell_levels,
                               timestamp=datetime.datetime.utcnow())
    return price_update


def price_update_message(price_update: PriceUpdate) -> dict:
    levels = {
        "buy": [{"quantity": level.quantity,
                 "price": level.price} for level in price_update.buy_levels],
        "sell": [{"quantity": level.quantity,
                  "price": level.price} for level in price_update.sell_levels]
    }
    message = {
        "event": "prices",
        "success": True,
        "instrument": price_update.instrument.instrument_code,
        "levels": levels,
        "timestamp": datetime_obj2z_string(price_update.timestamp)
    }
    return message
