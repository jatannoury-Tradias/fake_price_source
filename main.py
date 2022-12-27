import logging
import asyncio
import datetime
import time

import websockets
import websockets.exceptions

from app.authentication.header_param_protocol import HeaderParamProtocol

from app.controllers.processing.process_request import process_request
from app.config.constants import HOST, PORT, PRICE_UPDATE_TIME


async def callback(websocket, path):
    customer = websocket.customer
    await websocket.send("WEBSOCKET CONNECTED, Kindly find following the ws documentation")
    await websocket.send("{type:stream_predefined}")
    await websocket.send("{source:(Optional, default='fromS3bucket') fromRequest/fromS3bucket}")
    await websocket.send("{fileName:(Optional, default='FAKE_PRICE_SOURCE_CONFIG.txt')}")
    await websocket.send("{time_delta:(Optional, default=2000ms)time interval in milliseconds}")
    await websocket.send("{payload:(default=[{Warning: Payload empty}])array of objects}")
    logger.info(f"At {datetime.datetime.utcnow()}, {customer.customer_name} connected.")
    try:
        async for message in websocket:
            try:
                await process_request(customer, websocket, message)
            except Exception as e:
                print(e)
                logger.exception(f"Unknown error: {str(e)}")


    except websockets.ConnectionClosed as e:
        logger.info(f"At {datetime.datetime.utcnow()}, {customer.customer_name} disconnected.")
    except Exception as e:
        print(e)
        logger.exception(f"At {datetime.datetime.utcnow()}, an unknown exception occured: {str(e)}")


async def main():
    async with websockets.serve(callback, HOST, PORT, create_protocol=HeaderParamProtocol):
        await asyncio.Future()


if __name__ == '__main__':
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info('Start')
    asyncio.run(main())
