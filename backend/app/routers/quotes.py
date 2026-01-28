from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import logging
import json
import asyncio

from .. import crud, schemas
from ..database import get_db
from ..services.ai_quote_agent import ai_quote_agent

router = APIRouter(prefix="/api/quotes", tags=["quotes"])
logger = logging.getLogger(__name__)


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
def get_matching_quote(player_id: str, use_ai: bool = True, db: Session = Depends(get_db)):
    """
    Get a quote that matches the player's recent answers.
    
    If use_ai=True (default), uses AI agent to intelligently select quotes from existing ones
    or fetch new relevant quotes from the internet.
    
    If use_ai=False, falls back to simple keyword matching.
    """
    # Verify player exists
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    if use_ai:
        try:
            logger.info(f"Using AI agent to select quote for player: {player_id}")
            quote, relevance_score, reason = ai_quote_agent.select_best_quote(db, player_id)
            
            # Create a QuoteMatch response with the relevance score
            quote_match = schemas.QuoteMatch(
                id=quote.id,
                quote_text=quote.quote_text,
                author=quote.author,
                category=quote.category,
                keywords=quote.keywords,
                created_at=quote.created_at,
                source=quote.source,
                is_ai_generated=quote.is_ai_generated,
                ai_relevance_reason=reason,
                relevance_score=relevance_score
            )
            
            return quote_match
            
        except Exception as e:
            logger.error(f"AI quote selection failed: {e}, falling back to keyword matching")
            # Fall back to keyword matching if AI fails
            use_ai = False
    
    if not use_ai:
        # Fallback to original keyword matching
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
            source=quote.source,
            is_ai_generated=quote.is_ai_generated,
            ai_relevance_reason=quote.ai_relevance_reason,
            relevance_score=relevance_score
        )
        
        return quote_match


@router.get("/match/{player_id}/stream")
async def get_matching_quote_stream(player_id: str, use_ai: bool = True, db: Session = Depends(get_db)):
    """
    Get a quote with real-time progress updates via Server-Sent Events (SSE).
    Returns a stream of progress messages followed by the final quote.
    """
    async def generate_progress():
        should_use_ai = use_ai  # Create local variable to avoid scope issues
        try:
            # Verify player exists
            db_player = crud.get_player(db, player_id=player_id)
            if db_player is None:
                yield f"data: {json.dumps({'error': 'Player not found'})}\n\n"
                return
            
            # Send initial progress
            yield f"data: {json.dumps({'status': 'starting', 'message': 'Analyzing your answers...'})}\n\n"
            await asyncio.sleep(0.1)
            
            if should_use_ai:
                try:
                    # Get recent answers
                    yield f"data: {json.dumps({'status': 'progress', 'message': 'Reviewing your recent responses...'})}\n\n"
                    await asyncio.sleep(0.1)
                    
                    recent_answers = crud.get_player_recent_answers(db, player_id, days=7)
                    
                    if not recent_answers:
                        yield f"data: {json.dumps({'status': 'progress', 'message': 'No recent answers found, selecting random quote...'})}\n\n"
                        await asyncio.sleep(0.1)
                    else:
                        yield f"data: {json.dumps({'status': 'progress', 'message': f'Found {len(recent_answers)} recent answers'})}\n\n"
                        await asyncio.sleep(0.1)
                    
                    # Check existing quotes
                    yield f"data: {json.dumps({'status': 'progress', 'message': 'Checking database quotes...'})}\n\n"
                    await asyncio.sleep(0.1)
                    
                    existing_quotes = crud.get_quotes(db, limit=100)
                    yield f"data: {json.dumps({'status': 'progress', 'message': f'Found {len(existing_quotes)} quotes in database'})}\n\n"
                    await asyncio.sleep(0.1)
                    
                    # Create a callback to send AI logs to frontend
                    async def log_callback(message):
                        yield f"data: {json.dumps({'status': 'progress', 'message': message})}\n\n"
                        await asyncio.sleep(0.05)
                    
                    # Get the quote with detailed logging
                    logger.info(f"Using AI agent to select quote for player: {player_id}")
                    
                    # We need to handle the callback differently since select_best_quote is sync
                    # Let's collect logs and send them
                    logs = []
                    def sync_log_callback(message):
                        logs.append(message)
                    
                    quote, relevance_score, reason = ai_quote_agent.select_best_quote(db, player_id, sync_log_callback)
                    
                    # Send all collected logs
                    for log_message in logs:
                        yield f"data: {json.dumps({'status': 'progress', 'message': log_message})}\n\n"
                        await asyncio.sleep(0.05)
                    
                    if quote.source == 'brainyquote' or quote.is_ai_generated:
                        yield f"data: {json.dumps({'status': 'progress', 'message': 'Found a perfect match from the web!'})}\n\n"
                    else:
                        yield f"data: {json.dumps({'status': 'progress', 'message': 'Selected best matching quote!'})}\n\n"
                    await asyncio.sleep(0.1)
                    
                    # Create response
                    quote_match = schemas.QuoteMatch(
                        id=quote.id,
                        quote_text=quote.quote_text,
                        author=quote.author,
                        category=quote.category,
                        keywords=quote.keywords,
                        created_at=quote.created_at,
                        source=quote.source,
                        is_ai_generated=quote.is_ai_generated,
                        ai_relevance_reason=reason,
                        relevance_score=relevance_score
                    )
                    
                    # Send final result
                    yield f"data: {json.dumps({'status': 'complete', 'quote': quote_match.model_dump(mode='json')})}\n\n"
                    return  # Exit after successful AI quote
                    
                except Exception as e:
                    logger.error(f"AI quote selection failed: {e}, falling back to keyword matching")
                    yield f"data: {json.dumps({'status': 'progress', 'message': 'AI unavailable, using keyword matching...'})}\n\n"
                    await asyncio.sleep(0.1)
                    should_use_ai = False
            
            if not should_use_ai:
                # Fallback to keyword matching
                yield f"data: {json.dumps({'status': 'progress', 'message': 'Matching keywords from your answers...'})}\n\n"
                await asyncio.sleep(0.1)
                
                result = crud.find_matching_quote(db, player_id=player_id)
                if result is None:
                    yield f"data: {json.dumps({'error': 'No quotes available'})}\n\n"
                    return
                
                quote, relevance_score = result
                
                quote_match = schemas.QuoteMatch(
                    id=quote.id,
                    quote_text=quote.quote_text,
                    author=quote.author,
                    category=quote.category,
                    keywords=quote.keywords,
                    created_at=quote.created_at,
                    source=quote.source,
                    is_ai_generated=quote.is_ai_generated,
                    ai_relevance_reason=quote.ai_relevance_reason,
                    relevance_score=relevance_score
                )
                
                yield f"data: {json.dumps({'status': 'complete', 'quote': quote_match.model_dump(mode='json')})}\n\n"
                
        except Exception as e:
            logger.error(f"Error in quote stream: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_progress(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


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
