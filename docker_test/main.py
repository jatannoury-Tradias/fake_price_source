import asyncio
import websockets
import http



async def echo_header(websocket, path):
    extra_headers = websocket.extra_headers
    async for message in websocket:
        await websocket.send(message + str(extra_headers))


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)


async def main():
    host = "0.0.0.0"
    async with websockets.serve(echo_header, "localhost", 8765, create_protocol=HeaderParamProtocol):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
