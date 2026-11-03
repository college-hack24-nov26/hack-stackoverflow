import cv2


class Camera:

    def __init__(self, camera_index=0):

        self.camera_index = camera_index
        self.cap = None

    def start(self):

        self.cap = cv2.VideoCapture(
            self.camera_index
        )

        if not self.cap.isOpened():
            raise RuntimeError("Unable to open webcam")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("Camera started.")

    def get_frame(self):

        if self.cap is None:
            return None

        success, frame = self.cap.read()

        if not success:
            return None

        return frame

    def stop(self):

        if self.cap is not None:

            self.cap.release()
            self.cap = None

        cv2.destroyAllWindows()