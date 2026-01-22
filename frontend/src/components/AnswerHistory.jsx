import { useState, useEffect } from 'react';
import api from '../services/api';
import './AnswerHistory.css';

function AnswerHistory({ playerId }) {
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnswers();
  }, [playerId]);

  const fetchAnswers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getAnswerHistory(playerId);
      setAnswers(data);
    } catch (err) {
      setError('Failed to load answer history. Please try again.');
      console.error('Error fetching answers:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="history-container">
        <h2>My Answer History</h2>
        <div className="loading">Loading your answers...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="history-container">
        <h2>My Answer History</h2>
        <div className="error-card">
          <p>{error}</p>
          <button onClick={fetchAnswers} className="btn-retry">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <h2>My Answer History</h2>
        <p className="answer-count">
          {answers.length} {answers.length === 1 ? 'answer' : 'answers'} recorded
        </p>
      </div>

      {answers.length === 0 ? (
        <div className="no-answers">
          <p>You haven't answered any questions yet.</p>
          <p>Start by answering today's questions!</p>
          <a href="/questions" className="btn-primary">
            Answer Questions
          </a>
        </div>
      ) : (
        <div className="answers-list">
          {answers.map((answer) => (
            <div key={answer.id} className="answer-card">
              <div className="answer-header">
                <span className="answer-category">{answer.question.category}</span>
                <span className="answer-date">{formatDate(answer.answered_at)}</span>
              </div>
              <div className="answer-question">
                <strong>Q:</strong> {answer.question.question_text}
              </div>
              <div className="answer-text">
                <strong>A:</strong> {answer.answer_text}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AnswerHistory;

// Made with Bob
