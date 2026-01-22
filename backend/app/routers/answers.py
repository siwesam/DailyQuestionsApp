from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/answers", tags=["answers"])


@router.post("/", response_model=schemas.Answer, status_code=status.HTTP_201_CREATED)
def create_answer(answer: schemas.AnswerCreate, db: Session = Depends(get_db)):
    """
    Submit an answer to a question.
    Players can answer multiple questions per day.
    """
    # Verify player exists
    db_player = crud.get_player(db, player_id=answer.player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    # Verify question exists
    db_question = crud.get_question(db, question_id=answer.question_id)
    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return crud.create_answer(db=db, answer=answer)


@router.get("/player/{player_id}", response_model=List[schemas.AnswerWithQuestion])
def read_player_answers(
    player_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all answers for a specific player, ordered by most recent first.
    """
    # Verify player exists
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    answers = crud.get_player_answers(db, player_id=player_id, skip=skip, limit=limit)
    return answers


@router.get("/player/{player_id}/today", response_model=List[schemas.AnswerWithQuestion])
def read_player_answers_today(player_id: str, db: Session = Depends(get_db)):
    """
    Get all answers submitted by the player today.
    """
    # Verify player exists
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    answers = crud.get_player_answers_today(db, player_id=player_id)
    return answers


@router.get("/{answer_id}", response_model=schemas.AnswerWithQuestion)
def read_answer(answer_id: int, db: Session = Depends(get_db)):
    """
    Get a specific answer by ID.
    """
    db_answer = crud.get_answer(db, answer_id=answer_id)
    if db_answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    return db_answer

# Made with Bob
