import React, { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [mood, setMood] = useState('');
  const [tag, setTag] = useState('');
  const [playlist, setPlaylist] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyzeText = async () => {
    setLoading(true);
    setMood('');
    setPlaylist(null);

    try {
      const sentimentRes = await fetch('http://localhost:5000/analyze-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      const sentimentData = await sentimentRes.json();
      const detectedMood = sentimentData.mood;
      setMood(detectedMood);

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

  const handleImagePlaylist = async () => {
    setLoading(true);
    setTag('');
    setPlaylist(null);

    try {
      const res = await fetch('http://localhost:5000/image-to-playlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_url: imageUrl }),
      });

      const data = await res.json();
      if (data.error) {
        alert(data.error);
      } else {
        setTag(data.tag_detected);
        setPlaylist(data);
      }
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

      {/* TEXT ANALYSIS */}
      <textarea
        placeholder="Type how you're feeling..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={4}
        cols={50}
      />
      <br />
      <button onClick={handleAnalyzeText} disabled={loading || !text}>
        {loading ? 'Analyzing...' : 'Generate Playlist from Mood'}
      </button>

      <hr style={{ margin: '30px 0' }} />

      {/* IMAGE ANALYSIS */}
      <input
        type="text"
        placeholder="Paste image URL (e.g., from Unsplash)"
        value={imageUrl}
        onChange={(e) => setImageUrl(e.target.value)}
        style={{ width: '400px' }}
      />
      <br />
      <button onClick={handleImagePlaylist} disabled={loading || !imageUrl}>
        {loading ? 'Analyzing image...' : 'Generate Playlist from Image'}
      </button>

      <br /><br />

      {/* OUTPUTS */}
      {mood && <p><strong>Mood detected:</strong> {mood}</p>}
      {tag && <p><strong>Tag detected from image:</strong> {tag}</p>}

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
