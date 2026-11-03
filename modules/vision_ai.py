import ollama
import cv2


class VisionAI:

    def __init__(self, model="qwen3-vl:2b"):

        self.model = model

        print("Qwen Vision AI initialized.")

    def ask(self, image, question):

        if image is None:
            return "I cannot access the camera image."

        success, encoded_image = cv2.imencode(
            ".jpg",
            image,
            [cv2.IMWRITE_JPEG_QUALITY, 85]
        )

        if not success:
            return "Unable to process camera image."

        image_bytes = encoded_image.tobytes()

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": question,
                    "images": [image_bytes]
                }
            ]
        )

        return response["message"]["content"]