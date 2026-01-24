import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

q = queue.Queue()
model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

def callback(indata, frames, time, status):
    q.put(bytes(indata))

# Set your correct input device index
mic_index = 1  # change this after checking with sd.query_devices()

with sd.RawInputStream(samplerate=16000, blocksize=8000,
                       dtype='int16', channels=1,
                       device=mic_index,
                       callback=callback):
    print("🎙️ Speak into the mic (Ctrl+C to stop)")
    while True:
        try:
            data = q.get(timeout=5)
        except queue.Empty:
            print("⚠️ No input received.")
            continue

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("🗣️ You said:", result.get("text", ""))
