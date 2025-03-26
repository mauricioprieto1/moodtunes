import React, { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [mood, setMood] = useState('');
  const [playlist, setPlaylist] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    setMood('');
    setPlaylist(null);

    try {
      // 1. Analyze the text
      const sentimentRes = await fetch('http://localhost:5000/analyze-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      const sentimentData = await sentimentRes.json();
      const detectedMood = sentimentData.mood;
      setMood(detectedMood);

      // 2. Get playlist
      const playlistRes = await fetch(`http://localhost:5000/get-playlist?mood=${detectedMood}`);
      const playlistData = await playlistRes.json();
      setPlaylist(playlistData);
    } catch (err) {
      console.error(err);
      alert('Something went wrong. Try again!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>MoodTunes AI 🎵</h1>

      <textarea
        placeholder="Type how you're feeling..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={4}
        cols={50}
      />
      <br />
      <button onClick={handleAnalyze} disabled={loading || !text}>
        {loading ? 'Analyzing...' : 'Generate Playlist'}
      </button>

      {mood && <p><strong>Mood detected:</strong> {mood}</p>}

      {playlist && (
        <div>
          <h2>{playlist.playlist_name}</h2>
          <img src={playlist.image} alt="Playlist cover" style={{ width: '300px' }} />
          <p>
            <a href={playlist.playlist_url} target="_blank" rel="noopener noreferrer">
              Listen on Spotify
            </a>
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
