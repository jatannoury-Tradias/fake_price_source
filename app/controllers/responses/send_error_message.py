import json
from app.tools.dt_helper import datetime_obj2z_string


async def send_error_message(websocket, message, timestamp):
    error_message = {
        "type": "error",
        "message": message,
        "timestamp": datetime_obj2z_string(timestamp)
    }
    await websocket.send(json.dumps(error_message))
