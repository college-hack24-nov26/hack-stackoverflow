import sys
from pathlib import Path

# Project root ko Python path mein add karo
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.tts import TextToSpeech

tts = TextToSpeech()

tts.speak("Hello! I am AVAQ. I can see two people in the room.")