# Multisport GFX-Engine V2 – Projekt-Review PHASE 0 + PHASE 1

Dieses Dokument beschreibt die bisher durchgeführten Schritte: Git-Setup, Grundstruktur, venv, Redis-Anbindung und Basis-Tools.

---

# PHASE 0 — REPO & SKELETT (Tag 1)

## 0.1 Projektverzeichnis

```bash
sudo mkdir -p /opt/gfx-engine
sudo chown -R $USER:$USER /opt/gfx-engine
```

## 0.2 Git initialisieren

```bash
cd /opt/gfx-engine
git init
git branch -M main
git remote add origin https://github.com/richtertoralf/gfx-engineV2.git
```

## 0.3 Projektstruktur

```
input/        kes/ hora/ winlaufen/
core/         config.py redis.py model/
api/          main.py state/ start/ startlist/ biathlon/
dashboard/    control.html control.js modules/
renderer/     index.html update.js modules/
static/       css/ js/
tools/        reset_redis.py
docs/         README.md
```

## 0.4 .gitignore

```
__pycache__/
*.pyc
.env
.venv/
venv/
.DS_Store
.vscode/
.idea/
dump.rdb
```

## 0.5 Commit für Phase 0

```bash
git add .
git commit -m "Phase 0: Clean folder structure for Multisport GFX Engine V2"
git push -u origin main --force
```

---

# PHASE 1 — REDIS + CORE-BASIS (Tag 2)

Ziel: Redis lauffähig, Python-Abstraktion verfügbar, Reset-Tool funktionsfähig.

## 1.1 Redis installieren

```bash
sudo apt update
sudo apt install redis-server -y
sudo systemctl enable --now redis
redis-cli ping
```

## 1.2 Python-venv erstellen

```bash
cd /opt/gfx-engine
python3 -m venv .venv
source .venv/bin/activate
pip install redis
```

## 1.3 core/config.py

```python
REDIS_URL = "redis://localhost:6379/0"
NAMESPACE = "gfx:"
```

## 1.4 core/redis.py

Implementierte Funktionen:

- set_json(key, data)
- get_json(key)
- exists(key)
- delete_pattern(pattern)

Redis-Client:

```python
client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
```

## 1.5 tools/reset_redis.py

```python
delete_pattern("gfx:*")
delete_pattern("event:*")
delete_pattern("startlist:*")
```

Projektroot wurde per sys.path hinzugefügt.

## 1.6 Funktionstests

### Test: JSON setzen

```bash
python3 - << 'EOF'
from core.redis import set_json
set_json("test:key", {"hello": "world", "value": 123})
print("OK")
EOF
```

### Test: JSON lesen

```bash
python3 - << 'EOF'
from core.redis import get_json
print(get_json("test:key"))
EOF
```

### redis-cli Test

```bash
redis-cli GET gfx:test:key
```

### Reset-Tool Test

```bash
python3 tools/reset_redis.py
```

---

# PHASE 1 — STATUS: Abgeschlossen

- Redis läuft  
- venv aktiv und installiert  
- redis-Python-Client vorhanden  
- JSON-Abstraktion voll funktionsfähig  
- Reset-Tool funktioniert  
- Werte setzen/lesen/löschen erfolgreich  
- Noch keine Sportlogik  

Phase 1 ist vollständig abgeschlossen.


---

# PHASE 2 — API BASIS (Tag 3)

Ziel: FastAPI starten, Router einbinden, Redis-State-Endpunkte funktionsfähig.

## 2.1 FastAPI & Uvicorn installieren

```bash
source .venv/bin/activate
pip install fastapi uvicorn[standard] redis
```

## 2.2 api/main.py erstellt

```python
from fastapi import FastAPI

from api.state.router import router as state_router
from api.start.router import router as start_router
from api.startlist.router import router as startlist_router
from api.biathlon.router import router as biathlon_router

app = FastAPI(title="Multisport GFX Engine V2")

@app.get("/")
async def root():
    return {"status": "ok", "engine": "gfx-engine-v2"}

app.include_router(state_router,     prefix="/state",     tags=["state"])
app.include_router(start_router,     prefix="/start",     tags=["start"])
app.include_router(startlist_router, prefix="/startlist", tags=["startlist"])
app.include_router(biathlon_router,  prefix="/biathlon",  tags=["biathlon"])
```

