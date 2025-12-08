from fastapi import APIRouter
from core.redis import get_json, set_json

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "ok", "component": "state"}

@router.get("/get/{key}")
async def get_state(key: str):
    value = get_json(f"state:{key}")
    return {"key": key, "value": value}

@router.post("/set/{key}")
async def set_state(key: str, payload: dict):
    set_json(f"state:{key}", payload)
    return {"status": "stored", "key": key, "value": payload}

