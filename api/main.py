from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Router importieren
from api.state.router import router as state_router
from api.start.router import router as start_router
from api.startlist.router import router as startlist_router
from api.biathlon.router import router as biathlon_router
from api.event.router import router as event_router

app = FastAPI(title="Multisport GFX Engine V2")

# ============================================
# Root Endpoint
# ============================================

@app.get("/")
async def root():
    return {"status": "ok", "engine": "gfx-engine-v2"}

# ============================================
# STATIC FILES SERVING
# ============================================

# Statische Dateien für CSS, JS, Bilder
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# Dashboard-HTML (control.html und weitere UI-Dateien)
app.mount(
    "/dashboard",
    StaticFiles(directory="dashboard"),
    name="dashboard"
)

# ============================================
# API ROUTER
# ============================================

app.include_router(state_router, prefix="/state", tags=["state"])
app.include_router(start_router, prefix="/start", tags=["start"])
app.include_router(startlist_router, prefix="/startlist", tags=["startlist"])
app.include_router(biathlon_router, prefix="/biathlon", tags=["biathlon"])
app.include_router(event_router, prefix="/event", tags=["event"])
