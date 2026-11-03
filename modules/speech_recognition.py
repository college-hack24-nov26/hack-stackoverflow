from faster_whisper import WhisperModel
import numpy as np


class SpeechRecognizer:

    def __init__(self, model_size="base"):

        print("Loading Faster Whisper...")

        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

        print("Whisper ready.")

    def transcribe(self, audio):

        if audio is None or len(audio) == 0:
            return ""

        segments, info = self.model.transcribe(
            audio.astype(np.float32),
            beam_size=3,
            vad_filter=True
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text.strip()