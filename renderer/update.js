console.log("[RENDERER] update.js loaded");

//
// WebSocket verbinden
//
const ws = new WebSocket(`ws://${location.host}/api/state/ws`);

ws.onopen = () => console.log("[RENDERER] WS connected");
ws.onerror = err => console.error("[RENDERER] WS error:", err);
ws.onmessage = msg => {
    try {
        const state = JSON.parse(msg.data);
        renderState(state);
    } catch (e) {
        console.error("WS parse error:", e, msg.data);
    }
};


//
// Haupt-Render-Funktion
//
function renderState(state) {
    // State an alle Module verteilen
    renderStartOverlay(state);
}


//
// Modul: Start-Overlay anzeigen/verbergen
//
function renderStartOverlay(state) {
    const box = document.getElementById("overlay-start");
    const visible = state.overlay === true;

    if (visible) {
        box.classList.add("visible");
    } else {
        box.classList.remove("visible");
    }
}

