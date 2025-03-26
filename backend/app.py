from dotenv import load_dotenv
from flask import Flask, request, jsonify

import os
import requests
import base64


load_dotenv()

AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")


app = Flask(__name__)

def get_spotify_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    if response.status_code != 200:
        raise Exception("Failed to get Spotify token")
    

    token = response.json()["access_token"]
    print("Token: ", token)

    return token

@app.route('/')
def home():
    return jsonify({"message": "MoodTunes AI backend is running!"})

@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    user_input = request.json.get('text')

    if not user_input:
        return jsonify({"error": "No text provided"}), 400

    url = AZURE_ENDPOINT + "text/analytics/v3.1/sentiment"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "documents": [
            {
                "id": "1",
                "language": "en",
                "text": user_input
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        result = response.json()
        sentiment = result["documents"][0]["sentiment"]

        # Map sentiment to music mood
        sentiment_to_mood = {
            "positive": "happy",
            "neutral": "relaxed",
            "negative": "sad"
        }
        mood = sentiment_to_mood.get(sentiment, "relaxed")

        return jsonify({"mood": mood})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/get-playlist', methods=['GET'])
def get_playlist():
    mood = request.args.get('mood', 'happy')  # default mood

    token = get_spotify_token()

    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": mood,
        "type": "playlist",
        "limit": 5
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    playlists = data.get("playlists", {}).get("items", [])

    if not playlists:
        return jsonify({"error": "No playlists found"}), 404

    playlist = playlists[0]
    return jsonify({
        "playlist_name": playlist["name"],
        "playlist_url": playlist["external_urls"]["spotify"],
        "image": playlist["images"][0]["url"]
    })

    


if __name__ == '__main__':
    app.run(debug=True)