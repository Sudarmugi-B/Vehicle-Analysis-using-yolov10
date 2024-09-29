import cv2
import numpy as np
from ultralytics import YOLO

# Load pre-trained YOLOv8n model
model = YOLO('vehicle_v10.pt')

def detect_objects(frame, classes=None):
    results = model(frame)
    if classes:
        return results[0].boxes.data[results[0].boxes.cls.cpu().numpy().astype(int) == classes].cpu().numpy()
    return results[0].boxes.data.cpu().numpy()

def draw_boxes(frame, detections, with_label=True):
    for detection in detections:
        x1, y1, x2, y2, conf, cls = detection
        if conf > 0.5:  # Confidence threshold
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            if with_label:
                label = f"{model.names[int(cls)]}: {conf:.2f}"
                cv2.putText(frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return frame

def estimate_speed(detection1, detection2, fps, ppm):
    # ppm: pixels per meter
    x1, y1, _, _, _, _ = detection1
    x2, y2, _, _, _, _ = detection2
    distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    meters = distance / ppm
    time = 1 / fps
    speed = meters / time * 3.6  # convert to km/h
    return speed