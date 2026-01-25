import struct
import numpy as np
import tempfile
import soundfile as sf
import os
from ai_engine import *
from voice import *

from api_calls import *
from settings import *

def contains(words, text):
    text = text.lower()
    return all(w in text for w in words)

print("🎙️ IRIS is listening... Say 'Hey IRIS'")

def record_command():
    frames = []
    for _ in range(int(SAMPLE_RATE / 1024 * RECORD_SECONDS)):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    audio = b"".join(frames)
    audio_np = np.frombuffer(audio, dtype=np.int16)
    audio_np = audio_np.astype(np.float32) / 32768.0

    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(temp_wav.name, audio_np, SAMPLE_RATE)

    return temp_wav.name

try:
    while True:
        pcm_bytes = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = np.frombuffer(pcm_bytes, dtype=np.int16)

        if porcupine.process(pcm) >= 0:
            print("🟢 Wake word detected!")
            print("🎧 Listening for command...")

            wav_file = record_command()

            segments, info = whisper.transcribe(wav_file, language="en")

            os.remove(wav_file)

            text = "".join(segment.text for segment in segments)
            command = text.strip().lower()

            print("🗣️ Command:", command)

            if contains(["fan", "on"], command) or "start fan" in command:
                turn_on_off()

            elif contains(["fan", "increase"], command) or "speed up" in command:
                speedup()

            elif contains(["fan", "decrease"], command) or "slow down" in command:
                speeddown()

            elif "close" in command:
                print("🛑 Exiting IRIS")
                break
            else:
                reply=get_ai_reply(command)
                speak(reply)

            print("👂 Waiting for wake word...\n")

except KeyboardInterrupt:
    print("\n🛑 Stopped")

finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()
