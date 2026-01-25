
import struct
import numpy as np
import tempfile
import soundfile as sf

from api_calls import *
from settings import *

###################################### Classifiers #################

def contains(words, text):
    return all(w in text for w in words)



print("🎙️ IRIS is listening... Say 'Hey IRIS'")

def record_command():
    frames = []
    for _ in range(int(SAMPLE_RATE / 1024 * RECORD_SECONDS)):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    audio = b"".join(frames)
    audio_np = np.frombuffer(audio, dtype=np.int16)

    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(temp_wav.name, audio_np, SAMPLE_RATE)

    return temp_wav.name


try:
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        if porcupine.process(pcm) >= 0:
            print("🟢 Wake word detected!")
            print("🎧 Listening for command...")

            wav_file = record_command()

            segments, info = whisper.transcribe(
                wav_file,
                language="en"
            )

            text = ""
            for segment in segments:
                text += segment.text

            command = text.strip().lower()
            print("🗣️ Command:", command)

            # ===== INTENT EXAMPLES =====

            if contains(["fan", "on"], command) or "start fan" in command:
                turn_on_off()

            elif contains(["fan", "increase"], command) or "speed up" in command:
                speedup()

            elif contains(["fan", "decrease"], command) or "slow down" in command:
                speeddown()
            elif "close" in command:
                print("🛑 Exiting IRIS")
                break

            print("👂 Waiting for wake word...\n")

except KeyboardInterrupt:
    print("\n🛑 Stopped")

finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()
