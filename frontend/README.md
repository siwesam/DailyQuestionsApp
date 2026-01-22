# Daily Question Frontend

React frontend for the Daily Question web application.

## Setup Instructions

### Option 1: Initialize with Vite (Recommended)

If this is your first time setting up the frontend:

```bash
# Navigate to frontend directory
cd frontend

# Initialize React project with Vite
npm create vite@latest . -- --template react

# When prompted:
# "Current directory is not empty. Remove existing files and continue?" → Yes

# Install dependencies
npm install

# Install additional required packages
npm install axios react-router-dom

# Start development server
npm run dev
```

The app will be available at http://localhost:5173

### Option 2: Use Existing Configuration

If package.json already exists:

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── PlayerForm.jsx
│   │   ├── QuestionCard.jsx
│   │   ├── QuoteDisplay.jsx
│   │   └── AnswerHistory.jsx
│   ├── services/
│   │   └── api.js          # API integration
│   ├── App.jsx             # Main app component
│   ├── main.jsx            # Entry point
│   └── index.css           # Global styles
├── package.json
├── vite.config.js
└── Dockerfile
```

## Building Components

### 1. Player Registration Component

Create `src/components/PlayerForm.jsx`:

```jsx
import { useState } from 'react';
import { playerAPI } from '../services/api';

function PlayerForm({ onPlayerCreated }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await playerAPI.create({ username, email });
      onPlayerCreated(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create player');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>
      {error && <div className="error">{error}</div>}
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Register'}
      </button>
    </form>
  );
}

export default PlayerForm;
```

### 2. Question Card Component

Create `src/components/QuestionCard.jsx`:

```jsx
import { useState } from 'react';
import { answerAPI } from '../services/api';

function QuestionCard({ question, playerId, onAnswerSubmitted }) {
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await answerAPI.create({
        player_id: playerId,
        question_id: question.id,
        answer_text: answer,
      });
      setAnswer('');
      onAnswerSubmitted();
    } catch (error) {
      console.error('Error submitting answer:', error);
      alert('Failed to submit answer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="question-card">
      <h2>{question.question_text}</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Type your answer here..."
          rows="5"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Submit Answer'}
        </button>
      </form>
    </div>
  );
}

export default QuestionCard;
```

### 3. Quote Display Component

Create `src/components/QuoteDisplay.jsx`:

```jsx
function QuoteDisplay({ quote }) {
  return (
    <div className="quote-display">
      <h2>Your Inspirational Quote</h2>
      <blockquote>
        <p>"{quote.quote_text}"</p>
        {quote.author && <footer>— {quote.author}</footer>}
      </blockquote>
      {quote.relevance_score > 0 && (
        <p className="match-info">
          This quote was matched to your answers with a relevance score of {quote.relevance_score.toFixed(1)}
        </p>
      )}
    </div>
  );
}

export default QuoteDisplay;
```

### 4. Answer History Component

Create `src/components/AnswerHistory.jsx`:

```jsx
import { useState, useEffect } from 'react';
import { answerAPI } from '../services/api';

