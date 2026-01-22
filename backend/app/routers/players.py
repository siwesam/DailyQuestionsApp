from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from .. import crud, schemas
from ..database import get_db
from ..auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api/players", tags=["players"])


@router.post("/", response_model=schemas.Player, status_code=status.HTTP_201_CREATED)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    """
    Create a new player with username and email.
    """
    # Check if username already exists
    db_player = crud.get_player_by_username(db, username=player.username)
    if db_player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    db_player = crud.get_player_by_email(db, email=player.email)
    if db_player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return crud.create_player(db=db, player=player)


@router.post("/login", response_model=schemas.Token)
def login(player_login: schemas.PlayerLogin, db: Session = Depends(get_db)):
    """
    Authenticate a player and return an access token.
    """
    player = crud.authenticate_player(db, username=player_login.username, password=player_login.password)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": player.username, "player_id": player.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=List[schemas.Player])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve list of all players.
    """
    players = crud.get_players(db, skip=skip, limit=limit)
    return players


@router.get("/{player_id}", response_model=schemas.Player)
def read_player(player_id: str, db: Session = Depends(get_db)):
    """
    Get a specific player by ID.
    """
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    return db_player


@router.put("/{player_id}", response_model=schemas.Player)
def update_player(
    player_id: str,
    player_update: schemas.PlayerUpdate,
    db: Session = Depends(get_db)
):
    """
    Update player information.
    """
    # Check if username is being updated and if it's already taken
    if player_update.username:
        existing_player = crud.get_player_by_username(db, username=player_update.username)
        if existing_player and existing_player.id != player_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Check if email is being updated and if it's already taken
    if player_update.email:
        existing_player = crud.get_player_by_email(db, email=player_update.email)
        if existing_player and existing_player.id != player_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
    
    db_player = crud.update_player(db, player_id=player_id, player_update=player_update)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    return db_player


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(player_id: str, db: Session = Depends(get_db)):
    """
    Delete a player and all their answers.
    """
    success = crud.delete_player(db, player_id=player_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    return None

# Made with Bob
