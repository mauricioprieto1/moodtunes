# 🎶 MoodTunes AI

MoodTunes AI is a full-stack web application that detects a user's mood from either text **or images** using Azure AI and recommends a matching Spotify playlist.

## ✨ Features

- 🌈 Analyzes user input for emotional sentiment using **Azure Text Analytics**  
- 🖼️ Extracts image tags using **Azure Computer Vision API** to infer mood or theme  
- 🔍 Maps detected mood or tags to relevant Spotify playlists  
- 📊 Selects the most followed playlist for optimal results  
- ⚛️ React frontend + Flask backend  
- 🔐 Secure token-based API access

## 🚀 Technologies Used

- **Frontend**: React  
- **Backend**: Flask (Python)  
- **Text Mood Analysis**: Azure Text Analytics API  
- **Image Analysis**: Azure Computer Vision API  
- **Music Recommendation**: Spotify Web API

## 🧐 How It Works

### Text-based Mood Detection:
1. User enters a phrase (e.g., “I'm feeling nostalgic”).  
2. Backend analyzes sentiment using Azure Text Analytics.  
3. Sentiment is mapped to a general mood: `happy`, `relaxed`, or `sad`.  
4. The app fetches the most followed playlist matching the mood.

### Image-based Mood Detection:
1. User provides an image URL.  
2. Azure Vision API extracts tags from the image.  
3. Tags are mapped to predefined music themes (e.g., `car` → `roadtrip`).  
4. A relevant Spotify playlist is returned based on the theme.

## 🔧 Setup Instructions

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # or source venv/bin/activate on Mac/Linux
pip install -r requirements.txt
python app.py
```

Create a `.env` file in the `backend/` folder with:
```env
AZURE_KEY=your_azure_key
AZURE_ENDPOINT=your_azure_endpoint
AZURE_VISION_KEY=your_vision_key
AZURE_VISION_ENDPOINT=your_vision_endpoint
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 🛡️ Security

- Secrets are stored securely in environment variables.  
- Backend uses Spotify's Client Credentials Flow to retrieve access tokens.

## 📚 Future Features

- 🎭 More nuanced emotion detection (e.g., nostalgic, excited)  
- 🗨️ Voice input support  
- 🔄 Shuffle or refresh playlist feature  
- 🌐 Public user-shared playlists  
- 🎨 Improved user interface and animations  
- 🔐 Authentication and user accounts  
- 📲 Social sharing to send playlists to friends or post on social media

## 📜 License

This project is for educational/demo purposes and is not intended for production use.
