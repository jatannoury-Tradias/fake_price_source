import uuid
import datetime
import json
import logging

from app.tools.object2dict import object2dict

from app.models.trading.order import Order
from app.models.trading.trade import Trade
from app.models.order_confirmation import OrderConfirmation
from app.models.order_rejection import OrderRejection
from app.models.customer import Customer

from app.config.pricing_engines import pricing_engines_dict
from app.config.counterparties import counterparties, counterparties_dict
# from app.config.database import trades_table, orders_table

from app.controllers.responses.orders.order_confirmation import confirmation_message
from app.controllers.responses.orders.order_rejection import rejection_message
from app.controllers.requests.orders.check_order import is_valid_order


logger = logging.getLogger(__name__)


def create_order_confirmation_object(order: Order,
                                     trade: Trade) -> OrderConfirmation:
    """
    Maps a trade and an order object to an order confirmation object
    Args:
        order: The order object involved in the order confirmation
        trade: The trade object involved in the order confirmation

    Returns: Order confirmation object based on the data in the input objects

    """
    return OrderConfirmation(customer=order.created_by,
                             order_id=order.order_id,
                             trade_id=trade.trade_id,
                             order_side=order.order_side,
                             order_amount=order.amount,
                             order_instrument=order.order_instrument,
                             confirmed_price=trade.price,
                             total_amount=trade.leg_2_amount,
                             executed_at=trade.executed_at,
                             client_order_id=order.client_order_id)


def process_order(customer: Customer,
                  request_body: dict) -> dict:
    """
    Processes the order (evaluation, saving to db) and generates the response message

    Args:
        customer: The customer who sent the order
        request_body: the request which the customer sent as a dict

    Returns: The response message as a dict

    """
    response_body = dict()
    order_id = uuid.uuid4()
    try:
        is_valid_order(request_body)
    except Exception as e:
        logger.exception(str(e))
        order_rejection = OrderRejection(customer=customer,
                                         order_id=order_id,
                                         rejection_message=str(e),
                                         timestamp=datetime.datetime.utcnow(),
                                         request_body=json.dumps(request_body))
        # orders_table.put(order_rejection.order_id, object2dict(order_rejection))
        response_body = rejection_message(order_rejection)
    else:
        created_by = [counterparty for counterparty in counterparties if counterparty.customer == customer][0]
        accepted_by = counterparties_dict["AMM"]

        created_at = datetime.datetime.utcnow()
        order_side = request_body["order"]["side"].lower()
        order_type = request_body["order"]["order_type"]

        leg_1_amount = request_body["order"]["amount"]
        pricing_engine = pricing_engines_dict[request_body["order"]["instrument"]]
        instrument = pricing_engine.instrument
        leg_2_amount = pricing_engine.trade_currency_1_for_currency_2(leg_1_amount, order_side)
        confirmed_price = leg_2_amount/leg_1_amount

        if "client_order_id" in request_body["order"]:
            client_order_id = request_body["order"]["client_order_id"]
        else:
            client_order_id = ""

        order = Order(order_id=order_id,
                      created_at=created_at,
                      created_by=created_by,
                      accepted_by=accepted_by,
                      communication_channel="WS",
                      order_status="confirmed",
                      order_instrument=instrument,
                      order_type=order_type,
                      order_side=order_side,
                      amount=leg_1_amount,
                      amount_currency=instrument.currency_leg_1,
                      request_body=json.dumps(request_body),
                      response_body="",
                      client_order_id=client_order_id)

        trade_id = uuid.uuid4()
        leg_1_recipient = created_by if order_side.lower() == "buy" else accepted_by
        leg_2_recipient = accepted_by if order_side.lower() == "buy" else created_by

        trade = Trade(order=order,
                      trade_id=trade_id,
                      executed_at=created_at,
                      instrument=instrument,
                      leg_1_amount=leg_1_amount,
                      leg_1_currency=instrument.currency_leg_1,
                      leg_1_recipient=leg_1_recipient,
                      leg_2_amount=leg_2_amount,
                      leg_2_currency=instrument.currency_leg_2,
                      leg_2_recipient=leg_2_recipient,
                      fees=0,
                      fees_currency=None,
                      fee_payer=None,
                      price=confirmed_price,
                      prices_at_execution=None,
                      settlement_details=None)

        order_confirmation = create_order_confirmation_object(order, trade)
        response_body = confirmation_message(order_confirmation)
        order.response_body = json.dumps(response_body)

        # orders_table.put(order.order_id, object2dict(order))
        # trades_table.put(trade.trade_id, object2dict(trade))

    finally:
        return response_body

