import cv2
import keyboard
import time

from modules.camera import Camera
from modules.audio import AudioRecorder
from modules.speech_recognition import SpeechRecognizer
from modules.vision_ai import VisionAI
from modules.tts import TextToSpeech


def main():

    print("=" * 50)
    print("              AVAQ AI ASSISTANT")
    print("=" * 50)

    camera = Camera()
    recorder = AudioRecorder()
    whisper = SpeechRecognizer(model_size="base")
    qwen = VisionAI(model="qwen3-vl:2b")
    tts = TextToSpeech()

    camera.start()

    print("\nAVAQ READY")
    print("Hold SPACE to speak.")
    print("Release SPACE to submit your question.")
    print("Press ESC to exit.")

    recording = False
    previous_space_state = False

    try:

        while True:

            # Continuously capture webcam frames
            frame = camera.get_frame()

            if frame is None:
                continue

            # Display live camera
            cv2.imshow("AVAQ AI Assistant", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                break

            # Detect SPACE press/release
            space_pressed = keyboard.is_pressed("space")

            # SPACE pressed
            if space_pressed and not previous_space_state:

                recording = True

                recorder.start()

                print("\nListening...")

            # SPACE released
            if not space_pressed and previous_space_state:

                if recording:

                    recording = False

                    # Stop recording
                    audio = recorder.stop()

                    print("\nRecording stopped.")

                    # Capture CURRENT webcam frame
                    current_frame = camera.get_frame()

                    if current_frame is None:
                        current_frame = frame

                    # Speech recognition
                    print("Transcribing...")

                    question = whisper.transcribe(audio)

                    print("\nYOU:", question)

                    if question:

                        # Send current frame + question to Qwen
                        print("\nQwen is analyzing the image...")

                        try:

                            answer = qwen.ask(
                                current_frame,
                                question
                            )

                            print("\nAVAQ:", answer)

                            # Speak response
                            tts.speak(answer)

                        except Exception as e:

                            print("Qwen error:", e)

                    else:

                        print("No speech detected.")

                    print("\nAVAQ READY")

            previous_space_state = space_pressed

            time.sleep(0.01)

    except KeyboardInterrupt:

        print("\nStopping AVAQ...")

    finally:

        if recording:
            recorder.stop()

        camera.stop()

        print("AVAQ shutdown complete.")


if __name__ == "__main__":
    main()