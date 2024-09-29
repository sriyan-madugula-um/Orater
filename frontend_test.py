import streamlit as st
import requests
import os

# Specify the Flask server URL
FLASK_SERVER_URL = "http://localhost:5000"

def download_video(filename):
    # Send a GET request to retrieve the video file
    response = requests.get(f"{FLASK_SERVER_URL}/uploads/{filename}")

    if response.status_code == 200:
        # Save the file locally
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        st.error(f"Failed to download {filename}: {response.status_code}")
        return None

def main():
    st.title("Video Downloader from Flask Server")

    # Input for the filename
    filename = st.text_input("Enter the video filename (e.g., recorded_video.webm):")

    if st.button("Download Video"):
        if filename:
            downloaded_file = download_video(filename)
            if downloaded_file:
                st.success(f"Downloaded {downloaded_file} successfully.")
                st.video(downloaded_file)  # Display the video

                # Optionally, provide a download link
                st.download_button(
                    label="Download Video",
                    data=open(downloaded_file, 'rb').read(),
                    file_name=downloaded_file,
                    mime="video/webm"
                )
        else:
            st.warning("Please enter a filename.")

if __name__ == "__main__":
    main()

