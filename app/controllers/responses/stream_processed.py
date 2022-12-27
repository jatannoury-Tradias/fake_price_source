import datetime
import asyncio
import json

async def stream_processed(websocket,config,delta_value):
    now = datetime.datetime.today()
    delta = datetime.timedelta(milliseconds=delta_value)
    time_delta = now + delta
    while True:
        now = datetime.datetime.today()
        if now > time_delta:
            time_delta = now + delta
            try:
                curr = config.pop(0)
                print(curr)
                await websocket.send(json.dumps(curr))
            except:
                break
            await asyncio.sleep(delta_value / 10000)
    await websocket.send("DONE")