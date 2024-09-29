import streamlit as st
import pandas as pd
import altair as alt
import sys
sys.path.append(r'C:\Users\hrwan\OneDrive\Documents\GitHub\PublicSpeaking')
from detect_emotion import emotion_detection
from app import main as metrics

emotes = emotion_detection('recorded_video.webm')
metricals, obamtext = metrics()

totalemote = 0
for i in emotes:
  totalemote += emotes[i]

# Function to display a metric with a score
def display_metric(name, score):
    # Set the color based on the score
    if isinstance(score, list):
        score = sum(score) / len(score)  # Calculate average if score is a list

    if score <= 3:
        color = "#FF0000"  # Pastel Red
    elif score <= 6:
        color = "#FFFF00"  # Pastel Yellow
    else:
        color = "#00FF00"  # Pastel Green
    
    # Calculate the stroke-dasharray value based on the score
    circumference = 2 * 3.14159 * 45  # 2 * pi * radius (radius is 45)
    dasharray = (score / 10) * circumference

    # HTML/CSS to create a circular progress indicator with animation
    metric_html = f"""
    <div class="metric-container" style="text-align: center; margin: 10px;">
        <h4 style="text-align: center; color: #C1BFB5;">{name}</h4>
        <div class="metric-circle" style="display: inline-block; transition: transform 0.3s ease, box-shadow 0.3s ease;">
            <svg width="100" height="100" viewBox="0 0 100 100" style="transform: rotate(-90deg);">
                <circle cx="50" cy="50" r="45" stroke="#011638" stroke-width="10" fill="none" />
                <circle cx="50" cy="50" r="45" stroke="{color}" stroke-width="10" fill="none"
                        stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}"
                        style="transition: stroke-dashoffset 2s ease; stroke-dashoffset: {circumference - dasharray};" />
            </svg>
            <div style="position: relative; top: -70px; color: #C1BFB5; font-size: 20px;">
                {score}
            </div>
        </div>
    </div>
    """
    return metric_html

# Custom function to create a subheader with a specific color
def custom_subheader(text, color="#C1BFB5"):
    st.markdown(f'<h2 style="color:{color};">{text}</h2>', unsafe_allow_html=True)

custom_subheader("Transcript")
# Display the transcript text with custom color
transcript_text = metricals['Text']

st.markdown(f'<p style="color:#C1BFB5;">{transcript_text}</p><br><br>', unsafe_allow_html=True)

custom_subheader("Confidence")
# Display the line chart for the "Confidence" metric
confidence_scores = metricals['Confidence']
confidence_df = pd.DataFrame(confidence_scores, columns=["Confidence"])

# Create a new column for scaled times
length = metricals['Length']
confidence_df['ScaledTime'] = pd.Series(range(0, length + 1, length // (len(confidence_scores) - 1)))

# Create an Altair chart with labels
line_chart = alt.Chart(confidence_df).mark_line(point=True).encode(
    x=alt.X('ScaledTime:Q', title='Time'),
    y=alt.Y('Confidence:Q', title='Confidence'),
    color=alt.value('white'),
    tooltip=['ScaledTime', 'Confidence']
).properties(
    width=600,
    height=400
)

# Add text labels to the points
text = line_chart.mark_text(
    align='left',
    baseline='middle',
    dx=0,
    dy=-10
).encode(
    text='Confidence:Q'
)

st.altair_chart(line_chart + text, use_container_width=True)

custom_subheader("Other Metrics")
# Displaying metrics
metrics = {
    "Speed": metricals['Speed'],
    "Filler Words": metricals['Filler score'],
    "Relevancy": metricals['Relevance score'],
    "Suppositional Strength": metricals['Suppositional strength score'],
    "Professionalism": min(10, ((emotes['neutral'] + emotes['happy'])*10)//totalemote + 4)
}

# Use columns for layout
cols = st.columns(3)  # Create 3 columns for the first row

# Loop through the first three metrics and display them in columns
for i, (metric_name, score) in enumerate(list(metrics.items())[:3]):
    with cols[i]:  # Distribute metrics evenly across the columns
        st.markdown(display_metric(metric_name, score), unsafe_allow_html=True)

# Create columns for the second row with empty columns on the sides to center the metrics
cols = st.columns([1, 2,2, 1])  # Create 5 columns with equal width

# Loop through the remaining metrics and display them in the center columns
for i, (metric_name, score) in enumerate(list(metrics.items())[3:]):
    with cols[i + 1]:  # Place metrics in the center columns
        st.markdown(display_metric(metric_name, score), unsafe_allow_html=True)
st.markdown('<br><br><br><br>', unsafe_allow_html=True)

custom_subheader("How would Obama say it?")
st.audio("output.mp3")

st.write(obamtext)