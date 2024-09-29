import streamlit as st
import sys
sys.path.append(r'C:\Users\hrwan\OneDrive\Documents\GitHub\PublicSpeaking')
from detect_emotion import emotion_detection
from app import main as metrics

# HTML and JavaScript for video/audio recording
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video and Audio Recording</title>
    <style>
        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }
        body {
            text-align: center;
        }
        .inline-element {
            display: inline-block; /* Ensures elements remain inline */
            margin-bottom: 20px;   /* Adds 20px of vertical space */
        }

        .mainTitle {
            font-size: 65px;
            color: #8eb1c7;
            font-family: 'Abolition', sans-serif;
            white-space: nowrap;
            width: 0;
            overflow: hidden;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 10px; 
            animation: typing 2.5s steps(40, end);
            animation-fill-mode: forwards;
        }

        /* Add margin to ensure buttons are visible and not overlapped by the video */
        video {
            margin-bottom: 20px; /* Add space below the video */
        }

        /* Style buttons */
        button {
            padding: 10px 20px;
            margin: 10px;
            font-size: 16px;
            background-color: #4CAF50; /* Green background */
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049; /* Darker green on hover */
        }
    </style>
</head>
<body>
<h1 class="mainTitle">Record Your Speech</h1>

<!-- Video element for live preview -->
<video id="preview" controls autoplay style="width: 100%; max-width: 640px;"></video>
<br/>


<!-- Buttons to start and stop recording -->
<button id="startButton">Start Recording</button>
<button id="stopButton">Stop Recording</button>

<script>
let mediaRecorder;
let recordedChunks = [];
let stream;

// Get user media
navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(function(userStream) {
        stream = userStream; // Save stream to stop later
        // Preview the stream
        document.getElementById('preview').srcObject = stream;

        // Create a MediaRecorder instance
        mediaRecorder = new MediaRecorder(stream);

        // Handle data availability
        mediaRecorder.ondataavailable = function(event) {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        // Stop recording and create the download link
        mediaRecorder.onstop = function() {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });

            // Create a form to send the blob to the server
            const formData = new FormData();
            formData.append("file", blob, "recorded_video.webm");

            // Send the video to the Flask server
            const xhr = new XMLHttpRequest();
            xhr.open("POST", "http://localhost:5000/upload", true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    console.log("Video successfully uploaded.");
                } else {
                    console.error("Failed to upload video.");
                }
            };
            xhr.send(formData);
            
            // Stop the media stream and end the video preview
            stream.getTracks().forEach(track => track.stop());
            document.getElementById('preview').srcObject = null;
            console.log("Video preview stopped");
        };
    })
    .catch(function(error) {
        console.error("Error accessing media devices.", error);
    });

// Start recording function
document.getElementById('startButton').onclick = function() {
    recordedChunks = []; // Clear previous recordings
    mediaRecorder.start();
    console.log("Recording started");
};

// Stop recording function
document.getElementById('stopButton').onclick = function() {
    mediaRecorder.stop();
    console.log("Recording stopped");
};
</script>

</body>
</html>
"""

# Streamlit app
st.components.v1.html(html_code, height=800)

if st.button('Display Metrics: '):
    emotes = emotion_detection('recorded_video.webm')
    metricals, obamtext = metrics()
    st.write(f'Happiness is: ', {emotes['happy']})
    st.write(metricals)
    st.write(obamtext)
    st.audio('output.mp3')
