import ollama
import cv2


class VisionAI:

    def __init__(self, model="qwen3-vl:2b"):
        self.model = model
        print("Qwen Vision AI initialized.")

    def ask(self, image, question):

        if image is None:
            return "I can't see the image."

        success, encoded_image = cv2.imencode(
            ".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 85]
        )

        if not success:
            return "Unable to process image."

        image_bytes = encoded_image.tobytes()

        prompt = f"""
You are AVAQ, a concise visual assistant.

Question: {question}

Instructions:
- Answer in one short sentence.
- Maximum 20 words.
- Use simple English.
- Answer only the question.
- Do not provide internal reasoning.
- If uncertain, say so.
"""

        try:

            print("Sending image to Qwen...")

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [image_bytes]
                    }
                ],
                options={"temperature": 0.2, "num_predict": 512},
                think=False
            )

            # SDK response handling
            message = response.message

            answer = message.content

            print("Qwen content:", repr(answer))

            if not answer or not answer.strip():
                print("Full response:", response)
                return "Qwen returned an empty answer."

            return answer.strip()

        except Exception as e:

            print("QWEN ERROR:", repr(e))

            return "Qwen encountered an error."