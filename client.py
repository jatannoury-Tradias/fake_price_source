import asyncio
import websockets
import json


URL_LOCAL = "ws://localhost:8765/"
URL_REMOTE = "ws://18.196.187.64:8765"
NEW = "ws://PrototypingLoadBalancer-1063592976.eu-central-1.elb.amazonaws.com"
NEW2 = "wss://prototyping.tradias.de"
#AWS_URL = "wss://c2di9yuin0.execute-api.eu-central-1.amazonaws.com/mock"
NEW3 = "ws://localhost:8765/"

price_subscription = {
    "type": "subscribe",
    "channelname": "prices",
    "instrument": "TKN-EUR",
    "levels": [10, 20, 30]
}

order_message = {
   "type": "CREATE_ORDER",
   "order": {
         "instrument": "TKN-EUR",
         "order_type": "MARKET",
         "side": "BUY",
         "amount": 1.5
         #"client_order_id": "Satoshi Nakamoto" #Optional
   }
}


async def hello():
    async with websockets.connect(f"{URL_LOCAL}", extra_headers={"Authorization": "a"}) as websocket:
        await websocket.send(json.dumps(order_message))
        while True:
            print(await websocket.recv())


if __name__ == "__main__":
    asyncio.run(hello())