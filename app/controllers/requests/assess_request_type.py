from typing import Union

from app.models.exceptions.exceptions import *

from app.tools.assert_raise import assert_raise


def asses_request_type(request_body: dict) -> str:
    """
    Asseses what type of request was sent by the customer.

    Args:
        request_body: The request body as sent by the customer

    Returns: The strings "price_request" or "create_order_request", or Errors if such occured.
    """

    assert_raise("type" in request_body.keys(),
                 PriceRequestValueError("Invalid request type."))
    request_type = request_body["type"]
    assert_raise(isinstance(request_type, str),
                 PriceRequestFormatError(f"type: Expected str, got {type(request_type)} instead."))
    if request_body["type"].lower() == "subscribe":
        return "price_request"
    elif request_body["type"].lower() == "create_order":
        return "create_order_request"
    elif request_body['type'].lower()=="stream_predefined":
        return "custom_response"
    else:
        raise SubscriptionRequestError(f"Unknown request type {request_type}")
