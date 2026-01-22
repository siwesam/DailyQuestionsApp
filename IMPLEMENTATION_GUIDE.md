# Implementation Guide - Daily Question Web App

## Prerequisites

Before starting implementation, ensure you have:

- Python 3.9 or higher installed
- Node.js 16+ and npm/yarn installed
- PostgreSQL 13+ installed (or Docker)
- Git for version control
- Code editor (VS Code recommended)
- Basic knowledge of Python, JavaScript, and SQL

## Phase 1: Backend Setup

### Step 1: Project Structure

Create the following directory structure:

```
DummyPythonApp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── players.py
│   │   │   ├── questions.py
│   │   │   ├── answers.py
│   │   │   └── quotes.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── quote_matcher.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_players.py
│   │   ├── test_questions.py
│   │   └── test_answers.py
│   ├── alembic/
│   │   └── versions/
│   ├── requirements.txt
│   ├── .env.example
│   ├── .env
│   ├── alembic.ini
│   └── init_db.py
├── frontend/
├── docker-compose.yml
├── .gitignore
├── README.md
├── PLAN.md
└── ARCHITECTURE.md
```

### Step 2: Dependencies (requirements.txt)

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
alembic==1.12.1
python-multipart==0.0.6
```

### Step 3: Configuration (config.py)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Step 4: Database Models (models.py)

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Float, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base

class Player(Base):
    __tablename__ = "players"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    answers = relationship("Answer", back_populates="player", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    answered_at = Column(DateTime, default=datetime.utcnow)
    answer_date = Column(Date, default=datetime.utcnow().date, index=True)
    
    player = relationship("Player", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    quote_matches = relationship("AnswerQuote", back_populates="answer")

class Quote(Base):
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    quote_text = Column(Text, nullable=False)
    author = Column(String(100))
    category = Column(String(50))
    keywords = Column(Text)  # Comma-separated keywords
    created_at = Column(DateTime, default=datetime.utcnow)
    
    answer_matches = relationship("AnswerQuote", back_populates="quote")

class AnswerQuote(Base):
    __tablename__ = "answer_quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, ForeignKey("answers.id"), nullable=False)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)
    relevance_score = Column(Float, default=0.0)
    matched_at = Column(DateTime, default=datetime.utcnow)
    
    answer = relationship("Answer", back_populates="quote_matches")
    quote = relationship("Quote", back_populates="answer_matches")
```

### Step 5: Pydantic Schemas (schemas.py)

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

# Player Schemas
class PlayerBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None

class Player(PlayerBase):
    id: UUID
    created_at: datetime
    last_active: datetime
    
    class Config:
        from_attributes = True

# Question Schemas
class QuestionBase(BaseModel):
    question_text: str
    category: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Answer Schemas
class AnswerBase(BaseModel):
    answer_text: str

class AnswerCreate(AnswerBase):
    player_id: UUID
    question_id: int

class Answer(AnswerBase):
    id: int
    player_id: UUID
    question_id: int
    answered_at: datetime
    answer_date: date
    
    class Config:
        from_attributes = True

class AnswerWithQuestion(Answer):
    question: Question

# Quote Schemas
class QuoteBase(BaseModel):
    quote_text: str
    author: Optional[str] = None
    category: Optional[str] = None
    keywords: Optional[str] = None

class QuoteCreate(QuoteBase):
    pass

