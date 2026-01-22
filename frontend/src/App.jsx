import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css';
import PlayerList from './components/PlayerList';
import PlayerRegistration from './components/PlayerRegistration';
import DailyQuestions from './components/DailyQuestions';
import AnswerHistory from './components/AnswerHistory';
import QuoteDisplay from './components/QuoteDisplay';

function App() {
  const [currentPlayer, setCurrentPlayer] = useState(null);

  // Load player from localStorage on mount
  useEffect(() => {
    const savedPlayer = localStorage.getItem('currentPlayer');
    if (savedPlayer) {
      setCurrentPlayer(JSON.parse(savedPlayer));
    }
  }, []);

  // Save player to localStorage when it changes
  useEffect(() => {
    if (currentPlayer) {
      localStorage.setItem('currentPlayer', JSON.stringify(currentPlayer));
    } else {
      localStorage.removeItem('currentPlayer');
    }
  }, [currentPlayer]);

  const handleLogout = () => {
    setCurrentPlayer(null);
  };

  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <div className="header-content">
            <h1>📝 Daily Questions App</h1>
            {currentPlayer && (
              <div className="user-info">
                <span>Welcome, {currentPlayer.username}!</span>
                <button onClick={handleLogout} className="btn-logout">
                  Logout
                </button>
              </div>
            )}
          </div>
          {currentPlayer && (
            <nav className="nav-menu">
              <Link to="/questions" className="nav-link">Daily Questions</Link>
              <Link to="/history" className="nav-link">My History</Link>
              <Link to="/quote" className="nav-link">Get Quote</Link>
            </nav>
          )}
        </header>

        <main className="app-main">
          <Routes>
            <Route 
              path="/" 
              element={
                currentPlayer ? (
                  <Navigate to="/questions" />
                ) : (
                  <div className="home-container">
                    <PlayerList onSelectPlayer={setCurrentPlayer} />
                    <PlayerRegistration onRegister={setCurrentPlayer} />
                  </div>
                )
              } 
            />
            <Route 
              path="/questions" 
              element={
                currentPlayer ? (
                  <DailyQuestions playerId={currentPlayer.id} />
                ) : (
                  <Navigate to="/" />
                )
              } 
            />
            <Route 
              path="/history" 
              element={
                currentPlayer ? (
                  <AnswerHistory playerId={currentPlayer.id} />
                ) : (
                  <Navigate to="/" />
                )
              } 
            />
            <Route 
              path="/quote" 
              element={
                currentPlayer ? (
                  <QuoteDisplay playerId={currentPlayer.id} />
                ) : (
                  <Navigate to="/" />
                )
              } 
            />
          </Routes>
        </main>

        <footer className="app-footer">
          <p>Reflect, Grow, and Get Inspired Daily 🌱</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;

// Made with Bob
