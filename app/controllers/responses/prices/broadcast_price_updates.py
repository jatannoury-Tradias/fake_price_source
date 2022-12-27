import asyncio
import json

from app.models.instrument import Instrument

from app.controllers.responses.prices.get_price_updates import get_price_update, price_update_message


def level_is_available(instrument: Instrument,
                       quantity: float,
                       side: str):
    ## TODO: check level availability
    return True


async def broadcast_price_updates(websocket,
                                  instrument: Instrument,
                                  levels: list[float],
                                  sleep_time: float):
    """
    Continuously send price updates through the websocket

    Args:
        websocket: The websocket through which the customer connects
        instrument: The instrument of the requested prices
        levels: The levels of the requested prices as a list
        sleep_time: The sleep time between price updates

    Returns: None

    """
    while True:
        buy_quantities = [quantity for quantity in levels if level_is_available(instrument, quantity, "buy")]
        sell_quantities = [quantity for quantity in levels if level_is_available(instrument, quantity, "sell")]
        price_update = get_price_update(instrument, buy_quantities, sell_quantities)
        response = price_update_message(price_update)
        await websocket.send(json.dumps(response))
        await asyncio.sleep(sleep_time)
