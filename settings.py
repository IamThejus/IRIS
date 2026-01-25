from faster_whisper import WhisperModel
import pvporcupine
import pyaudio
# ================== SETTINGS ==================
ACCESS_KEY = "9N0aoPuDnlrN0wLoh4qzVmxfyeDnVJJXLIoQ91Sg2T+OIiu3VGtC4A=="
WAKE_WORD_FILE = "iris.ppn"

WHISPER_MODEL = "base.en"   # or "tiny.en" or  "base.en" 
SAMPLE_RATE = 16000
RECORD_SECONDS = 4          # command length
# ==============================================

# Load Whisper
whisper = WhisperModel(
    WHISPER_MODEL,
    device="cpu",
    compute_type="int8"   # IMPORTANT for Pi 4
)

# Load Porcupine
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