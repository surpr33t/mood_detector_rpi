Partners: Surpreet Kaur | Alan Yusuf 
EE250 Final Project 




Real Time Emotion Detector for Music Recommendation 


This application uses spotify API and deepface to host a small website. The website will take a photo of you after necessary permissions and then play music according to your 
percieved feeling. We use DeepFace AI to detect your emotions. Currently this can run on your local computer or alternatively on an rpi (where a few dependency changes are neccessary
that you'll see on the requirements file). The website will direct you to spotify to log in and play your music
Instructions : 


1. Clone the project
2. Open terminal and navigate to the project folder:
   cd mood_detector_rpi
3. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate
4. Install the required libraries:
   pip install -r requirements.txt
5. Create a `.env` file in the root folder with your Spotify credentials:
6. Make sure that you also authorize yourself in the user dashboard so     that you can actually make use of the script, you will most likely get user not registered error if not.
7. Run the app:
   python mood_detector.py
8. Open your browser and go to:
   http://127.0.0.1:5000


Rules : 
- Must have Spotify Premium
- Make sure Spotify is open and playing something before using the application
- Must have Webcam, local device cameras can get flimsy

Extra info:
-sometimes the necessary requirements are too heavy and process might appear too slow, if that is the case you can also test locally by changing where the app runs. the requirements file contains the downloads you need for mac alongside the rpi if you choose to do so


Resources : 
opencv.org
Sefik Ilkin Serengil (YouTube, DeepFace documentation and tutorials)
spotipy.readthedocs.io
flask.palletsprojects.com
developer.spotify.com
https://docs.opencv.org/4.x/index.html
ChatGPT for help with 2 functions as stated in the video