function AnswerHistory({ playerId }) {
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnswers = async () => {
      try {
        const response = await answerAPI.getPlayerAnswers(playerId);
        setAnswers(response.data);
      } catch (error) {
        console.error('Error fetching answers:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnswers();
  }, [playerId]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="answer-history">
      <h2>Your Answer History</h2>
      {answers.length === 0 ? (
        <p>No answers yet. Start answering questions!</p>
      ) : (
        <div className="answers-list">
          {answers.map((answer) => (
            <div key={answer.id} className="answer-item">
              <h3>{answer.question.question_text}</h3>
              <p>{answer.answer_text}</p>
              <small>{new Date(answer.answered_at).toLocaleString()}</small>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AnswerHistory;
```

## Main App Component

Update `src/App.jsx`:

```jsx
import { useState, useEffect } from 'react';
import PlayerForm from './components/PlayerForm';
import QuestionCard from './components/QuestionCard';
import QuoteDisplay from './components/QuoteDisplay';
import AnswerHistory from './components/AnswerHistory';
import { questionAPI, quoteAPI } from './services/api';
import './App.css';

function App() {
  const [player, setPlayer] = useState(null);
  const [question, setQuestion] = useState(null);
  const [quote, setQuote] = useState(null);
  const [showHistory, setShowHistory] = useState(false);
  const [loading, setLoading] = useState(false);

  const fetchNewQuestion = async () => {
    if (!player) return;
    setLoading(true);
    try {
      const response = await questionAPI.getRandom(player.id);
      setQuestion(response.data);
      setQuote(null);
    } catch (error) {
      console.error('Error fetching question:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSubmitted = () => {
    const wantMore = window.confirm('Answer submitted! Do you want to answer another question?');
    if (wantMore) {
      fetchNewQuestion();
    } else {
      fetchQuote();
    }
  };

  const fetchQuote = async () => {
    setLoading(true);
    try {
      const response = await quoteAPI.getMatching(player.id);
      setQuote(response.data);
      setQuestion(null);
    } catch (error) {
      console.error('Error fetching quote:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePlayerCreated = (newPlayer) => {
    setPlayer(newPlayer);
    fetchNewQuestion();
  };

  return (
    <div className="App">
      <header>
        <h1>Daily Question</h1>
        {player && <p>Welcome, {player.username}!</p>}
      </header>

      <main>
        {!player && <PlayerForm onPlayerCreated={handlePlayerCreated} />}

        {player && !showHistory && (
          <>
            {loading && <div>Loading...</div>}
            {question && !loading && (
              <QuestionCard
                question={question}
                playerId={player.id}
                onAnswerSubmitted={handleAnswerSubmitted}
              />
            )}
            {quote && !loading && <QuoteDisplay quote={quote} />}
            <button onClick={() => setShowHistory(true)}>View History</button>
          </>
        )}

        {player && showHistory && (
          <>
            <AnswerHistory playerId={player.id} />
            <button onClick={() => setShowHistory(false)}>Back to Questions</button>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
```

## Styling

Add basic styles to `src/index.css`:

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 20px;
}

.App {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

h1 {
  color: #667eea;
  font-size: 2.5rem;
  margin-bottom: 10px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 400px;
  margin: 0 auto;
}

input, textarea {
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-size: 16px;
  transition: border-color 0.3s;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #667eea;
}

button {
  padding: 12px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background: #5568d3;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error {
  color: #e74c3c;
  padding: 10px;
  background: #fadbd8;
  border-radius: 5px;
}

.question-card, .quote-display, .answer-history {
  margin: 20px 0;
}

blockquote {
  font-size: 1.5rem;
  font-style: italic;
  padding: 20px;
  background: #f8f9fa;
  border-left: 4px solid #667eea;
  margin: 20px 0;
}

.answer-item {
  padding: 15px;
  margin: 10px 0;
  background: #f8f9fa;
  border-radius: 5px;
  border-left: 3px solid #667eea;
}

.answer-item h3 {
  color: #667eea;
  margin-bottom: 10px;
}

.answer-item small {
  color: #666;
}
```

## Environment Variables

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000/api
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Troubleshooting

### "Cannot find module"
```bash
npm install
```

### "Port 5173 already in use"
```bash
# Kill the process
lsof -ti:5173 | xargs kill

# Or change port in vite.config.js
```

### "Failed to fetch"
- Make sure backend is running on port 8000
- Check CORS settings in backend
- Verify API_URL in .env file

## Next Steps

1. Customize the styling to match your preferences
2. Add more features (authentication, social sharing, etc.)
3. Implement error boundaries
4. Add loading states and animations
5. Make it responsive for mobile devices

## Learn More

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Axios Documentation](https://axios-http.com/)