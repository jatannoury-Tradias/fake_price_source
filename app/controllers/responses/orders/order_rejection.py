from app.models.order_rejection import OrderRejection


def rejection_message(order_rejection: OrderRejection) -> dict:
    """
    Generates a rejection message from an OrderRejection object
    Args:
        order_rejection: The OrderRejection object for which the message should be created.

    Returns: The order rejection message as a dict

    """
    return {"order_id": order_rejection.order_id,
            "message": order_rejection.rejection_message,
            "timestamp": order_rejection.timestamp}