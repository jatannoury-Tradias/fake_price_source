from typing import Union

from app.config.constants import PRICE_UPDATE_TIME
from app.config.instruments import instruments_dict
from app.controllers.responses.prices.broadcast_price_updates import broadcast_price_updates


async def  send_prices(websocket,
                      price_request: dict[str, Union[str, list]]) -> None:
    """
    Maps the request and send a continuous pricestream to the websocket.

    Args:
        websocket: The websocket through which the price updates should be sent
        price_request: request message as a dict

    Returns: None
    """
    instrument = instruments_dict[price_request["instrument"]]
    levels = price_request["levels"]
    sleep_time = PRICE_UPDATE_TIME
    await broadcast_price_updates(websocket, instrument, levels, sleep_time)
