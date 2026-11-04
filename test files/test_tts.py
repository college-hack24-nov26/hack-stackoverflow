
import pyttsx3
import time

print("Initializing TTS...")

engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

print("Speaking 1...")
engine.say("Hello. This is AVAQ.")
engine.runAndWait()

time.sleep(1)

print("Speaking 2...")
engine.say("Second speech test.")
engine.runAndWait()

time.sleep(1)

print("Speaking 3...")
engine.say("Third speech test.")
engine.runAndWait()

print("TTS test completed.")
