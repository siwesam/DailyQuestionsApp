from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, timedelta, date
from typing import List, Optional
import random

from . import models, schemas
from .auth import get_password_hash, verify_password


# ==================== Player CRUD ====================

def create_player(db: Session, player: schemas.PlayerCreate) -> models.Player:
    player_data = player.model_dump()
    password = player_data.pop("password")
    hashed_password = get_password_hash(password)
    
    db_player = models.Player(**player_data, hashed_password=hashed_password)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def authenticate_player(db: Session, username: str, password: str) -> Optional[models.Player]:
    """Authenticate a player by username and password."""
    player = get_player_by_username(db, username)
    if not player:
        return None
    if not verify_password(password, player.hashed_password):
        return None
    return player


def get_player(db: Session, player_id: str) -> Optional[models.Player]:
    return db.query(models.Player).filter(models.Player.id == player_id).first()


def get_player_by_username(db: Session, username: str) -> Optional[models.Player]:
    return db.query(models.Player).filter(models.Player.username == username).first()


def get_player_by_email(db: Session, email: str) -> Optional[models.Player]:
    return db.query(models.Player).filter(models.Player.email == email).first()


def get_players(db: Session, skip: int = 0, limit: int = 100) -> List[models.Player]:
    return db.query(models.Player).offset(skip).limit(limit).all()


def update_player(db: Session, player_id: str, player_update: schemas.PlayerUpdate) -> Optional[models.Player]:
    db_player = get_player(db, player_id)
    if not db_player:
        return None
    
    update_data = player_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_player, field, value)
    
    db_player.last_active = datetime.utcnow()
    db.commit()
    db.refresh(db_player)
    return db_player


def delete_player(db: Session, player_id: str) -> bool:
    db_player = get_player(db, player_id)
    if not db_player:
        return False
    
    db.delete(db_player)
    db.commit()
    return True


# ==================== Question CRUD ====================

def create_question(db: Session, question: schemas.QuestionCreate) -> models.Question:
    db_question = models.Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_question(db: Session, question_id: int) -> Optional[models.Question]:
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Question]:
    return db.query(models.Question).offset(skip).limit(limit).all()


def get_random_question(db: Session) -> Optional[models.Question]:
    questions = db.query(models.Question).all()
    return random.choice(questions) if questions else None


def get_random_question_for_player(db: Session, player_id: str, days_back: int = 7) -> Optional[models.Question]:
    """
    Get a random question that the player hasn't answered in the last N days.
    If all questions have been answered recently, allow repeating questions.
    Default is 7 days to allow more frequent question rotation.
    """
    # Get questions answered by player in last N days
    cutoff_date = date.today() - timedelta(days=days_back)
    answered_question_ids = db.query(models.Answer.question_id).filter(
        and_(
            models.Answer.player_id == player_id,
            models.Answer.answer_date >= cutoff_date
        )
    ).all()
    answered_ids = [q[0] for q in answered_question_ids]
    
    # Get all questions from database
    all_questions = db.query(models.Question).all()
    
    if not all_questions:
        return None
    
    # Get questions not answered recently
    if answered_ids:
        available_questions = [q for q in all_questions if q.id not in answered_ids]
    else:
        available_questions = all_questions
    
    # If all questions answered recently, allow repeating (return any question)
    if not available_questions:
        available_questions = all_questions
    
    return random.choice(available_questions) if available_questions else None


# ==================== Answer CRUD ====================

def create_answer(db: Session, answer: schemas.AnswerCreate) -> models.Answer:
    db_answer = models.Answer(**answer.model_dump())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    
    # Update player's last_active timestamp
    db_player = get_player(db, answer.player_id)
    if db_player:
        db_player.last_active = datetime.utcnow()
        db.commit()
    
    return db_answer


def get_answer(db: Session, answer_id: int) -> Optional[models.Answer]:
    return db.query(models.Answer).filter(models.Answer.id == answer_id).first()


def get_player_answers(db: Session, player_id: str, skip: int = 0, limit: int = 100) -> List[models.Answer]:
    return db.query(models.Answer).filter(
        models.Answer.player_id == player_id
    ).order_by(models.Answer.answered_at.desc()).offset(skip).limit(limit).all()


def get_player_answers_today(db: Session, player_id: str) -> List[models.Answer]:
    today = date.today()
    return db.query(models.Answer).filter(
        and_(
            models.Answer.player_id == player_id,
            models.Answer.answer_date == today
        )
    ).order_by(models.Answer.answered_at.desc()).all()


def get_player_recent_answers(db: Session, player_id: str, days: int = 7) -> List[models.Answer]:
    cutoff_date = date.today() - timedelta(days=days)
    return db.query(models.Answer).filter(
        and_(
            models.Answer.player_id == player_id,
            models.Answer.answer_date >= cutoff_date
        )
    ).order_by(models.Answer.answered_at.desc()).all()


# ==================== Quote CRUD ====================

def create_quote(db: Session, quote: schemas.QuoteCreate) -> models.Quote:
    db_quote = models.Quote(**quote.model_dump())
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote


def get_quote(db: Session, quote_id: int) -> Optional[models.Quote]:
    return db.query(models.Quote).filter(models.Quote.id == quote_id).first()


def get_quotes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Quote]:
    return db.query(models.Quote).offset(skip).limit(limit).all()


def get_random_quote(db: Session) -> Optional[models.Quote]:
    quotes = db.query(models.Quote).all()
    return random.choice(quotes) if quotes else None


def find_matching_quote(db: Session, player_id: str) -> Optional[tuple[models.Quote, float]]:
    """
    Find a quote that matches the player's recent answers.
    Returns tuple of (quote, relevance_score) or None.
    """
    # Get recent answers (last 7 days)
    recent_answers = get_player_recent_answers(db, player_id, days=7)
    
    if not recent_answers:
        # Return random quote if no recent answers
        random_quote = get_random_quote(db)
        return (random_quote, 0.0) if random_quote else None
    
    # Extract keywords from answers (simple implementation - convert to lowercase)
    answer_text = " ".join([a.answer_text.lower() for a in recent_answers])
    answer_words = set(answer_text.split())
    
    # Get all quotes and score them
    quotes = db.query(models.Quote).all()
    if not quotes:
        return None
    
    scored_quotes = []
    
    for quote in quotes:
        score = 0.0
        if quote.keywords:
            keywords = [k.strip().lower() for k in quote.keywords.split(",")]
            # Count matching keywords
            for keyword in keywords:
                if keyword in answer_text:
                    score += 1.0
                # Also check for partial matches in answer words
                for word in answer_words:
                    if keyword in word or word in keyword:
                        score += 0.5
        
        scored_quotes.append((quote, score))
    
    # Sort by score (descending) and return best match
    scored_quotes.sort(key=lambda x: x[1], reverse=True)
    
    # If no matches found (all scores are 0), return random quote
    if scored_quotes[0][1] == 0.0:
        return (random.choice(quotes), 0.0)
    
    return scored_quotes[0]


def create_answer_quote_match(db: Session, answer_id: int, quote_id: int, relevance_score: float) -> models.AnswerQuote:
    """
    Create a record of a quote being matched to an answer.
    """
    db_match = models.AnswerQuote(
        answer_id=answer_id,
        quote_id=quote_id,
        relevance_score=relevance_score
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

# Made with Bob
