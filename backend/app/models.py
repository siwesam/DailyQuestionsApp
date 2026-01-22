from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base


class Player(Base):
    __tablename__ = "players"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
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
    player_id = Column(String(36), ForeignKey("players.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    answered_at = Column(DateTime, default=datetime.utcnow)
    answer_date = Column(Date, default=lambda: datetime.utcnow().date(), index=True)
    
    player = relationship("Player", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    quote_matches = relationship("AnswerQuote", back_populates="answer", cascade="all, delete-orphan")


class Quote(Base):
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    quote_text = Column(Text, nullable=False)
    author = Column(String(100))
    category = Column(String(50))
    keywords = Column(Text)  # Comma-separated keywords
    created_at = Column(DateTime, default=datetime.utcnow)
    
    answer_matches = relationship("AnswerQuote", back_populates="quote", cascade="all, delete-orphan")


class AnswerQuote(Base):
    __tablename__ = "answer_quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, ForeignKey("answers.id"), nullable=False)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)
    relevance_score = Column(Float, default=0.0)
    matched_at = Column(DateTime, default=datetime.utcnow)
    
    answer = relationship("Answer", back_populates="quote_matches")
    quote = relationship("Quote", back_populates="answer_matches")

# Made with Bob
