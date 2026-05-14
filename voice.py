import subprocess
import tempfile
import os
import winsound

PIPER_BIN = r"D:\Github\IRIS\piper\piper.exe"
VOICE_MODEL = r"D:\Github\IRIS\voices\en_US-amy-medium.onnx"

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
        stdin=subprocess.PIPE
    )

    process.stdin.write(text.encode("utf-8"))
    process.stdin.close()
    process.wait()

    winsound.PlaySound(wav_path, winsound.SND_FILENAME)

    os.remove(wav_path)