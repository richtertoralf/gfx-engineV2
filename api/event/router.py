from fastapi import APIRouter
from core.redis import set_json
from core.logging import logger

router = APIRouter()

@router.post("/trigger")
async def trigger_event(payload: dict):
    """
    Zentrales Event-System.
    Dashboard sendet:
    { "type": "STARTLIST_SHOW", "data": {...} }
    """
    event_type = payload.get("type", "UNKNOWN")
    set_json("event:last", payload)
    logger.info("Event received: %s", event_type)
    return {"status": "ok", "event": event_type}
