from pyht import Client, TTSOptions, Format

def obama():
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
        speed=1,
  )

    # start streaming!
  text = "I've been working as an administrative assistant for two and a half years. My first job in the field was with Dorfshire Housing and my main responsibilities were organising and updating housing records for the local area. One of my greatest accomplishments was implementing an excel model to automate updates to the database. This saved a lot of time each month. After a year I moved to Barksdale Housing, a private company where I've been working as a senior administrative assistant. I oversee the records management there and I look after a team of two. I'm proud of the development of my leadership skills during that time and I'm thankful for the support of my current employer who helped with this. I understand from the job post that you need someone who could update your existing records management and help lead a team of four through the changes. I'm sure I'm sure that with my experience and creativity, I will be able to make positive changes for you."

  with open('output.mp3', 'wb') as f:
        for chunk in client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=options):
            f.write(chunk)