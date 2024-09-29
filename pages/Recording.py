import streamlit as st
import streamlit.components.v1 as components

st.markdown("""
<style>
body {
    backgroundColor: blue;   
    text-align: center;
    text-color: white;

}

@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}

.mainTitle {
    font-size: 75px;
    color: #8eb1c7;
    font-family: 'Abolition', sans-serif;
    white-space: nowrap; /* Prevent text from wrapping */
    width: 0;
    overflow: hidden; /* Hide the text until it is revealed */
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 10; /* Remove default bottom margin */
    animation: typing 2.5s steps(40, end);
    animation-fill-mode: forwards; /* Keep the final state after animation ends */
    text-align: center;
}

.description {
    font-size: 25px;
    color: #c1bfb5;
    font-family: 'Abolition', sans-serif;
    white-space: nowrap;
    width: 0;
    overflow: hidden;
    margin-left: auto;
    margin-right: auto;
    animation: typing 3.5s steps(60, end);
    animation-delay: 2.5s; /* Delay description animation until title finishes */
    animation-fill-mode: forwards;
    text-align: center;
}
.button{
    background-color: #364156;
    color: white;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
}
button[kind="primary"] {
    color: white !important; /* Text color */
    background-color: #364156 !important; /* Button background color */
    border: none !important;
    border-radius: 5px !important;
    padding: 10px 20px !important;
    font-size: 16px !important;
    cursor: pointer !important;
    transition: background-color 0.3s ease !important;
}

button[kind="primary"]:hover {
    color: #ffcc00 !important; /* Text color on hover */
    background-color: #555 !important; /* Background color on hover */
}

button[kind="primary"]:active {
    color: white !important; /* Text color when clicked */
    background-color: #4CAF50 !important; /* Background color when clicked */
}
</style>
""", unsafe_allow_html=True)



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
            background-color: #364156; /* Green background */
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #555; /* Darker green on hover */
        }
    </style>
</head>
<body>
<h1 class="mainTitle">Record Your Speech</h1>

<!-- Video element for live preview -->
<video id="preview" controls autoplay muted style="width: 100%; max-width: 640px;"></video>
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

pressed = st.button("Go to Metrics")

if pressed:
    st.switch_page("pages/Metrics.py")