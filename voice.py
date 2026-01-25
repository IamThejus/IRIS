import subprocess
import tempfile
import os

PIPER_BIN = "piper"
VOICE_MODEL = "voices/en_US-amy-medium.onnx"

def speak(text):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name

    cmd = [
        PIPER_BIN,
        "--model", VOICE_MODEL,
        "--output_file", wav_path
    ]

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    process.stdin.write(text.encode("utf-8"))
    process.stdin.close()
    process.wait()

    # Play audio
    os.system(f"aplay {wav_path}")

    os.remove(wav_path)


