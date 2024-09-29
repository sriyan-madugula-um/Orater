import streamlit as st

# HTML and JavaScript for video/audio recording
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video and Audio Recording</title>
</head>
<body>

<h1>Record Video and Audio</h1>

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

        // Stop recording and send the video to the server
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
st.title("Video and Audio Recorder")
st.components.v1.html(html_code, height=600)