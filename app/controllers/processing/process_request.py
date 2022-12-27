import json
import logging
import datetime
import asyncio

from app.models.customer import Customer
from app.controllers.processing.S3_bucket_handler import s3_bucket_controller
from app.config.constants import PRICE_UPDATE_TIME

from app.controllers.responses.send_error_message import send_error_message
from app.controllers.requests.assess_request_type import asses_request_type
from app.controllers.requests.assess_source_type import asses_source_type
from app.controllers.requests.prices.check_price_subscription import is_valid_price_subscription
from app.controllers.requests.orders.check_order import is_valid_order

from app.controllers.processing.process_order import process_order
from app.controllers.processing.process_price_stream import send_prices
from app.controllers.processing.process_predefined_and_stream import process_and_stream

logger = logging.getLogger(__name__)


async def process_request(customer: Customer,
                          websocket,
                          raw_message: str):
    """
    Handles the request by the customer by converting it to json, checking the syntax and generating the desired response
    Args:
        customer: The customer who sent the resquest
        websocket: The websocket through which responses should be sent back to the customer
        raw_message: The raw (str) version of the message sent by the customer

    Returns: None

    """
    # Check whether the request can be converted to json
    try:
        request_body = json.loads(raw_message)

        # Check which sort of request was sent
        request_type = asses_request_type(request_body)
        source_type=asses_source_type(request_body)

        # Handle order requests
        if request_type == "create_order_request" and is_valid_order(request_body):
            response = process_order(customer, request_body)
            await websocket.send(json.dumps(response))

        # Handle price streaming requests
        elif request_type == "price_request" and is_valid_price_subscription(request_body):
            await send_prices(websocket, request_body)
        elif request_type == 'custom_response':
            await process_and_stream(websocket,source_type,request_body)


    except Exception as e:
        logger.exception(str(e))
        await send_error_message(websocket, str(e), datetime.datetime.utcnow())
