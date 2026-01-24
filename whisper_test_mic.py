import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile

model = whisper.load_model("small")  # or "small", "medium"

def record_audio(filename, duration=5, fs=16000):
    print(f"🎙️ Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    scipy.io.wavfile.write(filename, fs, recording)
    print(f"✅ Saved to {filename}")

def transcribe_audio(filename):
    result = model.transcribe(filename)
    return result["text"]
if __name__=="__main__":
    record_audio("speech.wav", duration=5)
    print(transcribe_audio("speech.wav"))
