from fastapi import FastAPI, BackgroundTasks
import websocket_bridge

app = FastAPI()

@app.get("/start_stream")
def start_stream(background_tasks: BackgroundTasks, first_ticker: str, second_ticker: str, interval: str):
    background_tasks.add_task(websocket_bridge.start_websocket_bridge, first_ticker, second_ticker, interval)
    return {"status": "WebSocket streaming started"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
