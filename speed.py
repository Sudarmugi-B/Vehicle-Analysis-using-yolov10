import cv2
import numpy as np
from helper import detect_objects, model
import sqlite3
from datetime import datetime

def estimate_speed(prev_frame, curr_frame, fps=30, ppm=8):  # Assuming 8 pixels per meter
    prev_detections = detect_objects(prev_frame)
    curr_detections = detect_objects(curr_frame)
    
    output_frame = curr_frame.copy()
    
    for curr_det in curr_detections:
        curr_center = ((curr_det[0] + curr_det[2]) / 2, (curr_det[1] + curr_det[3]) / 2)
        min_dist = float('inf')
        matching_prev_det = None
        
        for prev_det in prev_detections:
            prev_center = ((prev_det[0] + prev_det[2]) / 2, (prev_det[1] + prev_det[3]) / 2)
            dist = np.sqrt((curr_center[0] - prev_center[0])**2 + (curr_center[1] - prev_center[1])**2)
            
            if dist < min_dist and curr_det[5] == prev_det[5]:  # Same class
                min_dist = dist
                matching_prev_det = prev_det
        
        if matching_prev_det is not None:
            speed = (min_dist / ppm) / (1 / fps) * 3.6  # Convert to km/h
            
            # Determine color based on speed
            if speed < 30:
                color = (0, 255, 0)  
            elif speed < 60:
                color = (0, 255, 255)  
            else:
                color = (0, 0, 255)  
            
            # Draw bounding box
            x1, y1, x2, y2 = map(int, curr_det[:4])
            cv2.rectangle(output_frame, (x1, y1), (x2, y2), color, 2)
            
            # Display speed
            label = f"{speed:.1f} km/h"
            cv2.putText(output_frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    
    return output_frame