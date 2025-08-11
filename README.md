# MoodTunes – Real-Time Emotion-Based Music Recommendation

**Author:** Surpreet Kaur  
**Course:** EE250 Final Project  

## Overview
MoodTunes is a real-time emotion detection application that recommends and plays music based on the user’s mood. It uses a webcam image, DeepFace AI for emotion recognition, and the Spotify API to generate a playlist that matches the detected mood. The app can run on both a local computer and a Raspberry Pi (with minor dependency adjustments).

## How It Works
1. The user grants camera access through the web app.
2. A snapshot is taken and analyzed using DeepFace to detect emotions.
3. Based on the detected mood, the application selects and plays a corresponding Spotify playlist.
4. The user is redirected to log in to Spotify for authentication.

## Quick Start
1. **Clone the project:**
   ```bash
   git clone https://github.com/<your-username>/moodtunes.git
   cd moodtunes
   ```
   ## Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
   ## Install dependancies:
   ```bash
   pip install -r requirements.txt
   ```
   Create a .env file in the root folder with your Spotify credentials.
   Authorize your app in the Spotify developer dashboard (failure to do so may result in a “user not registered” error)

   ## Run the application:
   ```bash
   python mood_detector.py
   ```
   ## Open your browser and go to:
   ```bash
   python mood_detector.py
   ```

   ## Rules
   ```bash
   Must have Spotify Premium.
   Spotify must be open and actively playing before use.
   A webcam is required (note: built-in device cameras can sometimes be unreliable).
   ```

  ## Extra Notes
  ```bash
  On Raspberry Pi, performance may vary due to processing requirements. You can test locally by modifying the app’s runtime configuration.
  The requirements.txt file contains dependencies for both Mac and Raspberry Pi setups.
  ```

  ## Resources
  ```bash
  OpenCV
  DeepFace Documentation & Tutorials – Sefik Ilkin Serengil
  Spotipy Documentation
  Flask Documentation
  Spotify Developer Portal
  OpenCV Docs


   


