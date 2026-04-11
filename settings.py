from faster_whisper import WhisperModel
import pvporcupine
import pyaudio
# ================== SETTINGS ==================
ACCESS_KEY = "/nJOsIk+S58a5d5VDAshf9LzMs4422wJALLkl8+otvtj5AIM3SS9kA=="
WAKE_WORD_FILE = "iris.ppn"

WHISPER_MODEL = "base.en"   # or "tiny.en" or  "base.en" 
SAMPLE_RATE = 16000
RECORD_SECONDS = 4          # command length
# ==============================================

# Load Whisper
whisper = WhisperModel(
    WHISPER_MODEL,
    device="cuda",
    compute_type="float16"  # GPU accelerated on RTX 3050
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