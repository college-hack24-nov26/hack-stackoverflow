
import cv2
import keyboard
import time
import threading

from modules.camera import Camera, summarize_objects
from modules.audio import AudioRecorder
from modules.speech_recognition import SpeechRecognizer
from modules.vision_ai import VisionAI
from modules.tts import TextToSpeech

from pathlib import Path
from datetime import datetime


# Shared application state
state = {
    "running": True,
    "recording": False,
    "processing": False,
    "frame": None,
    "annotated_frame": None,
    "frame_id": 0,
    "detected_objects": []
}

lock = threading.Lock()


# -----------------------------------------
# YOLO BACKGROUND DETECTION
# -----------------------------------------
def yolo_worker(camera):

    last_frame_id = -1

    while state["running"]:


        with lock:
            if state["processing"]:
                time.sleep(0.05)
                continue
            frame = state["frame"]
            frame_id = state["frame_id"]

        if frame is None or frame_id == last_frame_id:
            time.sleep(0.005)
            continue

        last_frame_id = frame_id

        try:
            annotated, objects = camera.detect(frame)

            with lock:
                state["annotated_frame"] = annotated
                state["detected_objects"] = objects

        except Exception as e:
            print("YOLO Error:", e)


# -----------------------------------------
# AI QUESTION PROCESSING
# -----------------------------------------
def process_question(audio, image, objects_text, whisper, qwen, tts):

    try:

        print("\nTranscribing...")

        question = whisper.transcribe(audio)

        print("AVAQ HEARD:", question)

        if not question:
            print("No speech detected.")
            return

        print("\nQwen is analyzing...")

        answer = qwen.ask(
            image,
            question,
            objects_text=objects_text
        )

        print("\nAVAQ:", answer)

        tts.speak(answer)

    except Exception as e:
        print("AI Processing Error:", e)

    finally:

        with lock:
            state["processing"] = False

        print("\nAVAQ READY - Hold SPACE to speak.")

#### for history of captured images 
# -----------------------------------------
# SAVE CAMERA FRAME
# -----------------------------------------

def save_frame(image):

    history_dir = Path("history")
    history_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    # Timestamped history image
    history_path = history_dir / f"{timestamp}.jpg"

    # Latest captured image
    last_frame_path = history_dir / "last_frame.jpg"

    cv2.imwrite(str(history_path), image)
    cv2.imwrite(str(last_frame_path), image)

    print(f"Image saved: {history_path}")

    return history_path

# -----------------------------------------
# MAIN APPLICATION
# -----------------------------------------
def main():

    print("=" * 50)
    print("             AVAQ AI ASSISTANT")
    print("=" * 50)

    camera = Camera()
    camera_indexes = [0, 1]
    recorder = AudioRecorder()

    whisper = SpeechRecognizer(model_size="base")
    qwen = VisionAI(model="qwen3-vl:2b")
    tts = TextToSpeech()

    camera.start()

    cv2.namedWindow("AVAQ AI Assistant", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("AVAQ AI Assistant", 1000, 700)

    print("\n========== AVAQ CONTROLS ==========")
    print("HOLD SPACE : Ask AVAQ a question")
    print("C          : Switch camera")
    print("Q / ESC    : Exit AVAQ")
    print("=================================\n")

    # Start YOLO in background
    threading.Thread(
        target=yolo_worker,
        args=(camera,),
        daemon=True
    ).start()

    print("\nAVAQ READY")
    print("Hold SPACE to speak.")
    print("Release SPACE to submit.")
    print("Press Q to exit.")

    previous_space = False

    try:

        while state["running"]:

            # ---------------------------------
            # LIVE CAMERA
            # ---------------------------------
            frame = camera.get_frame()

            if frame is None:
                time.sleep(0.01)
                continue

            with lock:
                state["frame"] = frame.copy()
                state["frame_id"] += 1

                display_frame = state["annotated_frame"]
                processing = state["processing"]
                
            # Keep camera preview LIVE during Qwen processing
            if processing or display_frame is None:
                cv2.imshow("AVAQ AI Assistant", frame)
            else:
                cv2.imshow("AVAQ AI Assistant", display_frame)
                
            # # key = cv2.waitKey(1) & 0xFF

            # if key == ord("q") or key == 27:
            #     break


            # key = cv2.waitKey(1) & 0xFF
            # # QUIT AVAQ
            # # if key == ord("q") or key == 27:
            # #     break
            # # SWITCH CAMERA USING C
            # if key == ord("c"):
            #     current_index = camera.camera_index
            #     try:
            #         current_position = camera_indexes.index(current_index)
            #     except ValueError:
            #         current_position = 0
                
            #     next_position = (current_position + 1) % len(camera_indexes)
            #     next_index = camera_indexes[next_position]
                
            #     if camera.switch_camera(next_index):
            #         with lock:
            #             state["frame"] = None
            #             state["annotated_frame"] = None
            #             state["detected_objects"] = []
            #             state["frame_id"] += 1
            #         print(f"Active camera: {next_index}")


            # ---------------------------------
            # KEYBOARD CONTROLS
            # ---------------------------------
            key = cv2.waitKey(1) & 0xFF

            # QUIT AVAQ
            if key == ord("q") or key == 27:
                break

# SWITCH CAMERA USING C
            if key == ord("c"):
                current_index = camera.camera_index

                try:
                    current_position = camera_indexes.index(current_index)
                except ValueError:
                    current_position = 0

                next_position = (current_position + 1) % len(camera_indexes)
                next_index = camera_indexes[next_position]

                if camera.switch_camera(next_index):
                    with lock:
                        state["frame"] = None
                        state["annotated_frame"] = None
                        state["detected_objects"] = []
                        state["frame_id"] += 1

                    print(f"Active camera: {next_index}")





            # ---------------------------------
            # SPACEBAR RECORDING
            # ---------------------------------
            space_pressed = keyboard.is_pressed("space")

            # Start recording
            if space_pressed and not previous_space:

                with lock:
                    busy = state["processing"]

                if not busy:

                    recorder.start()
                    state["recording"] = True

                    print("\nListening...")

                else:

                    print("\nAVAQ is processing your previous question.")

            # Stop recording
            if not space_pressed and previous_space:

                if state["recording"]:

                    state["recording"] = False

                    audio = recorder.stop()

                    # Capture current live frame
                    
                    current_frame = frame.copy()
                    with lock:

                        objects_snapshot = list(state["detected_objects"])
                    objects_text = summarize_objects(objects_snapshot)
                    print("YOLO hint:", objects_text or "(nothing detected)")
                    
                    # Save captured image to history
                
                    save_frame(current_frame)

                    if audio is not None:

                        with lock:
                            state["processing"] = True

                        threading.Thread(
                            target=process_question,
                            args=(
                                audio,
                                current_frame,
                                objects_text,
                                whisper,
                                qwen,
                                tts
                            ),
                            daemon=True
                        ).start()

                    else:
                        print("No audio recorded.")

            previous_space = space_pressed

            time.sleep(0.005)

    except KeyboardInterrupt:

        print("\nStopping AVAQ...")

    finally:

        state["running"] = False

        if state["recording"]:
            recorder.stop()

        camera.stop()

        cv2.destroyAllWindows()

        print("AVAQ shutdown complete.")


if __name__ == "__main__":
    main()


