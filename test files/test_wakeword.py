
import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import sounddevice as sd
from modules.wakeword import WakeWordDetector

detector = WakeWordDetector()

print("Listening... Say Hey Jarvis")

def callback(indata, frames, time, status):
    audio = indata[:, 0]

    if detector.detect(audio):
        print("HEY JARVIS DETECTED!")

with sd.InputStream(
    channels=1,
    samplerate=16000,
    blocksize=1280,
    callback=callback
):
    while True:
        sd.sleep(1000)
