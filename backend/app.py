from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import requests
import base64

#import the tags
from tag_mapping import TAG_TO_THEME, DEFAULT_THEME


load_dotenv()

AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")


app = Flask(__name__)
CORS(app)

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
    mood = request.args.get('mood', 'happy')

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

    print("Spotify API response:")
    print(data)

    all_playlists = data.get("playlists", {}).get("items", [])
    valid_playlists = [p for p in all_playlists if p is not None]

    if not valid_playlists:
        return jsonify({"error": "No valid playlist returned"}), 500

    # New logic to find playlist with most followers
    best_playlist = None
    max_followers = -1

    for playlist in valid_playlists:
        playlist_id = playlist["id"]
        details_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        detail_res = requests.get(details_url, headers=headers)
        if detail_res.status_code != 200:
            continue
        detail_data = detail_res.json()
        followers = detail_data.get("followers", {}).get("total", 0)
        if followers > max_followers:
            max_followers = followers
            best_playlist = detail_data

    if not best_playlist:
        return jsonify({"error": "No playlist with follower data found"}), 500

    return jsonify({
        "playlist_name": best_playlist["name"],
        "playlist_url": best_playlist["external_urls"]["spotify"],
        "image": best_playlist["images"][0]["url"]
    })


@app.route('/image-to-playlist', methods=['POST'])
def image_to_playlist():
    image_url = request.json.get('image_url')

    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    vision_endpoint = os.getenv("AZURE_VISION_ENDPOINT") + "vision/v3.2/analyze"
    vision_key = os.getenv("AZURE_VISION_KEY")

    headers = {
        "Ocp-Apim-Subscription-Key": vision_key,
        "Content-Type": "application/json"
    }

    params = {
        "visualFeatures": "Tags"
    }

    body = {
        "url": image_url
    }

    try:
        response = requests.post(vision_endpoint, headers=headers, params=params, json=body)
        result = response.json()

        tags = [tag["name"] for tag in result.get("tags", [])]

        print("Image Tags:", tags)

        

        # Prioritize tags that match your mapping
        mapped_keywords = [TAG_TO_THEME[tag] for tag in tags if tag in TAG_TO_THEME]


        # Use the first mapped keyword, or fallback to 'vibes'
        keyword = mapped_keywords[0] if mapped_keywords else DEFAULT_THEME



        # Now fetch playlist from Spotify like before
        token = get_spotify_token()
        url = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "q": keyword,
            "type": "playlist",
            "limit": 5
        }

        res = requests.get(url, headers=headers, params=params)
        playlists = res.json().get("playlists", {}).get("items", [])
        playlists = [p for p in playlists if p is not None]

        if not playlists:
            return jsonify({"error": "No playlists found"}), 404

        best = playlists[0]
        return jsonify({
            "tag_detected": keyword,
            "tags": tags,
            "playlist_name": best["name"],
            "playlist_url": best["external_urls"]["spotify"],
            "image": best["images"][0]["url"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)