from dotenv import load_dotenv
import os
import spotipy
import json
import cv2
from spotipy.oauth2 import SpotifyOAuth
from deepface import DeepFace
from flask import Flask, session, redirect, request, url_for
from spotipy.exceptions import SpotifyException
import numpy as np

load_dotenv()   # reads .env into os.environ
print("SPOTIPY_REDIRECT_URI:", os.getenv("SPOTIPY_REDIRECT_URI"))

CLIENT_ID     = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SECRET_KEY    = os.getenv("SECRET_KEY")

EMOTION_PLAYLISTS = {
    "angry": "spotify:playlist:37i9dQZF1EIgNZCaOGb0Mi",
    "disgust": "spotify:playlist:37i9dQZF1E8KEaf5o7wGZB",
    "fear": "spotify:playlist:5A16Qc2yGTZnVPJGuWBYBN",
    "happy": "spotify:playlist:37i9dQZF1EIgG2NEOhqsD7",
    "sad": "spotify:playlist:37i9dQZF1EIg6gLNLe52Bd",
    "surprise": "spotify:playlist:37i9dQZF1E8P9e4WhpIhrd",   
    "neutral":  "spotify:playlist:4ADcSA8oePEucvwIOv5lzj"

}


app = Flask(__name__)
app.config.update(
    SECRET_KEY = SECRET_KEY,
    TESTING = True
)

def find_working_camera():
    for index in range(5):  # test indices 0-4
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret and frame is not None and frame.shape[0] > 0:
                print(f"✅ Found working camera at index {index}")
                return index
            else:
                print(f"⚠️ Camera {index} opened but returned no frame.")
        else:
            print(f"❌ Camera {index} could not be opened.")
    return None

def convert_numpy_types(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(i) for i in obj]
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-playback-state user-modify-playback-state streaming user-read-currently-playing",
        cache_path=None,  # No caching so each user logs in
        show_dialog=True
    )

def get_authorized(scope=None):
    sp_oauth = get_spotify_oauth()
    token_info = session.get("token_info", None)

    if not token_info:
        return redirect(url_for("login"))

    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info

    print("Granted scopes:", token_info.get("scope"))
    return spotipy.Spotify(auth=token_info["access_token"])


   
def preprocess_image(frame):
    # frame is BGR from cv2.VideoCapture
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(rgb, (800, 800))
    return img

def get_emotion(img):
    result = DeepFace.analyze(
        img,
        detector_backend="retinaface",
        actions=["emotion"],
        enforce_detection=False
    )
    if isinstance(result, list):
        result = result[0]

    # convert numpy values to Python native types
    cleaned_result = convert_numpy_types(result)
    print(" DeepFace raw result:", json.dumps(cleaned_result, indent=2))

    if "region" in cleaned_result:
        print("Face region detected:", cleaned_result["region"])
    else:
        print( " No face detected — fallback result likely")

    return cleaned_result["dominant_emotion"]


def play_4_emotion(sp, emotion):
    # 1) Print account product (“premium” vs “free”)
    try:
        me = sp.current_user()
        print("Spotify account product:", me.get("product", "<unknown>"))
    except SpotifyException as e:
        print(" Failed to fetch account info:", e)

    # 2) Fetch & print devices
    try:
        devices_resp = sp.devices()
        devices = devices_resp.get("devices", [])
        print("Available devices:")
        for d in devices:
            print(f"   • {d.get('name')} (id={d.get('id')}, type={d.get('type')})")
    except SpotifyException as e:
        # in case of 403 error
        print(" Failed to fetch devices:", e)
        return "Could not retrieve Spotify devices. Check your account or app settings.", 403

    #  No devices check
    if not devices:
        msg = "No active Spotify devices found. Start Spotify on one of your devices."
        print("info: ", msg)
        return msg, 404

    #  play music
    playlist_uri = EMOTION_PLAYLISTS.get(emotion)
    device_id = devices[0]["id"]
    sp.start_playback(device_id=device_id, context_uri=playlist_uri)
    return None, None  # signal “no error”


@app.route("/login")
def login():
    session.clear()  # this is critical
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    
    return redirect(auth_url)

@app.route("/callback")
def callback():
    sp_oauth = get_spotify_oauth()
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code, as_dict=True)
    session["token_info"] = token_info
    return redirect(url_for("detect_and_play"))


@app.route("/detect_and_play", methods=['POST', 'GET'])
def detect_and_play():
    camera_index = find_working_camera()
    if camera_index is None:
        return " No working camera found", 500

    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Image Processing Error", 500

    img = preprocess_image(frame)
    cv2.imwrite("debug_last_frame.jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    print("📸 Saved debug frame as debug_last_frame.jpg")
    emotion = get_emotion(img)

    sp = get_authorized(scope="user-read-playback-state user-modify-playback-state")
    play_4_emotion(sp, emotion)

    return f"Detected emotion: {emotion}. Playing corresponding Spotify playlist.", 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)