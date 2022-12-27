import pytest

from app.controllers.requests.assess_request_type import asses_request_type
from app.config.pricing_engines import pricing_engines_dict

from app.models.exceptions.exceptions import PriceRequestFormatError, SubscriptionRequestError

import random


def test_prices_subscription_positive():
    for instrument_code in pricing_engines_dict:
        request_body = {
            "type": "subscribe",
            "instrument": instrument_code
        }
        assert asses_request_type(request_body) == "price_request"


def my_other_function():
    print("do not print")


def test_prices_subscription_subscribe_negative():
    my_other_function()
    for instrument_code in pricing_engines_dict:
        request_body = {
            "type": "invalid",
            "instrument": instrument_code
        }
        with pytest.raises(SubscriptionRequestError):
            asses_request_type(request_body)



"""

def test_prices_subscription_instrument_negative():
    invalid_instrument = "NOT-VALID"
    while invalid_instrument in pricing_engines_dict.keys():
        invalid_instrument += "a"

    request_body = {
        "type": "subscribe",
        "instrument": invalid_instrument
    }
    with pytest.raises(PriceRequestFormatError):
        asses_request_type(request_body)
"""