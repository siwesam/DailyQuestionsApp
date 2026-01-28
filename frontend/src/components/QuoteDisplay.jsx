import { useState, useEffect } from 'react';
import api from '../services/api';
import './QuoteDisplay.css';

function QuoteDisplay({ playerId }) {
  const [quote, setQuote] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [progressSteps, setProgressSteps] = useState([]);

  useEffect(() => {
    fetchQuoteWithProgress();
  }, [playerId]);
  
  const addProgressStep = (message) => {
    setProgressSteps(prev => [...prev, { message, timestamp: Date.now() }]);
  };

  const fetchQuoteWithProgress = async () => {
    try {
      setLoading(true);
      setError(null);
      setProgressSteps([]);
      addProgressStep('Starting quote search...');
      console.log('Fetching quote with progress for player:', playerId);
      
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      // Use regular API without AI (faster)
      // SSE with AI is too slow, so we'll use simple keyword matching
      try {
        addProgressStep('Loading quote...');
        const data = await api.getPersonalizedQuote(playerId, false); // use_ai=false
        console.log('Quote data received:', data);
        addProgressStep('Quote found!');
        setQuote(data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching quote:', err);
        if (err.response?.status === 404) {
          setError('Please answer some questions first to get a personalized quote.');
        } else {
          setError('Failed to load quote. Please try again.');
        }
        setLoading(false);
      }
      
    } catch (err) {
      console.error('Error fetching quote:', err);
      setError('Failed to load quote. Please try again.');
      setLoading(false);
    }
  };

  const handleGetNewQuote = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('Fetching random quote');
      const data = await api.getRandomQuote();
      console.log('Random quote data received:', data);
      // Add relevance_score of 0 for random quotes
      setQuote({ ...data, relevance_score: 0 });
    } catch (err) {
      console.error('Error fetching random quote:', err);
      setError('Failed to load quote. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="quote-container">
        <div className="loading">
          <div className="loading-spinner">✨</div>
          <div className="progress-steps">
            {progressSteps.map((step, index) => (
              <div key={step.timestamp} className="progress-step">
                <span className="step-icon">✓</span>
                <span className="step-message">{step.message}</span>
              </div>
            ))}
            {progressSteps.length === 0 && <p>Finding your perfect quote...</p>}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="quote-container">
        <div className="error-card">
          <p>{error}</p>
          <div className="action-buttons">
            <button onClick={fetchQuoteWithProgress} className="btn-retry">
              Try Again
            </button>
            <a href="/questions" className="btn-primary">
              Answer Questions
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="quote-container">
      <div className="quote-card">
        <div className="quote-icon">✨</div>
        <h2>Your Personalized Quote</h2>
        
        {quote && (
          <>
            <div className="quote-text">
              <p className="quote-content">"{quote.quote_text}"</p>
              <p className="quote-author">— {quote.author}</p>
            </div>

            <div className="quote-info">
              <div className="quote-category">
                <span className="label">Category:</span>
                <span className="value">{quote.category}</span>
              </div>
              <div className="match-score">
                <span className="label">
                  {quote.relevance_score > 0 ? 'Relevance Score:' : 'Random Quote'}
                </span>
                <span className="value">
                  {quote.relevance_score > 0 ? `${Math.round(quote.relevance_score * 100)}%` : '✨'}
                </span>
              </div>
            </div>

            {quote.keywords && (
              <div className="matching-keywords">
                <p className="keywords-label">Quote keywords:</p>
                <div className="keywords-list">
                  {quote.keywords.split(',').map((keyword, index) => (
                    <span key={index} className="keyword-tag">
                      {keyword.trim()}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="quote-actions">
              <button onClick={handleGetNewQuote} className="btn-secondary">
                Get Another Quote
              </button>
              <a href="/questions" className="btn-primary">
                Answer More Questions
              </a>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default QuoteDisplay;

// Made with Bob
