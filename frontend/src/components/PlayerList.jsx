import { useState, useEffect } from 'react';
import api from '../services/api';
import './PlayerList.css';

function PlayerList({ onSelectPlayer }) {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState(null);
  const [loggingIn, setLoggingIn] = useState(false);

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getPlayers();
      setPlayers(data);
    } catch (err) {
      setError('Failed to load players. Please try again.');
      console.error('Error fetching players:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPlayer = (player) => {
    setSelectedPlayer(player);
    setPassword('');
    setLoginError(null);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    
    if (!password) {
      setLoginError('Password is required');
      return;
    }

    try {
      setLoggingIn(true);
      setLoginError(null);
      
      // Call login API
      const response = await api.loginPlayer({
        username: selectedPlayer.username,
        password: password
      });
      
      // Store token
      localStorage.setItem('token', response.access_token);
      
      // Pass player to parent
      onSelectPlayer(selectedPlayer);
    } catch (err) {
      if (err.response?.status === 401) {
        setLoginError('Incorrect password');
      } else {
        setLoginError('Login failed. Please try again.');
      }
      console.error('Login error:', err);
    } finally {
      setLoggingIn(false);
    }
  };

  const handleCancelLogin = () => {
    setSelectedPlayer(null);
    setPassword('');
    setLoginError(null);
  };

  if (loading) {
    return (
      <div className="player-list-container">
        <h2>Select Existing Player</h2>
        <div className="loading">Loading players...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="player-list-container">
        <h2>Select Existing Player</h2>
        <div className="error">{error}</div>
        <button onClick={fetchPlayers} className="btn-retry">
          Retry
        </button>
      </div>
    );
  }

  // Show login form if player is selected
  if (selectedPlayer) {
    return (
      <div className="player-list-container">
        <h2>Login as {selectedPlayer.username}</h2>
        <form onSubmit={handleLogin} className="login-form">
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              disabled={loggingIn}
              autoFocus
              required
            />
          </div>

          {loginError && <div className="error-message">{loginError}</div>}

          <div className="button-group">
            <button
              type="submit"
              className="btn-submit"
              disabled={loggingIn}
            >
              {loggingIn ? 'Logging in...' : 'Login'}
            </button>
            <button
              type="button"
              className="btn-cancel"
              onClick={handleCancelLogin}
              disabled={loggingIn}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    );
  }

  return (
    <div className="player-list-container">
      <h2>Select Existing Player</h2>
      {players.length === 0 ? (
        <p className="no-players">No players yet. Register a new player below!</p>
      ) : (
        <div className="player-grid">
          {players.map((player) => (
            <div
              key={player.id}
              className="player-card"
              onClick={() => handleSelectPlayer(player)}
            >
              <div className="player-avatar">
                {player.username.charAt(0).toUpperCase()}
              </div>
              <div className="player-info">
                <h3>{player.username}</h3>
                <p className="player-email">{player.email}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PlayerList;

// Made with Bob
