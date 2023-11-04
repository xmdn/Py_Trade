# 1. https://github.com/dotnet/aspnetcore/blob/main/src/SignalR/docs/specs/TransportProtocols.md
# 2. https://github.com/dotnet/aspnetcore/blob/main/src/SignalR/docs/specs/HubProtocol.md
import asyncio
import websockets
import requests
import json

BINANCE_URI = "wss://stream.binance.com:9443/ws/btcusdt@kline_1s"
NEGOTIATE_URI = 'http://localhost:5000/hub/negotiate?negotiateVersion=0'
SIGNALR_URI_TEMPLATE = "ws://localhost:5000/hub?id={}"


def toSignalRMessage(data):
    return f'{json.dumps(data)}\u001e'


async def handshake(signalr_ws):
    await signalr_ws.send(toSignalRMessage({"protocol": "json", "version": 1}))
    handshake_response = await signalr_ws.recv()
    print(f"SignalR Handshake Response: {handshake_response}")


async def binance_to_signalr_websocket():
    negotiation = requests.post(NEGOTIATE_URI).json()
    connection_id = negotiation['connectionId']
    signalr_uri = SIGNALR_URI_TEMPLATE.format(connection_id)

    async with websockets.connect(BINANCE_URI) as binance_ws, \
            websockets.connect(signalr_uri) as signalr_ws:
        await handshake(signalr_ws)

        while True:
            binance_message = await binance_ws.recv()

            # Create a message format for SignalR hub
            signalr_message = {
                "type": 1,  # Assuming this type is correct for sending messages to your hub
                "invocationId": "some_unique_id",  # Generate or create an appropriate ID
                "target": "ReceiveStream",
                "arguments": [binance_message],
                "streamIds": ["some_stream_id"]
            }

            # Send to SignalR hub
            await signalr_ws.send(toSignalRMessage(signalr_message))


asyncio.run(binance_to_signalr_websocket())
