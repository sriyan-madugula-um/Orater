import cv2
from deepface import DeepFace
import streamlit as st
import requests
import os

# Function to download the video from the Flask server
def download_video(filename):
    FLASK_SERVER_URL = "http://localhost:5000/uploads"
    response = requests.get(f"{FLASK_SERVER_URL}/{filename}")

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        st.error(f"Failed to download {filename}: {response.status_code}")
        return None

def emotion_detection(filename):
    emotions = {'angry': 0, 'disgust': 0, 'fear': 0, 'sad': 0, 'happy': 0, 'surprise': 0, 'neutral': 0, 'no face': 0}
    VIDEOS_DIR = 'uploads'
    VIDEO_NAME = filename
    emotion_color_mapping = {
        'angry': (0, 0, 255),
        'disgust': (0, 0, 255),
        'fear': (0, 0, 255),
        'sad': (0, 0, 255),
        'happy': (0, 255, 0),
        'surprise': (0, 255, 0),
        'neutral': (128, 128, 128),
    }

    # Download the video from the Flask server
    downloaded_file = download_video(VIDEO_NAME)
    if downloaded_file is None:
        return {"error": "Failed to download the video."}

    video_path = os.path.join(VIDEOS_DIR, VIDEO_NAME)
    video_path_out = '{}_out.mp4'.format(video_path[:-4])

    cap = cv2.VideoCapture(video_path)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    ret, frame = cap.read()
    H, W, _ = frame.shape
    out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (W, H))

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    frame_count = 0

    while ret:
        if frame_count % frame_rate == 0:  # Process every second
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for x, y, w, h in faces:
                if w > 100:
                    try:
                        analyze = DeepFace.analyze(frame, actions=['emotion'], silent=True)
                        emotion = analyze[0]['dominant_emotion']
                        color = emotion_color_mapping.get(emotion)
                        img = cv2.rectangle(frame, (x, y), (x + w, y + w), color, 4)
                        cv2.putText(frame, emotion.upper(), (int(x), int(y - 10)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3, cv2.LINE_AA)
                        if emotion in emotions:
                            emotions[emotion] += 1
                        else:
                            emotions[emotion] = 1
                    except Exception as e:
                        print(f"Error analyzing face: {e}")
                        emotions["no face"] += 1
                else:
                    emotions["no face"] += 1

        out.write(frame)
        ret, frame = cap.read()
        frame_count += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return emotions

# Specify the video file you want to analyze
video_filename = 'recorded_video.webm'
print(emotion_detection(video_filename))
