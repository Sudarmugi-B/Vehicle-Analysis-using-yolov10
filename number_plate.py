import cv2
import numpy as np
import imutils
import easyocr
import sqlite3
from datetime import datetime
from helper import detect_objects, draw_boxes

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def detect_number_plate(frame):
    detections = detect_objects(frame)
    output_frame = draw_boxes(frame, detections, with_label=False)
    
    conn = sqlite3.connect('video_detection.db')
    c = conn.cursor()
    
    for detection in detections:
        x1, y1, x2, y2, conf, cls = detection
        if conf > 0.5 and cls == 2:  # Assuming class 2 is for cars
            # Draw green bounding box for the vehicle
            cv2.rectangle(output_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            
            # Extract the region of interest (ROI)
            roi = frame[int(y1):int(y2), int(x1):int(x2)]
            
            # Process the ROI
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
            edged = cv2.Canny(bfilter, 30, 200)
            
            # Find contours
            keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(keypoints)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
            
            location = None
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 10, True)
                if len(approx) == 4:
                    location = approx
                    break
            
            if location is not None:
                # Create mask and crop image
                mask = np.zeros(gray.shape, np.uint8)
                new_image = cv2.drawContours(mask, [location], 0, 255, -1)
                new_image = cv2.bitwise_and(roi, roi, mask=mask)
                
                (x, y) = np.where(mask == 255)
                (topx, topy) = (np.min(x), np.min(y))
                (bottomx, bottomy) = (np.max(x), np.max(y))
                cropped_image = gray[topx:bottomx+1, topy:bottomy+1]
                
                # Perform OCR
                result = reader.readtext(cropped_image)
                
                if result:
                    text = result[0][-2]
                    
                    # Calculate the position of the number plate within the full frame
                    plate_x1 = int(x1) + topy
                    plate_y1 = int(y1) + topx
                    plate_x2 = int(x1) + bottomy
                    plate_y2 = int(y1) + bottomx
                    
                    # Draw red bounding box for the number plate
                    cv2.rectangle(output_frame, (plate_x1, plate_y1), (plate_x2, plate_y2), (0, 0, 255), 2)
                    
                    # Draw the plate text above the number plate bounding box
                    text_position = (plate_x1, plate_y1 - 10)
                    cv2.putText(output_frame, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
                    
                    # Save to database
                    c.execute("INSERT INTO number_plate (class, plate_text, timestamp) VALUES (?, ?, ?)",
                              ('car', text, datetime.now()))
    
    conn.commit()
    conn.close()
    
    return output_frame

# You may want to add this function to initialize EasyOCR only once
def initialize_ocr():
    global reader
    reader = easyocr.Reader(['en'])