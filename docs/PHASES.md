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
