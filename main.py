from datetime import datetime

from fastapi import FastAPI, BackgroundTasks, HTTPException, requests
import websocket_bridge
from rest_bridge import fetch_binance_klines

app = FastAPI()

@app.get("/start_stream")
def start_stream(background_tasks: BackgroundTasks, first_ticker: str, second_ticker: str, interval: str):
    background_tasks.add_task(websocket_bridge.start_websocket_bridge, first_ticker, second_ticker, interval)
    return {"status": "WebSocket streaming started"}
@app.get("/end_stream")
def end_stream():
    websocket_bridge.stop_websocket_bridge()
    return {"status": "WebSocket streaming stopped"}

def convert_to_timestamp(date_str: str) -> int:
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    timestamp = int(date_obj.timestamp()) * 1000
    return timestamp

@app.get("/get_binance_data")
async def get_binance_data(symbol: str, interval: str, start_date: str, end_date: str):
    try:
        startTime = convert_to_timestamp(start_date)
        endTime = convert_to_timestamp(end_date)

        data = fetch_binance_klines(symbol, interval, startTime, endTime)
        return data
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
