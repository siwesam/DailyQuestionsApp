from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import players, questions, answers, quotes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Daily Question API",
    description="API for daily question web app where players answer questions and receive personalized quotes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration - allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Vue default
    ],
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
    """
    Root endpoint - welcome message.
    """
    return {
        "message": "Welcome to Daily Question API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}

# Made with Bob
