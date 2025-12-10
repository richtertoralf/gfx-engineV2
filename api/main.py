from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# V2-Konfiguration laden
from core.config import PATHS

# Router importieren
from api.state.router import router as state_router
from api.start.router import router as start_router
from api.startlist.router import router as startlist_router
from api.biathlon.router import router as biathlon_router
from api.event.router import router as event_router


app = FastAPI(title="Multisport GFX Engine V2")


# =====================================================
# ROOT ENDPOINT
# =====================================================
@app.get("/")
async def root():
    return {"status": "ok", "engine": "gfx-engine-v2"}


# =====================================================
# STATIC FILES (NEUES V2-PATH SYSTEM)
# =====================================================

app.mount(
    "/static",
    StaticFiles(directory=PATHS.static),
    name="static"
)

app.mount(
    "/dashboard",
    StaticFiles(directory=PATHS.dashboard),
    name="dashboard"
)

app.mount(
    "/renderer",
    StaticFiles(directory=PATHS.renderer),
    name="renderer"
)


# =====================================================
# API ROUTER (REST-KONFORM)
# =====================================================
app.include_router(state_router,     prefix="/api/state",     tags=["state"])
app.include_router(start_router,     prefix="/api/start",     tags=["start"])
app.include_router(startlist_router, prefix="/api/startlist", tags=["startlist"])
app.include_router(biathlon_router,  prefix="/api/biathlon",  tags=["biathlon"])
app.include_router(event_router,     prefix="/api/event",     tags=["event"])
