import sounddevice as sd
import numpy as np


class AudioRecorder:

    def __init__(self, samplerate=16000):

        self.samplerate = samplerate
        self.stream = None
        self.audio_chunks = []

    def start(self):

        self.audio_chunks = []

        def callback(indata, frames, time_info, status):

            if status:
                print("Audio status:", status)

            self.audio_chunks.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=1,
            dtype="float32",
            blocksize=1024,
            callback=callback
        )

        self.stream.start()

        print("Recording started...")

    def stop(self):

        if self.stream is not None:

            self.stream.stop()
            self.stream.close()
            self.stream = None

        if not self.audio_chunks:
            return None

        audio = np.concatenate(
            self.audio_chunks,
            axis=0
        )

        return audio.flatten()