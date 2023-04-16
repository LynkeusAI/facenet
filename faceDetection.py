import cv2
import typing
import numpy as np
import mediapipe as mp

class MPFaceDetection:

    def __init__(
        self,
        model_selection: bool = 1,
        confidence: float = 0.01,
        mp_drawing_utils: bool = True,
        color: typing.Tuple[int, int, int] = (255, 255, 255),
        thickness: int = 2,
        ) -> None:

        self.mp_drawing_utils = mp_drawing_utils
        self.color = color
        self.thickness = thickness
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=model_selection, min_detection_confidence=confidence)

    def tlbr(self, frame: np.ndarray, mp_detections: typing.List) -> np.ndarray:

        detections = []
        frame_height, frame_width, _ = frame.shape
        for detection in mp_detections:
            height = int(detection.location_data.relative_bounding_box.height * frame_height)
            width = int(detection.location_data.relative_bounding_box.width * frame_width)
            left = max(0 ,int(detection.location_data.relative_bounding_box.xmin * frame_width))
            top = max(0 ,int(detection.location_data.relative_bounding_box.ymin * frame_height))

            detections.append([top, left, top + height, left + width])

        return np.array(detections)

    def __call__(self, frame: np.ndarray, return_tlbr: bool = False) -> np.ndarray:

        results = self.face_detection.process(frame)

        if return_tlbr:
            if results.detections:
                return self.tlbr(frame, results.detections)
            return []

        if results.detections:
            if self.mp_drawing_utils:
                # Draw face detections of each face using media pipe drawing utils.
                for detection in results.detections:
                    self.mp_drawing.draw_detection(frame, detection)
            
            else:
                # Draw face detections of each face using our own tlbr and cv2.rectangle
                for tlbr in self.tlbr(frame, results.detections):
                    cv2.rectangle(frame, tlbr[:2][::-1], tlbr[2:][::-1], self.color, self.thickness)

        return frame