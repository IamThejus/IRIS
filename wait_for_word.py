import pvporcupine
import pyaudio
import struct
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
from whisper_test_mic import *

# === SETTINGS ===
WAKE_WORD_FILE = "iris.ppn"  # your custom .ppn file
ACCESS_KEY = "9N0aoPuDnlrN0wLoh4qzVmxfyeDnVJJXLIoQ91Sg2T+OIiu3VGtC4A=="
VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"

# === INIT VOSK ===
model = Model(VOSK_MODEL_PATH)
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

# === INIT Wake Word ===
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[WAKE_WORD_FILE]
)

pa = pyaudio.PyAudio()
stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("\🎙️ IRIS is listening... (say 'Hey IRIS')")
out=True
try:
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        if porcupine.process(pcm) >= 0:
            print("🟢 Wake word detected! Listening for command...")

            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                                   channels=1, callback=audio_callback):
                grammar = '["turn on ac", "turn off ac", "fan on", "fan off"]'
                rec = KaldiRecognizer(model, 16000,grammar)

                while True:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        print("🗣️ Command:", result.get("text", ""))
                        if result.get("text", "")=="close":
                            out=False
                        break
            if out!=True:
                break
            print("👂 Listening again for wake word...")

except KeyboardInterrupt:
    print("\n🛑 Exiting cleanly.")
finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()
