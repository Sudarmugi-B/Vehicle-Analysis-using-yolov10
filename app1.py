import streamlit as st
import cv2
import tempfile
import os
from detect import detect_vehicles
from count import count_vehicles
from speed import estimate_speed
from number_plate import detect_number_plate
from number_plate import initialize_ocr

def main():
    st.set_page_config(layout="wide")
    st.title("Video-Based Detection System")

    # Sidebar for task selection and input
    st.sidebar.header("Task Selection")
    task = st.sidebar.selectbox("Choose a task", ["Vehicle Detection", "Vehicle Counting", "Speed Estimation", "Number Plate Detection"])

    st.sidebar.header("Input Selection")
    input_type = st.sidebar.radio("Select input type", ["Video File", "RTSP Stream"])

    if input_type == "Video File":
        video_file = st.sidebar.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
    else:
        rtsp_url = st.sidebar.text_input("Enter RTSP URL")

    if st.sidebar.button("Run Task"):
        if input_type == "Video File" and video_file is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False) 
            tfile.write(video_file.read())
            process_video(tfile.name, task)
        elif input_type == "RTSP Stream" and rtsp_url:
            process_video(rtsp_url, task)

def process_video(video_path, task):
    cap = cv2.VideoCapture(video_path)
    
    # Display input video
    st.subheader("Input Video")
    input_video = st.empty()
    
    # Display output video
    st.subheader("Output Video")
    output_video = st.empty()

    # Display vehicle counts (for Vehicle Counting task)
    if task == "Vehicle Counting":
        count_display = st.empty()

    prev_frame = None
    total_in = 0
    total_out = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        input_video.image(frame, channels="BGR")

        if task == "Vehicle Detection":
            output_frame = detect_vehicles(frame)
        elif task == "Vehicle Counting":
            output_frame, class_counts, new_in, new_out = count_vehicles(frame, total_in, total_out)
            total_in += new_in
            total_out += new_out
            count_display.write(f"Total In: {total_in}, Total Out: {total_out}\nClass Counts: {class_counts}")
        elif task == "Speed Estimation":
            if prev_frame is not None:
                output_frame = estimate_speed(prev_frame, frame)
            else:
                output_frame = frame
        elif task == "Number Plate Detection":
            output_frame = detect_number_plate(frame)

        output_video.image(output_frame, channels="BGR")
        prev_frame = frame.copy()

    cap.release()

if __name__ == "__main__":
    main()