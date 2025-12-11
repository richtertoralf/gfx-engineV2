# api/state/websocket_manager.py
# ------------------------------------------------------------
# Verwaltet alle WebSocket-Verbindungen & Broadcasts
# ------------------------------------------------------------

from fastapi import WebSocket
import json


class StateWebSocketManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcast(self, message: dict):
        data = json.dumps(message)
        for ws in list(self.active):
            try:
                await ws.send_text(data)
            except Exception:
                # Wenn WebSocket tot ist -> entfernen
                self.disconnect(ws)


# Singleton-Instanz
manager = StateWebSocketManager()
