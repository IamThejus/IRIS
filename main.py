import numpy as np
import tempfile
import soundfile as sf
import os
import threading
import asyncio
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

from ai_engine import get_ai_reply
from voice import speak
from api_calls import turn_on_off, speedup, speeddown,turn_on_off_ac,ac_cool,ac_hot
from settings import porcupine, stream, whisper, SAMPLE_RATE, pa

# ─────────────────────────────────────────────
# Connection manager
# ─────────────────────────────────────────────
class ConnectionManager:
    def __init__(self):
        self.clients: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.clients.append(ws)

    def disconnect(self, ws: WebSocket):
        self.clients.remove(ws)

    async def broadcast(self, data: dict):
        dead = []
        for ws in self.clients:
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.clients.remove(ws)

manager = ConnectionManager()

# ─────────────────────────────────────────────
# Shared asyncio loop (set once uvicorn starts)
# ─────────────────────────────────────────────
_loop: asyncio.AbstractEventLoop | None = None

def broadcast_sync(data: dict):
    """Thread-safe broadcast from the hardware thread."""
    if _loop and manager.clients:
        asyncio.run_coroutine_threadsafe(manager.broadcast(data), _loop)

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def contains(words, text):
    text = text.lower()
    return all(w in text for w in words)

def record_command():
    frames = []
    for _ in range(int(SAMPLE_RATE / 1024 * 4)):  # 4 seconds
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    audio = b"".join(frames)
    audio_np = np.frombuffer(audio, dtype=np.int16).astype(np.float32) / 32768.0

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, audio_np, SAMPLE_RATE)
    return tmp.name

# ─────────────────────────────────────────────
# Hardware loop (runs in background thread)
# ─────────────────────────────────────────────
def hardware_loop():
    print("🎙️  IRIS is listening... Say 'Hey IRIS'")
    try:
        while True:
            pcm_bytes = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = np.frombuffer(pcm_bytes, dtype=np.int16)

            if porcupine.process(pcm) >= 0:
                print("🟢 Wake word detected!")
                broadcast_sync({"state": "listening"})

                print("🎧 Listening for command...")
                wav_file = record_command()

                segments, _ = whisper.transcribe(wav_file, language="en")
                os.remove(wav_file)

                command = "".join(seg.text for seg in segments).strip().lower()
                print("🗣️  Command:", command)

                # ── IoT commands ──────────────────────────────
                if contains(["fan", "on"], command) or "start fan" in command:
                    turn_on_off()
                    broadcast_sync({"state": "action", "command": command, "result": "Fan toggled ✓"})
                    speak("fan is turned on")
                    print("👂 Waiting for wake word...\n")
                    continue

                elif contains(["fan", "increase"], command) or "speed up" in command:
                    speedup()
                    broadcast_sync({"state": "action", "command": command, "result": "Fan speed increased ✓"})
                    speak("fan speed increased")
                    print("👂 Waiting for wake word...\n")
                    continue

                elif contains(["fan", "decrease"], command) or "slow down" in command:
                    speeddown()
                    broadcast_sync({"state": "action", "command": command, "result": "Fan speed decreased ✓"})
                    speak("fan speed decreased")
                    print("👂 Waiting for wake word...\n")
                    continue

                elif contains(["fan", "off"], command) or "slow down" in command:
                    turn_on_off()
                    broadcast_sync({"state": "action", "command": command, "result": "Fan turning  Off ✓"})
                    speak("fan is turned off")
                    print("👂 Waiting for wake word...\n")
                    continue

                ## For AC

                elif contains(["ac", "on"], command):
                    turn_on_off_ac()
                    broadcast_sync({"state": "action", "command": command, "result": "AC turning  On ✓"})
                    speak("AC is turned on")
                    print("👂 Waiting for wake word...\n")
                    continue

                elif contains(["ac", "off"], command) :
                    turn_on_off_ac()
                    broadcast_sync({"state": "action", "command": command, "result": "AC turning  Off ✓"})
                    speak("AC is turned off")
                    print("👂 Waiting for wake word...\n")
                    continue

                elif contains(["ac", "increase"], command) :
                    ac_hot()
                    broadcast_sync({"state": "action", "command": command, "result": "AC Temperature  Increased ✓"})
                    speak("AC temperature increased")
                    print("👂 Waiting for wake word...\n")
                    continue

                elif contains(["ac", "decrease"], command) :
                    ac_hot()
                    broadcast_sync({"state": "action", "command": command, "result": "AC Temperature  Decreased ✓"})
                    speak("AC temperature decreased")
                    print("👂 Waiting for wake word...\n")
                    continue

                elif "close" in command or "exit" in command or "quit" in command:
                    print("🛑 Exiting IRIS")
                    broadcast_sync({"state": "idle"})
                    break

                # ── AI reply ─────────────────────────────────
                else:
                    broadcast_sync({"state": "thinking", "command": command})
                    reply = get_ai_reply(command)
                    print("🤖 Reply:", reply)

                    broadcast_sync({"state": "speaking", "reply": reply})
                    speak(reply)

                    # Log to conversation history on the UI
                    broadcast_sync({"state": "history", "command": command, "reply": reply})
                    broadcast_sync({"state": "idle"})

                print("👂 Waiting for wake word...\n")

    except Exception as e:
        print(f"❌ Hardware loop error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
        print("🛑 Stopped")

# ─────────────────────────────────────────────
# FastAPI app & lifespan
# ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(application: FastAPI):
    global _loop
    _loop = asyncio.get_running_loop()
    t = threading.Thread(target=hardware_loop, daemon=True)
    t.start()
    print("🌐 Web UI available at http://localhost:8000")
    yield

app = FastAPI(lifespan=lifespan)

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("web_ui/index.html", "r",encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    # Send current idle state immediately on connect
    await websocket.send_text(json.dumps({"state": "idle"}))
    try:
        while True:
            await websocket.receive_text()   # keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
