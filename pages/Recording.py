import streamlit as st


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
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'recorded_video.webm';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a); // Remove the temporary anchor element
            console.log("Video automatically downloaded");

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
