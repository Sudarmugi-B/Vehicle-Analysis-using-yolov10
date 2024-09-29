import cv2
import numpy as np
from collections import defaultdict
from helper import detect_objects, model

def count_vehicles(frame, total_in, total_out, line_position=0.5):
    height, width = frame.shape[:2]
    line_y = int(height * line_position)
    
    detections = detect_objects(frame)
    output_frame = frame.copy()
    
    # Draw counting line
    cv2.line(output_frame, (0, line_y), (width, line_y), (0, 255, 255), 2)
    
    # Initialize counters
    class_counts = defaultdict(int)
    new_in = 0
    new_out = 0
    
    # Use a dictionary to track vehicle positions
    vehicle_positions = {}
    
    for detection in detections:
        x1, y1, x2, y2, conf, cls = detection
        if conf > 0.5:  # Confidence threshold
            center_y = (y1 + y2) / 2
            object_id = f"{int(cls)}_{int(x1)}_{int(y1)}"
            
            if object_id not in vehicle_positions:
                if center_y < line_y:
                    vehicle_positions[object_id] = "above"
                else:
                    vehicle_positions[object_id] = "below"
            else:
                prev_position = vehicle_positions[object_id]
                if prev_position == "above" and center_y > line_y:
                    new_in += 1
                    vehicle_positions[object_id] = "below"
                elif prev_position == "below" and center_y < line_y:
                    new_out += 1
                    vehicle_positions[object_id] = "above"
            
            # Draw bounding box
            cv2.rectangle(output_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            
            class_name = model.names[int(cls)]
            class_counts[class_name] += 1
    
    # Display counts on the frame
    y_offset = 30
    for class_name, count in class_counts.items():
        text = f"{class_name}: {count}"
        cv2.putText(output_frame, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        y_offset += 30
    
    # Display total in and out counts on the frame
    cv2.putText(output_frame, f"Total In: {total_in + new_in}", (width - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    cv2.putText(output_frame, f"Total Out: {total_out + new_out}", (width - 200, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    
    return output_frame, dict(class_counts), new_in, new_out