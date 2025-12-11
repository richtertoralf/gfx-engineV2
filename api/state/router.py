# api/state/router.py
# ------------------------------------------------------------
# V2 – Einheitlicher globaler Engine-State
# ------------------------------------------------------------

from fastapi import APIRouter
from core.redis import get_json, set_json

router = APIRouter()

GLOBAL_STATE_KEY = "state"    # gespeicherter Redis-Key: gfx:state


# ------------------------------------------------------------
# GET /api/state
# ------------------------------------------------------------
@router.get("/")
async def get_global_state():
    """
    Gibt das komplette State-Objekt zurück.
    """
    state = get_json(GLOBAL_STATE_KEY)
    return state or {}


# ------------------------------------------------------------
# PATCH /api/state
# ------------------------------------------------------------
@router.patch("/")
async def patch_global_state(payload: dict):
    """
    Aktualisiert Teilbereiche des globalen State-Objekts:
    - Merged neue Werte
    - Bewahrt vorhandene
    """
    current = get_json(GLOBAL_STATE_KEY) or {}
    current.update(payload)
    set_json(GLOBAL_STATE_KEY, current)

    from api.state.websocket_manager import manager
    await manager.broadcast(current)

    return {"status": "updated", "state": current}


# ------------------------------------------------------------
# POST /api/state/reset
# ------------------------------------------------------------
@router.post("/reset")
async def reset_state():
    """
    Setzt den State auf ein leeres Dict zurück.
    Wird z.B. beim Event-Neustart oder Renderer-Reset verwendet.
    """
    empty = {}
    set_json(GLOBAL_STATE_KEY, empty)
    return {"status": "reset", "state": empty}


# ------------------------------------------------------------
# OPTIONAL: Ping für Healthchecks
# ------------------------------------------------------------
@router.get("/ping")
async def ping():
    return {"status": "ok", "component": "state-api"}


# ------------------------------------------------------------
# WebSocket
# ------------------------------------------------------------

from fastapi import WebSocket
from api.state.websocket_manager import manager

@router.websocket("/ws")
async def state_websocket(websocket: WebSocket):
    """
    WebSocket für Live-State-Updates.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Renderer sendet nichts, bleibt nur offen
            await websocket.receive_text()
    except Exception:
        manager.disconnect(websocket)
