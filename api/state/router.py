from fastapi import APIRouter
from core.redis import get_json, set_json, delete_pattern, exists

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"status": "ok", "component": "state"}


@router.get("/get/{key}")
async def get_state(key: str):
    """
    Holt den State aus Redis:
    gespeicherter Key ist: gfx:state:<key>
    """
    value = get_json(f"state:{key}")
    return {"key": key, "value": value}


@router.post("/set/{key}")
async def set_state(key: str, payload: dict):
    """
    Speichert einen State in Redis:
    Key wird: gfx:state:<key>
    """
    set_json(f"state:{key}", payload)
    return {"status": "stored", "key": key, "value": payload}


@router.delete("/clear")
async def clear_state():
    """
    Löscht alle Keys, die zu gfx:state:* gehören.
    """
    count = delete_pattern("state:*")
    return {"deleted": count}
