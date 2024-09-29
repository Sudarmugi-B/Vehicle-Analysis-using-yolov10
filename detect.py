import cv2
from helper import detect_objects, draw_boxes
import sqlite3
from datetime import datetime

def detect_vehicles(frame):
    detections = detect_objects(frame)
    output_frame = draw_boxes(frame, detections)
    
    # Save detections to database
    conn = sqlite3.connect('video_detection.db')
    c = conn.cursor()
    for detection in detections:
        _, _, _, _, _, cls = detection
        c.execute("INSERT INTO detection (class, timestamp) VALUES (?, ?)",
                  (cls, datetime.now()))
    conn.commit()
    conn.close()
    
    return output_frame