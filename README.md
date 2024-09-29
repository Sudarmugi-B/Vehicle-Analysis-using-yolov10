# Vehicle-Analysis-using-yolov10
A comprehensive vehicle analysis system that performs vehicle detection, counting, speed estimation, and number plate detection using video input.

## Table of Contents
- [Features](#features)
- [Components](#components)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)

## Features

- Vehicle detection with bounding boxes
- Vehicle counting by type (e.g., car, truck, bike)
- Vehicle speed estimation
- Number plate detection and recognition
- Support for multiple input formats (video file, YouTube URL, RTSP stream)
- Streamlit web interface for easy interaction
- SQLite database for storing detection results

## Components

- Task selection: Choose between vehicle detection, counting, speed estimation, and number plate detection
- Input options: Upload video, provide YouTube URL, or RTSP stream link
- Drag and drop interface for input
- Run task button
- Input video display (top right of the webpage)
- Output video display (right below input video)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Sudarmugi-B/Vehicle-Analysis-using-yolov10
   cd video-based-detection-system
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```
   python setup_database.py
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Select a task, choose an input method, and upload or provide the video source

4. Click the "Run Task" button to start the analysis

5. View the results in real-time on the webpage

## How It Works

1. **Vehicle Detection**: Displays detected vehicles with bounding boxes and shows the count of each vehicle type on top of the video.
2. **Vehicle Counting**: Processes the entire video and displays the final count of each vehicle type. Saves the count to the database once the video is fully processed.
3. **Speed Estimation**: Shows the speed of each vehicle above its bounding box in the output video.
4. **Number Plate Detection**: Displays bounding boxes around detected number plates with the recognized text above each box.

All tasks display the input video at the top right of the webpage and the output video below it.

## Project Structure

- `app.py`: Main Streamlit user interface
- `helper.py`: Contains the machine learning model and utility functions
- `detect.py`: Implements vehicle detection functionality
- `count.py`: Handles vehicle counting logic
- `speed.py`: Manages speed estimation calculations
- `number_plate.py`: Processes number plate detection and recognition
- `setup_database.py`: Sets up the SQLite database structure
- `requirements.txt`: Lists all Python dependencies

## Database Schema

The SQLite database contains the following tables:

1. Detection: `id, class, timestamp`
2. Counting: `id, class, count, timestamp`
3. Speed: `id, class, speed, timestamp`
4. NumberPlate: `id, class, plate_text, timestamp`

## Contributing

We welcome contributions to improve the Vehicle-Analysis-using-yolov10. Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a pull request

