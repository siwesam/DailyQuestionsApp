import { useState, useEffect } from 'react';
import api from '../services/api';
import './QuoteDisplay.css';

function QuoteDisplay({ playerId }) {
  const [quote, setQuote] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [progressMessage, setProgressMessage] = useState('');

  useEffect(() => {
    fetchQuoteWithProgress();
  }, [playerId]);

  const fetchQuoteWithProgress = async () => {
    try {
      setLoading(true);
      setError(null);
      setProgressMessage('Finding your perfect quote...');
      console.log('Fetching quote with progress for player:', playerId);
      
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      // Try SSE first, but with timeout fallback
      let sseTimeout;
      let eventSource;
      
      try {
        eventSource = new EventSource(`${API_BASE_URL}/api/quotes/match/${playerId}/stream`);
        
        // Set a timeout to fallback to regular API if SSE doesn't work
        sseTimeout = setTimeout(() => {
          console.log('SSE timeout, falling back to regular API');
          if (eventSource) {
            eventSource.close();
          }
          fetchQuoteFallback();
        }, 3000); // 3 second timeout
        
        eventSource.onmessage = (event) => {
          try {
            clearTimeout(sseTimeout); // Clear timeout on first message
            const data = JSON.parse(event.data);
            console.log('Progress update:', data);
            
            if (data.error) {
              setError(data.error);
              setLoading(false);
              eventSource.close();
            } else if (data.status === 'complete' && data.quote) {
              setQuote(data.quote);
              setLoading(false);
              setProgressMessage('');
              eventSource.close();
            } else if (data.message) {
              setProgressMessage(data.message);
            }
          } catch (err) {
            console.error('Error parsing SSE data:', err);
          }
        };
        
        eventSource.onerror = (err) => {
          console.error('EventSource error:', err);
          clearTimeout(sseTimeout);
          eventSource.close();
          // Fallback to regular API
          fetchQuoteFallback();
        };
        
      } catch (sseErr) {
        console.error('SSE not supported or failed:', sseErr);
        clearTimeout(sseTimeout);
        // Fallback to regular API
        fetchQuoteFallback();
      }
      
    } catch (err) {
      console.error('Error fetching quote:', err);
      setError('Failed to load quote. Please try again.');
      setLoading(false);
      setProgressMessage('');
    }
  };
  
  const fetchQuoteFallback = async () => {
    try {
      console.log('Using fallback API');
      setProgressMessage('Loading quote...');
      const data = await api.getPersonalizedQuote(playerId);
      console.log('Quote data received:', data);
      setQuote(data);
      setLoading(false);
      setProgressMessage('');
    } catch (err) {
      console.error('Error fetching quote:', err);
      if (err.response?.status === 404) {
        setError('Please answer some questions first to get a personalized quote.');
      } else {
        setError('Failed to load quote. Please try again.');
      }
      setLoading(false);
      setProgressMessage('');
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
          <p>{progressMessage || 'Finding your perfect quote...'}</p>
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
            <button onClick={fetchQuote} className="btn-retry">
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
