from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/quotes", tags=["quotes"])


@router.post("/", response_model=schemas.Quote, status_code=status.HTTP_201_CREATED)
def create_quote(quote: schemas.QuoteCreate, db: Session = Depends(get_db)):
    """
    Create a new quote (admin function).
    """
    return crud.create_quote(db=db, quote=quote)


@router.get("/", response_model=List[schemas.Quote])
def read_quotes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve list of all quotes.
    """
    quotes = crud.get_quotes(db, skip=skip, limit=limit)
    return quotes


@router.get("/random", response_model=schemas.Quote)
def get_random_quote(db: Session = Depends(get_db)):
    """
    Get a random quote from the database.
    """
    quote = crud.get_random_quote(db)
    if quote is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No quotes available"
        )
    return quote


@router.get("/match/{player_id}", response_model=schemas.QuoteMatch)
def get_matching_quote(player_id: str, db: Session = Depends(get_db)):
    """
    Get a quote that matches the player's recent answers.
    Uses keyword matching to find the most relevant quote based on the player's
    answers from the last 7 days.
    """
    # Verify player exists
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    result = crud.find_matching_quote(db, player_id=player_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No quotes available"
        )
    
    quote, relevance_score = result
    
    # Create a QuoteMatch response with the relevance score
    quote_match = schemas.QuoteMatch(
        id=quote.id,
        quote_text=quote.quote_text,
        author=quote.author,
        category=quote.category,
        keywords=quote.keywords,
        created_at=quote.created_at,
        relevance_score=relevance_score
    )
    
    return quote_match


@router.get("/{quote_id}", response_model=schemas.Quote)
def read_quote(quote_id: int, db: Session = Depends(get_db)):
    """
    Get a specific quote by ID.
    """
    db_quote = crud.get_quote(db, quote_id=quote_id)
    if db_quote is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )
    return db_quote

# Made with Bob
