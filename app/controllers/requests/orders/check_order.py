from app.tools.assert_raise import assert_raise

from app.models.exceptions.exceptions import *
from app.config.pricing_engines import pricing_engines_dict


valid_instruments = list(pricing_engines_dict.keys())
valid_order_types = ["market"]
valid_order_sides = ["buy", "sell"]


def is_valid_order(request_body: dict) -> bool:
    """
    Checks the validity of an order and creates Error objects, if errors occur.
    Args:
        request_body: The body send by the customer in the request as a dict

    Returns: True, if no errors were found

    """
    assert_raise("order" in request_body.keys(),
                 OrderFormatError("No order wrapper found in request"))
    assert_raise(all(["instrument" in request_body["order"].keys(),
                      "order_type" in request_body["order"].keys(),
                      "side" in request_body["order"].keys(),
                      "amount" in request_body["order"].keys()]),
                 OrderFormatError("instrument, order_type, side and amount fields must be provided."))

    request_instrument = request_body["order"]["instrument"]
    assert_raise(isinstance(request_instrument, str),
                 InvalidDatatypeError(f"Expected str, got {type(request_instrument)} instead."))
    assert_raise(request_instrument.upper() in valid_instruments,
                 InstrumentNotFoundError(request_instrument))

    request_order_type = request_body["order"]["order_type"]
    assert_raise(isinstance(request_order_type, str),
                 InvalidDatatypeError(f"Expected str, got {type(request_order_type)} instead."))
    assert_raise(request_order_type.lower() in valid_order_types,
                 InvalidOrderTypeError(request_order_type))

    request_order_side = request_body["order"]["side"]
    assert_raise(isinstance(request_order_side, str),
                 InvalidDatatypeError(f"Expected str, got {type(request_order_side)} instead."))
    assert_raise(request_order_side.lower() in valid_order_sides,
                 InvalidOrderSideError(request_order_side))

    request_order_amount = request_body["order"]["amount"]
    assert_raise(isinstance(request_order_amount, float) or isinstance(request_order_amount, int),
                 InvalidDatatypeError(f"Expected number, got {type(request_order_side)} instead."))

    pricing_engine = pricing_engines_dict[request_instrument]
    allowed_precision = pricing_engine.instrument.currency_leg_1.currency_precision
    assert_raise(request_order_amount > 10**(-allowed_precision),
                 InvalidAmountError(f"The amount {request_order_amount} is too small. The minimum amount is {allowed_precision}"))
    maximum_amount = pricing_engine.pool_amount_leg_1_currency
    assert_raise(not((request_order_side == "buy") and (request_order_amount >= maximum_amount)),
                 InvalidAmountError(f"The amount {request_order_amount} is too large. The maximum amount is {maximum_amount}"))

    return True
