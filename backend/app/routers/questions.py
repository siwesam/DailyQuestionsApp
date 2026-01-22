from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/questions", tags=["questions"])


@router.post("/", response_model=schemas.Question, status_code=status.HTTP_201_CREATED)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    """
    Create a new question (admin function).
    """
    return crud.create_question(db=db, question=question)


@router.get("/", response_model=List[schemas.Question])
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve list of all questions.
    """
    questions = crud.get_questions(db, skip=skip, limit=limit)
    return questions


@router.get("/random", response_model=schemas.Question)
def get_random_question(db: Session = Depends(get_db)):
    """
    Get a random question from the database.
    """
    question = crud.get_random_question(db)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No questions available"
        )
    return question


@router.get("/random/{player_id}", response_model=schemas.Question)
def get_random_question_for_player(player_id: str, db: Session = Depends(get_db)):
    """
    Get a random question that the player hasn't answered in the last 30 days.
    This allows players to answer multiple questions per day while avoiding recent repeats.
    """
    # Verify player exists
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    question = crud.get_random_question_for_player(db, player_id=player_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No questions available"
        )
    return question


@router.get("/{question_id}", response_model=schemas.Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    """
    Get a specific question by ID.
    """
    db_question = crud.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    return db_question

# Made with Bob