class Quote(QuoteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuoteMatch(Quote):
    relevance_score: float
```

### Step 6: Database Connection (database.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 7: CRUD Operations (crud.py)

Key functions to implement:

```python
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, timedelta, date
from typing import List, Optional
from uuid import UUID
import random

from . import models, schemas

# Player CRUD
def create_player(db: Session, player: schemas.PlayerCreate) -> models.Player:
    db_player = models.Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_player(db: Session, player_id: UUID) -> Optional[models.Player]:
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def get_players(db: Session, skip: int = 0, limit: int = 100) -> List[models.Player]:
    return db.query(models.Player).offset(skip).limit(limit).all()

# Question CRUD
def get_random_question_for_player(db: Session, player_id: UUID, days_back: int = 30) -> Optional[models.Question]:
    # Get questions answered by player in last N days
    cutoff_date = date.today() - timedelta(days=days_back)
    answered_question_ids = db.query(models.Answer.question_id).filter(
        and_(
            models.Answer.player_id == player_id,
            models.Answer.answer_date >= cutoff_date
        )
    ).all()
    answered_ids = [q[0] for q in answered_question_ids]
    
    # Get questions not answered recently
    available_questions = db.query(models.Question).filter(
        ~models.Question.id.in_(answered_ids)
    ).all()
    
    if not available_questions:
        # If all questions answered, return any random question
        available_questions = db.query(models.Question).all()
    
    return random.choice(available_questions) if available_questions else None

# Answer CRUD
def create_answer(db: Session, answer: schemas.AnswerCreate) -> models.Answer:
    db_answer = models.Answer(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def get_player_answers(db: Session, player_id: UUID, skip: int = 0, limit: int = 100) -> List[models.Answer]:
    return db.query(models.Answer).filter(
        models.Answer.player_id == player_id
    ).order_by(models.Answer.answered_at.desc()).offset(skip).limit(limit).all()

def get_player_answers_today(db: Session, player_id: UUID) -> List[models.Answer]:
    today = date.today()
    return db.query(models.Answer).filter(
        and_(
            models.Answer.player_id == player_id,
            models.Answer.answer_date == today
        )
    ).all()

# Quote matching logic
def find_matching_quote(db: Session, player_id: UUID) -> Optional[models.Quote]:
    # Get recent answers (last 7 days)
    cutoff_date = date.today() - timedelta(days=7)
    recent_answers = db.query(models.Answer).filter(
        and_(
            models.Answer.player_id == player_id,
            models.Answer.answer_date >= cutoff_date
        )
    ).all()
    
    if not recent_answers:
        # Return random quote if no recent answers
        quotes = db.query(models.Quote).all()
        return random.choice(quotes) if quotes else None
    
    # Extract keywords from answers (simple implementation)
    answer_text = " ".join([a.answer_text.lower() for a in recent_answers])
    
    # Get all quotes and score them
    quotes = db.query(models.Quote).all()
    scored_quotes = []
    
    for quote in quotes:
        score = 0
        if quote.keywords:
            keywords = [k.strip().lower() for k in quote.keywords.split(",")]
            for keyword in keywords:
                if keyword in answer_text:
                    score += 1
        scored_quotes.append((quote, score))
    
    # Sort by score and return best match
    scored_quotes.sort(key=lambda x: x[1], reverse=True)
    return scored_quotes[0][0] if scored_quotes else None
```

### Step 8: API Routers

Example for players router (routers/players.py):

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/players", tags=["players"])

@router.post("/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_username(db, username=player.username)
    if db_player:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_player(db=db, player=player)

@router.get("/", response_model=List[schemas.Player])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    players = crud.get_players(db, skip=skip, limit=limit)
    return players

@router.get("/{player_id}", response_model=schemas.Player)
def read_player(player_id: UUID, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player
```

### Step 9: Main Application (main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import players, questions, answers, quotes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Daily Question API",
    description="API for daily question web app",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(players.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(quotes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Daily Question API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

## Phase 2: Frontend Setup (React)

### Step 1: Initialize React Project

```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install axios react-router-dom @tanstack/react-query
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Step 2: Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── PlayerForm.jsx
│   │   ├── PlayerSelector.jsx
│   │   ├── QuestionCard.jsx
│   │   ├── AnswerForm.jsx
│   │   ├── QuoteDisplay.jsx
│   │   ├── AnswerHistory.jsx
│   │   └── Layout.jsx
│   ├── services/
│   │   └── api.js
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── PlayerPage.jsx
│   │   └── HistoryPage.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
└── vite.config.js
```

### Step 3: API Service (services/api.js)

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const playerAPI = {
  create: (data) => api.post('/players/', data),
  getAll: () => api.get('/players/'),
  getById: (id) => api.get(`/players/${id}`),
};

export const questionAPI = {
  getRandom: (playerId) => api.get(`/questions/random/${playerId}`),
  getAll: () => api.get('/questions/'),
};

export const answerAPI = {
  create: (data) => api.post('/answers/', data),
  getPlayerAnswers: (playerId) => api.get(`/answers/player/${playerId}`),
  getTodayAnswers: (playerId) => api.get(`/answers/player/${playerId}/today`),
};

export const quoteAPI = {
  getMatching: (playerId) => api.get(`/quotes/match/${playerId}`),
};

export default api;
```

### Step 4: Key Components

Example QuestionCard component:

```jsx
import React, { useState } from 'react';
import { answerAPI, questionAPI } from '../services/api';

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

## Phase 3: Database Initialization

### Sample Data Script (init_db.py)

```python
from app.database import SessionLocal, engine
from app import models
from datetime import datetime

def init_db():
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Sample questions
    questions = [
        "What made you smile today?",
        "What's one thing you learned recently?",
        "If you could have dinner with anyone, who would it be?",
        "What's your favorite childhood memory?",
        "What are you grateful for today?",
        # Add more questions...
    ]
    
    for q_text in questions:
        question = models.Question(question_text=q_text, category="general")
        db.add(question)
    
    # Sample quotes
    quotes = [
        {
            "quote_text": "The only way to do great work is to love what you do.",
            "author": "Steve Jobs",
            "keywords": "work, passion, love, great"
        },
        # Add more quotes...
    ]
    
    for q_data in quotes:
        quote = models.Quote(**q_data)
        db.add(quote)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
```

## Phase 4: Docker Configuration

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: dailyquestion
      POSTGRES_PASSWORD: password123
      POSTGRES_DB: dailyquestion_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://dailyquestion:password123@db:5432/dailyquestion_db
    depends_on:
      - db

  frontend:
    build: ./frontend
    command: npm run dev -- --host
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    depends_on:
      - backend

volumes:
  postgres_data:
```

## Testing Strategy

1. **Backend Tests**: Use pytest for API endpoint testing
2. **Frontend Tests**: Use Vitest/Jest for component testing
3. **Integration Tests**: Test complete user flows
4. **Manual Testing**: Test in browser with real interactions

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Sample data loaded
- [ ] CORS properly configured
- [ ] API documentation accessible
- [ ] Frontend builds successfully
- [ ] Docker containers running
- [ ] All endpoints tested
- [ ] Error handling implemented
- [ ] README documentation complete

## Common Issues & Solutions

1. **CORS Errors**: Ensure backend CORS middleware includes frontend URL
2. **Database Connection**: Check DATABASE_URL format and credentials
3. **Port Conflicts**: Ensure ports 5432, 8000, 5173 are available
4. **Module Not Found**: Verify all dependencies installed
5. **UUID Issues**: Ensure PostgreSQL UUID extension enabled

## Next Steps After Implementation

1. Add user authentication
2. Implement email notifications
3. Add data export functionality
4. Create admin dashboard
5. Optimize database queries
6. Add comprehensive error handling
7. Implement rate limiting
8. Add analytics tracking