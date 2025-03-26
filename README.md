🎶 MoodTunes AI

MoodTunes AI is a full-stack web application that detects the mood of a user's input text using AI and generates a Spotify playlist that matches the mood.

✨ Features

🌈 Analyzes user input for emotional sentiment using Azure Text Analytics

🔍 Maps mood to a Spotify playlist using the Spotify API

🎷 Returns the most followed relevant playlist for an optimal experience

⚛️ React frontend + Flask backend

🔐 Secure token-based API access

🚀 Technologies Used

Frontend: React

Backend: Flask (Python)

AI Sentiment Analysis: Azure Cognitive Services

Music Recommendation: Spotify Web API

🧐 How It Works

User enters a text (e.g., “I'm feeling nostalgic”).

Backend analyzes sentiment via Azure Text Analytics.

Sentiment is mapped to a mood: happy, relaxed, or sad.

A Spotify playlist matching the mood is fetched.

The best playlist (based on follower count) is displayed in the frontend.

🔧 Setup Instructions

Backend

cd backend
python -m venv venv
venv\Scripts\activate   # or source venv/bin/activate on Mac/Linux
pip install -r requirements.txt
python app.py

Create a .env file in the backend/ folder with:

AZURE_KEY=your_azure_key
AZURE_ENDPOINT=your_azure_endpoint
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

Frontend

cd frontend
npm install
npm start

🛡️ Security

Secrets are stored securely in environment variables.

Backend uses the Client Credentials Flow to fetch a valid Spotify token.

📚 Future Features

🎭 More detailed mood classification (e.g., nostalgic, confident)

🗨️ Voice input support

🔄 Shuffle or refresh playlist

📱 Responsive mobile design

📜 License

This project is for educational/demo purposes and is not intended for production use.
