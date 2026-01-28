from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional


# Player Schemas
class PlayerBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class PlayerCreate(PlayerBase):
    password: str = Field(..., min_length=6, max_length=100)


class PlayerUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class Player(PlayerBase):
    id: str
    created_at: datetime
    last_active: datetime
    
    class Config:
        from_attributes = True


class PlayerLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


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
    player_id: str
    question_id: int


class Answer(AnswerBase):
    id: int
    player_id: str
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
    source: Optional[str] = None
    is_ai_generated: Optional[int] = 0
    ai_relevance_reason: Optional[str] = None


class Quote(QuoteBase):
    id: int
    created_at: datetime
    source: Optional[str] = None
    is_ai_generated: Optional[int] = 0
    ai_relevance_reason: Optional[str] = None
    
    class Config:
        from_attributes = True


class QuoteMatch(Quote):
    relevance_score: float = 0.0

# Made with Bob
