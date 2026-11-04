import cv2
from ultralytics import YOLO
from pathlib import Path


class Camera:

    def __init__(self, camera_index=0):

        self.camera_index = camera_index

        model_path = Path("models/yolo26n.pt")

        if not model_path.exists():
            raise FileNotFoundError(
                f"YOLO model not found: {model_path}"
            )

        print("Loading YOLO26...")

        self.model = YOLO(str(model_path))

        self.cap = None

    def start(self):

        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Unable to open webcam")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("Camera started.")

    def get_frame(self):

        success, frame = self.cap.read()

        if not success:
            return None

        return frame

    def switch_camera(self, camera_index):
        print(f"\nSwitching to camera {camera_index}...")
        new_cap = cv2.VideoCapture(camera_index)
        if not new_cap.isOpened():
            new_cap.release()
            print(f"Cannot open camera {camera_index}")
            return False
        new_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        new_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        old_cap = self.cap
        self.cap = new_cap
        self.camera_index = camera_index
        
        if old_cap is not None:
            old_cap.release()

        print(f"Camera switched to index {camera_index}")
        return True

    def detect(self, frame):

        results = self.model.predict(
            frame,
            imgsz=640,
            conf=0.35,
            verbose=False
        )

        annotated_frame = results[0].plot()

        detected_objects = []

        for box in results[0].boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            name = self.model.names[class_id]

            detected_objects.append({
                "name": name,
                "confidence": confidence,
                "box": tuple(int(v) for v in box.xyxy[0].tolist())
            })

        return annotated_frame, detected_objects

    def stop(self):

        if self.cap is not None:
            self.cap.release()

        cv2.destroyAllWindows()


def summarize_objects(objects, frame_width=640):
    """Turn YOLO detections into a short text hint for Qwen."""
    if not objects:
        return ""

    groups = {}

    for obj in objects:
        x1, _, x2, _ = obj["box"]
        center = (x1 + x2) / 2 / frame_width

        if center < 0.33:
            position = "left"
        elif center < 0.66:
            position = "center"
        else:
            position = "right"

        groups.setdefault(obj["name"], []).append(position)

    parts = [
        f"{len(positions)} {name} ({', '.join(positions)})"
        for name, positions in groups.items()
    ]

    return "; ".join(parts)