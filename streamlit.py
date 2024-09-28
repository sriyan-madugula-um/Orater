import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av

# Set the page title
st.title("Record Audio and Video")

# Define the video transformer class using recv() instead of transform()
class VideoTransformer(VideoTransformerBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")  # Convert the frame to an ndarray (as an image)
        return av.VideoFrame.from_ndarray(img, format="bgr24")  # Return the frame back

# Display live camera feed with streamlit-webrtc
st.header("Live Camera Feed")
webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

st.write("Press the button to start recording. Video will be displayed live above.")
st.write("Note: Audio capture is not supported natively in Streamlit. Use external tools or extensions.")