from typing import Union

from app.models.exceptions.exceptions import *

from app.tools.assert_raise import assert_raise


def asses_source_type(request_body: dict) -> str:
    """
    Asseses what source of data is desired by the customer.

    Args:
        request_body: The request body as sent by the customer

    Returns: The strings "BUCKET" or "REQUEST", or Errors if such occured.
    """

    if "source" not in request_body or request_body['source']=="":
        return "BUCKET"
    source_type= request_body["source"]
    assert_raise(isinstance(source_type, str),
                 PriceRequestFormatError(f"type: Expected str, got {type(source_type)} instead."))
    if request_body["source"].lower() == "froms3bucket":
        return "BUCKET"
    elif request_body["source"].lower() == "fromrequest":
        return "REQUEST"
    else:
        raise SubscriptionRequestError(f"Unknown source type {source_type}")
