import pyttsx3
import queue
import threading


class TextToSpeech:

    def __init__(self, rate=175):
        self.rate = rate
        self.q = queue.Queue()
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except ImportError:
            pass

        engine = pyttsx3.init()
        engine.setProperty("rate", self.rate)
        engine.setProperty("volume", 1.0)

        while True:
            text = self.q.get()
            if text is None:
                break
            engine.say(text)
            engine.runAndWait()

    def speak(self, text):
        if text:
            print("AVAQ:", text)
            self.q.put(text)