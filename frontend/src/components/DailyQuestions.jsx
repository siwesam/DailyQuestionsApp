import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './DailyQuestions.css';

function DailyQuestions({ playerId }) {
  const navigate = useNavigate();
  const successTimeoutRef = useRef(null);
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [noMoreQuestions, setNoMoreQuestions] = useState(false);

  useEffect(() => {
    fetchQuestion();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playerId]);

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (successTimeoutRef.current) {
        clearTimeout(successTimeoutRef.current);
      }
    };
  }, []);

  const fetchQuestion = async () => {
    try {
      setLoading(true);
      setError(null);
      setSuccess(false);
      setNoMoreQuestions(false);
      const data = await api.getDailyQuestion(playerId);
      setQuestion(data);
      setAnswer('');
    } catch (err) {
      if (err.response?.status === 404) {
        setNoMoreQuestions(true);
        setQuestion(null);
      } else {
        setError('Failed to load question. Please try again.');
        console.error('Error fetching question:', err);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!answer.trim()) {
      setError('Please provide an answer');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await api.submitAnswer(playerId, {
        question_id: question.id,
        answer_text: answer.trim()
      });
      setSuccess(true);
      setAnswer('');
      // Don't auto-hide success message - let user choose what to do
    } catch (err) {
      setError('Failed to submit answer. Please try again.');
      console.error('Error submitting answer:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerMore = () => {
    // Clear any pending timeout
    if (successTimeoutRef.current) {
      clearTimeout(successTimeoutRef.current);
    }
    setSuccess(false);
    fetchQuestion();
  };

  const handleSkip = () => {
    // Skip current question and load a new one
    fetchQuestion();
  };

  const handleFinish = () => {
    // Clear any pending timeout
    if (successTimeoutRef.current) {
      clearTimeout(successTimeoutRef.current);
    }
    navigate('/quote');
  };

  if (loading && !question) {
    return (
      <div className="questions-container">
        <div className="loading">Loading question...</div>
      </div>
    );
  }

  if (noMoreQuestions) {
    return (
      <div className="questions-container">
        <div className="no-questions-card">
          <h2>🎉 All Done!</h2>
          <p>You've answered all available questions for today.</p>
          <p>Come back tomorrow for more questions, or get your personalized quote!</p>
          <button onClick={handleFinish} className="btn-primary">
            Get My Quote
          </button>
        </div>
      </div>
    );
  }

  if (error && !question) {
    return (
      <div className="questions-container">
        <div className="error-card">
          <p>{error}</p>
          <button onClick={fetchQuestion} className="btn-retry">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="questions-container">
      <div className="question-card">
        <div className="question-header">
          <h2>Today's Question</h2>
          {question && (
            <span className="question-category">{question.category}</span>
          )}
        </div>

        {question && (
          <>
            <div className="question-text">
              <p>{question.question_text}</p>
            </div>

            {success ? (
              <div className="success-message">
                <h3>✅ Answer Submitted!</h3>
                <p>Would you like to answer another question?</p>
                <div className="action-buttons">
                  <button onClick={handleAnswerMore} className="btn-secondary">
                    Answer More Questions
                  </button>
                  <button onClick={handleFinish} className="btn-primary">
                    Finish & Get Quote
                  </button>
                </div>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="answer-form">
                <div className="form-group">
                  <label htmlFor="answer">Your Answer</label>
                  <textarea
                    id="answer"
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    placeholder="Type your answer here..."
                    rows="6"
                    disabled={loading}
                    required
                  />
                </div>

                {error && <div className="error-message">{error}</div>}

                <div className="form-actions">
                  <button
                    type="submit"
                    className="btn-submit"
                    disabled={loading || !answer.trim()}
                  >
                    {loading ? 'Submitting...' : 'Submit Answer'}
                  </button>
                  <button
                    type="button"
                    onClick={handleSkip}
                    className="btn-skip"
                    disabled={loading}
                  >
                    Skip Question
                  </button>
                </div>
              </form>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default DailyQuestions;

// Made with Bob
