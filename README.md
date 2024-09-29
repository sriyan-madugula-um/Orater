# Orater: An AI-powered public speaking coach with feedback from some of the world's best orators.

# Inspiration
Public speaking is the biggest fear for over 75% of people - including us. No matter how good your technical skills may be, success is hard to achieve if you fumble interviews or struggle presenting to a crowd (ask us how we know). If only there were a way to receive coaching from the best of the best...

# What it does
Orater takes in a public speaking prompt and records a video of the user giving their public speaking response, then provides metrics (some statistical, e.g. speed, filler words, etc.) as well AI-powered analysis such as relevancy, suppositional strength, and confidence from input audio and video.

Orater displays these metrics on a Streamlit dashboard, and the prompts the user to select a master of public speaking to be their AI coach, e.g. Barack Obama. The AI coach 

# How we built it

We used Streamlit for our frontend to display our metric and emotion information visually appealing charts and line graphs, showcasing summary information and metrics over time. We want the user to have access to as much of our analysis as possible, and we realized that Streamlit was strong in displaying this data visualization.

We used Flask for our backend server, storing the video and audio files after the user records a video. 

We then called the Groq API for analyzing our audio, converting speech to text, and calculating metrics on speed, filler words used, relevancy, and suppositional strength. We used the Librosa Python library to analyze audio and calculate a confidence score over time, taking into consideration the user's pitch, tone, and rhythm. 

We also used the DeepFace library to run emotion detection on the video, categorizing a score on happiness, fear, disgust, sadness, and other emotions based on the user's video. 

Overall, our Flask backend does analysis on the video, audio, and text from the user recording and displays the data visually on our Streamlit frontend.

# Challenges we ran into

This was our first time using Streamlit for frontend. It wasn't a huge learning curve since it was fairly intuitive to pick up, but it took us some time to integrate it appropriately with our video recording tool and the Flask backend.

Once we got the integrations running, we had to find specific API's and libraries for our textual, audio, and video analysis. Since it was multimodal, we had to spend a lot of time finding appropriate libraries and making sure our code was compatible with their API access. This also took a significant amount of time and research as we had to read through quite a bit of documentation.

# Accomplishments that we're proud of

One of the most exciting features is the ability to select a master public speaker, such as Barack Obama, as a virtual AI coach. This innovation helps users learn from the best by comparing their performance with renowned public figures. Even though the current version only supports one voice due to API limitations, the foundation is set for adding many more iconic voices in the future.

We implemented AI analysis that provides real-time feedback on the user’s public speaking skills, from speech pace to confidence level and emotion detection. Integrating the Groq API for speech-to-text conversion and analysis was complex but rewarding. This enabled us to give users actionable insights into their speaking performance in ways that typical public speaking apps don’t.

The most significant achievement was successfully integrating multimodal analysis into a single workflow. Handling video, audio, and text data simultaneously and feeding the results back into our Streamlit dashboard was challenging, but we managed to ensure that the entire process runs smoothly. By leveraging tools like DeepFace for emotion analysis and Librosa for audio metrics, we were able to provide comprehensive feedback to users.

# What we learned

One particularly valuable aspect of the project was learning how to structure the Flask backend to efficiently manage client-server communication, including handling errors and returning status codes for different outcomes. Additionally, we learned how to integrate third-party APIs and manage static files and templates in Flask. We were able to implement features like uploading files, handling user input, and returning dynamic data, all while maintaining a clean, functional backend.

# What's next for Orater

We plan on adding more voices to our Celebrity comparison tool. It currently only supports Barack Obama because our PlayHT API only supports one cloned voice on the free tier. We can very easily expand this API to other voices featuring prominent celebrities and well-known public speakers (both contemporary and older) like Oprah Winfrey, Winston Churchill, Ronald Reagan, and more.

We also hope to decrease loading time, further utilizing Streamlit caching and using lazy loading to optimize data loading only when it is needed. Since we're analyzing text, audio, and video, performance for larger videos can be an issue. This is something we plan to improve for Orater in the future. 