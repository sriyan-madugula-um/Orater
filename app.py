import os
from groq import Groq
from pydub import AudioSegment
import librosa
import numpy as np
import requests
from pyht import Client, TTSOptions, Format

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

# Initialize the Groq client
client = Groq(
  api_key="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"
)

def relevance_score(question, answer) -> int:
  chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        {
            "role": "user",
            "content": f"Question: {question}\nAnswer: {answer}\nIs this answer relevant to the question? Please provide a relevance score from 1 to 10. Your output should just be a number."
        }
    ],
    model="gemma2-9b-it",
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stop=None,
    stream=False,
  )
  
  return (int(chat_completion.choices[0].message.content))

def sup_strength_score(question, answer) -> int:
  chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        {
            "role": "user",
            "content": f"Question: {question}\nAnswer: {answer}\nHow strong are the arguments within the answer in answering the question? Please provide a suppositional strength score from 1 to 10. Your output should just be a number."
        }
    ],
    model="gemma2-9b-it",
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stop=None,
    stream=False,
  )
  
  return (int(chat_completion.choices[0].message.content))

    
def count_filler_words(text) -> int:
    # Define a list of common filler words
    filler_words = [
        "uh", "um", "like", "you know", "basically", "actually", 
        "literally", "so", "well", "just", "seriously", "right", 
        "probably", "kinda", "sorta", "I mean"
    ]
    filler_words = filler_words + [word + "..." for word in filler_words]
    print(filler_words)

    # Normalize the text to lowercase and split it into words
    words = text.lower().split()

    # Count the number of filler words in the text
    filler_count = sum(word in filler_words for word in words)
    print(filler_count)
    
    score = 10

    filler_percentage = (filler_count / len(words)) * 100 if len(words) > 0 else 0

    # Initialize score based on filler percentage
    if filler_percentage <= 5:
        score = 10
    elif filler_percentage <= 10:
        score = 9
    elif filler_percentage <= 12:
        score = 8
    elif filler_percentage <= 15:
        score = 7
    elif filler_percentage <= 17:
        score = 6
    elif filler_percentage <= 20:
        score = 5
    elif filler_percentage <= 25:
        score = 4
    elif filler_percentage <= 30:
        score = 3
    elif filler_percentage <= 35:
        score = 2
    else:
        score = 1
    
    return score


def speed_score(text: str, audio_length: float) -> int:
    ideal_speed = 150
    # audio length comes from a library, assuming in minutes
    words = text.lower().split()
    print(len(words))
    speed = len(words) / audio_length
    
    score = 10
    
    # Calculate the percentage difference from the ideal speed
    percentage_difference = abs((speed - ideal_speed) / ideal_speed)

    if speed > ideal_speed:
        # Penalize for speeds greater than ideal speed
        penalty = min(percentage_difference * 20, 10)  # Max penalty is 10
        score -= penalty
        
    elif speed < ideal_speed:
        # Apply a smaller penalty for speeds below ideal speed
        penalty = min(percentage_difference * 10, 5)  # Max penalty is 5
        score -= penalty
    
    # Ensure score is between 1 and 10
    print(speed)
    score = max(1, min(score, 10))
    
    return int(score)

def extract_audio_features(file_path):
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)
    
    # Extract features
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    # Get average pitch
    pitch_avg = np.mean(pitches[pitches > 0])
    
    # Calculate harmonic-to-noise ratio
    hnr = librosa.effects.hpss(y)[0]  # Harmonic component
    hnr_value = np.mean(20 * np.log10(np.mean(1 + hnr)))

    # Calculate tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    
    # Calculate root mean square energy
    rms = np.mean(librosa.feature.rms(y=y))

    # Extract MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfccs, axis=1)
    
    return {
        'average_pitch': pitch_avg,
        'hnr': hnr_value,
        'tempo': tempo,
        'rms_energy': rms,
        'mfcc_mean': mfcc_mean
    }

def compute_confidence_score(features) -> float:
    score = 10
    
    # Average pitch penalties
    if features['average_pitch'] < 300:
        score -= (300 - features['average_pitch']) / 300
    elif features['average_pitch'] > 1000:
        score -= (features['average_pitch'] - 1000) / 300
    
    # Harmonic-to-noise ratio adjustment
    if features['hnr'] < 10:
        score -= (10 - features['hnr']) / 10  # Arbitrary threshold for clarity
    
    # Tempo penalties
    if features['tempo'] < 60 or features['tempo'] > 180:
        score -= 0.8

    # RMS energy penalties
    if features['rms_energy'] < 0.05:
        score -= 0.8  # Example threshold
    
    # MFCC consistency assessment (example)
    if np.std(features['mfcc_mean']) > 2:  # Arbitrary threshold for variability
        score -= 0.8
    
    return max(1, min(10, score))

