import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API methods that match backend endpoints exactly
const apiService = {
  // Players
  getPlayers: async () => {
    const response = await api.get('/api/players/');
    return response.data;
  },
  
  createPlayer: async (data) => {
    const response = await api.post('/api/players/', data);
    return response.data;
  },
  
  getPlayer: async (playerId) => {
    const response = await api.get(`/api/players/${playerId}`);
    return response.data;
  },
  
  loginPlayer: async (credentials) => {
    const response = await api.post('/api/players/login', credentials);
    return response.data;
  },
  
  // Questions
  getDailyQuestion: async (playerId) => {
    const response = await api.get(`/api/questions/random/${playerId}`);
    return response.data;
  },
  
  // Answers
  submitAnswer: async (playerId, data) => {
    // Backend expects player_id in the data, not in the URL
    const answerData = {
      player_id: playerId,
      ...data
    };
    const response = await api.post('/api/answers/', answerData);
    return response.data;
  },
  
  getAnswerHistory: async (playerId) => {
    const response = await api.get(`/api/answers/player/${playerId}`);
    return response.data;
  },
  
  // Quotes
  getPersonalizedQuote: async (playerId, useAi = false) => {
    const response = await api.get(`/api/quotes/match/${playerId}?use_ai=${useAi}`);
    return response.data;
  },
  
  getRandomQuote: async () => {
    const response = await api.get('/api/quotes/random');
    return response.data;
  },
};

export default apiService;
