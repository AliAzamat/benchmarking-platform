import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from gateway.bus import subscribe_runs

app = FastAPI(title="Run Stream Gateway")
clients: set[WebSocket] = set()


async def broadcast(payload: bytes) -> None:
    """Push one run event to every connected dashboard."""
    dead = []
    for ws in clients:
        try:
            await ws.send_bytes(payload)
        except Exception:
            dead.append(ws)
    for ws in dead:
        clients.discard(ws)


@app.on_event("startup")
async def start_subscriber() -> None:
    # Redis → browsers: forward every published run to all clients.
    asyncio.create_task(
        subscribe_runs(lambda data: asyncio.create_task(broadcast(data)))
    )


@app.websocket("/ws/runs")
async def ws_runs(ws: WebSocket) -> None:
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()  # keep the socket open
    except WebSocketDisconnect:
        clients.discard(ws)
