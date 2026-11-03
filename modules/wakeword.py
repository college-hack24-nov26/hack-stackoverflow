from openwakeword.model import Model


class WakeWordDetector:

    def __init__(self):
        self.model = Model(
            wakeword_models=["hey_jarvis"],
            inference_framework="onnx"
        )

    def detect(self, audio):
        prediction = self.model.predict(audio)

        for score in prediction.values():
            if score > 0.35:
                return True

        return False