## 2.3 Router für state/start/startlist/biathlon ergänzt

### Beispiel state-Router:

```python
from fastapi import APIRouter
from core.redis import get_json, set_json

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "ok", "component": "state"}

@router.get("/get/{key}")
async def get_state(key: str):
    return {"key": key, "value": get_json(f"state:{key}")}

@router.post("/set/{key}")
async def set_state(key: str, payload: dict):
    set_json(f"state:{key}", payload)
    return {"status": "stored", "key": key, "value": payload}
```

Alle anderen Router erhielten mindestens:

```python
router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "ok", "component": "<name>"}
```

## 2.4 API manuell gestartet

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Erfolgreicher Start:

```
Uvicorn running on http://0.0.0.0:8000
```

## 2.5 API Funktionstests

### Ping:

```
http://<server>:8000/state/ping
```

→ `200 OK`

### JSON setzen:

```bash
curl -X POST "http://localhost:8000/state/set/test" \
     -H "Content-Type: application/json" \
     -d '{"hello":"world"}'
```

### JSON lesen:

```bash
curl http://localhost:8000/state/get/test
```

### Redis prüfen:

```bash
redis-cli GET gfx:state:test
```

## 2.6 Phase-2 Status

- FastAPI lauffähig  
- Router eingebunden  
- state/set + state/get funktionsfähig  
- API ↔ Redis vollständig getestet  
- Alle Router antworten `/ping`  
- Basis für Dashboard & Renderer steht  

**Phase 2 abgeschlossen.**


---

# PHASE 3 — API-Laufsystem & Event-Basis (Tag 4)

Ziel: Die API dauerhaft betreiben, Logging aktivieren und einen universellen Event-Endpunkt bereitstellen, den das Dashboard später nutzt.

## 3.1 systemd-Service für die API

Service-Datei erstellt:

```
sudo nano /etc/systemd/system/gfx-engine.service
```

Inhalt:

```
[Unit]
Description=Snowgames Multisport GFX Engine API
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/gfx-engine
ExecStart=/opt/gfx-engine/.venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3
StandardOutput=append:/var/log/gfx-engine/api.log
StandardError=append:/var/log/gfx-engine/api.log

[Install]
WantedBy=multi-user.target
```

Log-Ordner:

```bash
sudo mkdir -p /var/log/gfx-engine
sudo chown tori:tori /var/log/gfx-engine
```

Service aktiviert:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gfx-engine
```

## 3.2 Logging implementiert

Datei `core/logging.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("gfx-engine")
```

## 3.3 Event-Router erstellt

Neuer Ordner:

```
api/event/
```

Datei `api/event/router.py`:

```python
from fastapi import APIRouter
from core.redis import set_json
from core.logging import logger

router = APIRouter()

@router.post("/trigger")
async def trigger_event(payload: dict):
    event_type = payload.get("type", "UNKNOWN")
    set_json("event:last", payload)
    logger.info("Event received: %s", event_type)
    return {"status": "ok", "event": event_type}
```

Router in `api/main.py` eingebunden:

```python
from api.event.router import router as event_router
app.include_router(event_router, prefix="/event", tags=["event"])
```

## 3.4 Event-Endpunkt getestet

Event senden:

```bash
curl -X POST http://localhost:8000/event/trigger \
     -H "Content-Type: application/json" \
     -d '{"type":"TEST_EVENT","data":{"foo":123}}'
```

Redis prüfen:

```bash
redis-cli GET gfx:event:last
```

## 3.5 Phase 3 – Status

- systemd-Service installiert und läuft  
- Logging aktiv  
- Event-Router vorhanden  
- Dashboard kann später universelle Events senden  
- Renderer kann später darauf reagieren  
- Keine endgültige Event-Struktur nötig (wird erst im Dashboard definiert)

**Phase 3 abgeschlossen.**
