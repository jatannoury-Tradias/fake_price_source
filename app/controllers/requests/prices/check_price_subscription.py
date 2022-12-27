from app.config.pricing_engines import pricing_engines_dict
from app.models.exceptions.exceptions import *

from app.tools.assert_raise import assert_raise


available_instruments = list(pricing_engines_dict.keys())


def is_valid_price_subscription(request_body: dict) -> bool:
    """
    Checks the validity of a price stream request and raises an exceptions, if errors occur.
    Args:
        request_body: The body send by the customer in the request as a dicty

    Returns: True, if no errors were found

    """
    assert_raise(all(["type" in request_body.keys(),
                      "channelname" in request_body.keys(),
                      "instrument" in request_body.keys(),
                      "levels" in request_body.keys()]),
                 PriceRequestFormatError("Price subscription must contain type, channelname and instrument fields."))

    request_type = request_body["type"]
    assert_raise(isinstance(request_type, str),
                 PriceRequestFormatError(f"type: Expected str, got {type(request_type)} instead."))
    assert_raise(request_type == "subscribe",
                 PriceRequestValueError("Invalid request type."))

    request_channelname = request_body["channelname"]
    assert_raise(isinstance(request_channelname, str),
                 PriceRequestFormatError(f"channelname: Expected str, got {type(request_channelname)} instead."))
    assert_raise(request_channelname == "prices",
                 PriceRequestValueError("Invalid channelname"))

    request_instrument = request_body["instrument"]
    assert_raise(isinstance(request_instrument, str),
                 PriceRequestFormatError(f"instrument: Expected str, got {type(request_instrument)} instead."))
    assert_raise(request_instrument in available_instruments,
                 InstrumentNotPriceableError(f"Instrument cannot be priced: {request_instrument}"))

    request_levels = request_body["levels"]
    assert_raise(isinstance(request_levels, list) and all([isinstance(level, float) or isinstance(level, int) for level in request_levels]),
                 PriceRequestFormatError(f"instrument: Expected list[Union[float,int]], got {type(request_levels)} instead."))
    assert_raise(all([level > 0 for level in request_levels]),
                 InvalidLevelsError("Levels have to be positive."))
    return True
