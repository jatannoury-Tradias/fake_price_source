from app.models.order_confirmation import OrderConfirmation

from app.tools.dt_helper import datetime_obj2z_string


def confirmation_message(order_confirmation: OrderConfirmation) -> dict:
    """
    Generates a confirmation message from an OrderConfirmation object
    Args:
        order_confirmation: The OrderConfirmation object for which the message should be created.

    Returns: The order confirmation message as a dict

    """
    return {
        "event": "orders",
        "trade_id": str(order_confirmation.trade_id),
        "order_id": str(order_confirmation.order_id),
        "side": order_confirmation.order_side,
        "order_type": "MARKET",
        "amount": order_confirmation.order_amount,
        "instrument": order_confirmation.order_instrument.instrument_code,
        "confirmed_price": order_confirmation.confirmed_price,
        "executed_at": order_confirmation.executed_at,
        "total_amount": order_confirmation.total_amount,
        "order_status": "confirmed",
        "client_order_id": order_confirmation.client_order_id
    }