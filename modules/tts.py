
import queue
import threading
import pyttsx3


class TextToSpeech:

    def __init__(self, rate=175):
        self.rate = rate
        self.q = queue.Queue()

        self.worker = threading.Thread(
            target=self._worker,
            daemon=True
        )
        self.worker.start()

    def _worker(self):

        try:
            import pythoncom
            pythoncom.CoInitialize()
        except ImportError:
            pass

        while True:

            text = self.q.get()

            if text is None:
                self.q.task_done()
                break

            try:
                engine = pyttsx3.init("sapi5")
                engine.setProperty("rate", self.rate)
                engine.setProperty("volume", 1.0)

                engine.say(text)
                engine.runAndWait()

                engine.stop()
                del engine

            except Exception as e:
                print("TTS Error:", e)

            finally:
                self.q.task_done()

    def speak(self, text):

        if text:
            print("AVAQ SPEAKING:", text)
            self.q.put(text)