def obama(text):
    # Initialize PlayHT API with your credentials
  client = Client("mlBwhhZ2KrXQZLHFf2ltCR4Spe83", "54f215e81b7f44c5a55c0755e14b010f")

  # voices = client.listVoices()

  #   # Print the list of voices to find your specific cloned voice ID
  # id = None
  # for voice in voices:
  #       print(f"Voice Name: {voice['name']}, Voice ID: {voice['id']}, Gender: {voice['gender']}")
  #       if voice['name'] == 'Obama':
  #           id = voice['id']
            
  # url = "https://api.play.ht/api/v2/cloned-voices"

  # headers = {
  #     "accept": "application/json",
  #     "AUTHORIZATION": "54f215e81b7f44c5a55c0755e14b010f",
  #     "X-USER-ID": "mlBwhhZ2KrXQZLHFf2ltCR4Spe83"
  # }

  # response = requests.get(url, headers=headers)

  # print(response.text)


    # configure your stream
  options = TTSOptions(
        # this voice id can be one of our prebuilt voices or your own voice clone id, refer to the`listVoices()` method for a list of supported voices.
        voice="s3://voice-cloning-zero-shot/67d225d7-4887-4c61-a63d-33fc019aad84/original/manifest.json",

        # you can pass any value between 8000 and 48000, 24000 is default
        sample_rate=44_100,
      
        # the generated audio encoding, supports 'raw' | 'mp3' | 'wav' | 'ogg' | 'flac' | 'mulaw'
        format=Format.FORMAT_MP3,

        # playback rate of generated speech
        speed=0.8,
  )

    # start streaming!
  # text = "I've been working as an administrative assistant for two and a half years. My first job in the field was with Dorfshire Housing and my main responsibilities were organising and updating housing records for the local area. One of my greatest accomplishments was implementing an excel model to automate updates to the database. This saved a lot of time each month. After a year I moved to Barksdale Housing, a private company where I've been working as a senior administrative assistant. I oversee the records management there and I look after a team of two. I'm proud of the development of my leadership skills during that time and I'm thankful for the support of my current employer who helped with this. I understand from the job post that you need someone who could update your existing records management and help lead a team of four through the changes. I'm sure I'm sure that with my experience and creativity, I will be able to make positive changes for you."

  with open('output.mp3', 'wb') as f:
        for chunk in client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=options):
            f.write(chunk)


def main():
    # Specify the path to the audio file
    filename = download_video('recorded_video.webm') # Replace with your audio file!

    audio = AudioSegment.from_file(filename)
    length = len(audio) / 1000
    print(length)

    # Open the audio file
    with open(filename, "rb") as file:
        # Create a translation of the audio file
        translation = client.audio.translations.create(
          file=(filename, file.read()), # Required audio file
          model="whisper-large-v3", # Required model to use for translation
          prompt="Make sure filler words are included",  # Optional
          response_format="json",  # Optional
          temperature=0.0  # Optional
        )
    # Print the translation text
    print(translation.text)

    # Extract audio features
    features = extract_audio_features(filename)
    print(features)

    metrics = {}

    # Compute the confidence score
    confidence_score = compute_confidence_score(features)
    print(f"Confidence score: {confidence_score}")
    metrics["Confidence"] = confidence_score

    # Calculate the speed score
    text = translation.text
    speed = speed_score(text, length/60)
    print(f"Speed score: {speed}")
    metrics["Speed"] = speed

    # Calculate the filler word score
    filler_score = count_filler_words(text)
    print(f"Filler word score: {filler_score}")
    metrics["Filler score"] = filler_score

    # Ask a question to evaluate relevance
    question = "Tell me about yourself."
    relevance = relevance_score(question, text)
    print(f"Relevance score: {relevance}")
    metrics["Relevance score"] = relevance

    # Ask a question to evaluate suppositional strength
    strength = sup_strength_score(question, text)
    print(f"Suppositional strength score: {strength}")
    metrics["Suppositional strength score"] = strength

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are Barack Obama, the 44th president of the United States."
        },
        {
            "role": "user",
            "content": f"Rephrase the following text in the style of Barack Obama, make the text a stronger argument, remove filler words, keep the same word count, the same structure, and same meaning: {text}"
        }
    ],
    model="gemma2-9b-it",
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stop=None,
    stream=False,
    )
  
    obama_text = chat_completion.choices[0].message.content

    obama(obama_text)

    return metrics, obama_text

  

if __name__ == "__main__":
  main()