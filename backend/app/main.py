from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, SessionLocal
from .routers import players, questions, answers, quotes
from . import models

# Create database tables
Base.metadata.create_all(bind=engine)

# Auto-initialize database with sample data on startup
def init_sample_data():
    """Initialize database with sample questions and quotes if empty."""
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_questions = db.query(models.Question).count()
        if existing_questions > 0:
            print(f"Database already has {existing_questions} questions. Skipping initialization.")
            return
        
        print("Initializing database with sample data...")
        
        # Sample questions
        questions = [
            {"question_text": "What made you smile today?", "category": "daily"},
            {"question_text": "What are you grateful for today?", "category": "gratitude"},
            {"question_text": "What's one thing you learned recently?", "category": "learning"},
            {"question_text": "What's your favorite childhood memory?", "category": "memories"},
            {"question_text": "What's something you're proud of accomplishing?", "category": "achievement"},
            {"question_text": "If you could have dinner with anyone, who would it be and why?", "category": "aspirations"},
            {"question_text": "What's a skill you'd like to learn?", "category": "learning"},
            {"question_text": "What's your dream vacation destination?", "category": "travel"},
            {"question_text": "If you could change one thing about the world, what would it be?", "category": "aspirations"},
            {"question_text": "What does success mean to you?", "category": "philosophy"},
            {"question_text": "What book are you reading or would like to read?", "category": "interests"},
            {"question_text": "What's your favorite movie or TV show and why?", "category": "interests"},
            {"question_text": "What hobby brings you the most joy?", "category": "hobbies"},
            {"question_text": "What's your favorite way to spend a weekend?", "category": "lifestyle"},
            {"question_text": "What kind of music do you enjoy?", "category": "interests"},
            {"question_text": "What quality do you value most in a friend?", "category": "relationships"},
            {"question_text": "Who has had the biggest influence on your life?", "category": "relationships"},
            {"question_text": "What's the best advice you've ever received?", "category": "wisdom"},
            {"question_text": "What makes you feel most alive?", "category": "philosophy"},
            {"question_text": "What's your definition of happiness?", "category": "philosophy"},
            {"question_text": "What's a challenge you've overcome?", "category": "growth"},
            {"question_text": "What's something you're currently working on improving?", "category": "growth"},
            {"question_text": "What fear would you like to conquer?", "category": "growth"},
            {"question_text": "What's the most important lesson life has taught you?", "category": "wisdom"},
            {"question_text": "How do you handle difficult situations?", "category": "coping"},
            {"question_text": "If you could have any superpower, what would it be?", "category": "imagination"},
            {"question_text": "What would you do if you won the lottery?", "category": "imagination"},
            {"question_text": "If you could live in any time period, when would it be?", "category": "imagination"},
            {"question_text": "What's your idea of a perfect day?", "category": "lifestyle"},
            {"question_text": "If you could master any instrument, which would you choose?", "category": "interests"},
            {"question_text": "What's your morning routine like?", "category": "daily"},
            {"question_text": "What's your favorite meal to cook or eat?", "category": "food"},
            {"question_text": "How do you like to relax after a long day?", "category": "lifestyle"},
            {"question_text": "What's your favorite season and why?", "category": "preferences"},
            {"question_text": "What's something small that makes your day better?", "category": "daily"},
            {"question_text": "Where do you see yourself in five years?", "category": "future"},
            {"question_text": "What's a goal you're working towards?", "category": "goals"},
            {"question_text": "What legacy would you like to leave?", "category": "philosophy"},
            {"question_text": "What's something you want to achieve this year?", "category": "goals"},
            {"question_text": "What motivates you to keep going?", "category": "motivation"},
            {"question_text": "What's something you appreciate about yourself?", "category": "self-reflection"},
            {"question_text": "What brings you peace?", "category": "mindfulness"},
            {"question_text": "What's a recent act of kindness you witnessed or performed?", "category": "kindness"},
            {"question_text": "What are you looking forward to?", "category": "optimism"},
            {"question_text": "What's something you'd like to tell your younger self?", "category": "wisdom"},
            {"question_text": "What's your favorite joke or funny story?", "category": "humor"},
            {"question_text": "If you could have any pet, real or imaginary, what would it be?", "category": "fun"},
            {"question_text": "What's the most interesting place you've ever visited?", "category": "travel"},
            {"question_text": "What's your hidden talent?", "category": "fun"},
            {"question_text": "What's the best gift you've ever received?", "category": "memories"},
        ]
        
        for q_data in questions:
            question = models.Question(**q_data)
            db.add(question)
        
        # Sample quotes
        quotes = [
            {"quote_text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "motivation", "keywords": "work, passion, love, great, success, career"},
            {"quote_text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill", "category": "motivation", "keywords": "success, failure, courage, perseverance, continue, determination"},
            {"quote_text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt", "category": "motivation", "keywords": "believe, confidence, achievement, positive, mindset"},
            {"quote_text": "The beautiful thing about learning is that no one can take it away from you.", "author": "B.B. King", "category": "learning", "keywords": "learning, education, knowledge, growth, wisdom"},
            {"quote_text": "Live as if you were to die tomorrow. Learn as if you were to live forever.", "author": "Mahatma Gandhi", "category": "learning", "keywords": "learn, life, knowledge, education, wisdom, growth"},
            {"quote_text": "The only impossible journey is the one you never begin.", "author": "Tony Robbins", "category": "motivation", "keywords": "journey, begin, start, impossible, action, courage"},
            {"quote_text": "Happiness is not something ready made. It comes from your own actions.", "author": "Dalai Lama", "category": "happiness", "keywords": "happiness, actions, joy, gratitude, positive, mindset"},
            {"quote_text": "Gratitude turns what we have into enough.", "author": "Anonymous", "category": "gratitude", "keywords": "gratitude, thankful, appreciation, enough, contentment"},
            {"quote_text": "The secret of being happy is accepting where you are in life and making the most out of everyday.", "author": "Anonymous", "category": "happiness", "keywords": "happy, acceptance, life, everyday, present, mindfulness"},
            {"quote_text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "category": "dreams", "keywords": "future, dreams, believe, beauty, aspirations, hope"},
            {"quote_text": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson", "category": "motivation", "keywords": "time, perseverance, keep going, determination, action"},
            {"quote_text": "Dream big and dare to fail.", "author": "Norman Vaughan", "category": "dreams", "keywords": "dream, big, dare, fail, courage, risk, aspirations"},
            {"quote_text": "The only true wisdom is in knowing you know nothing.", "author": "Socrates", "category": "wisdom", "keywords": "wisdom, knowledge, learning, humility, philosophy"},
            {"quote_text": "Life is what happens when you're busy making other plans.", "author": "John Lennon", "category": "wisdom", "keywords": "life, plans, present, mindfulness, unexpected"},
            {"quote_text": "Be yourself; everyone else is already taken.", "author": "Oscar Wilde", "category": "wisdom", "keywords": "authentic, yourself, unique, individuality, identity"},
            {"quote_text": "Courage is not the absence of fear, but rather the assessment that something else is more important than fear.", "author": "Franklin D. Roosevelt", "category": "courage", "keywords": "courage, fear, brave, strength, overcome, challenge"},
            {"quote_text": "You are braver than you believe, stronger than you seem, and smarter than you think.", "author": "A.A. Milne", "category": "encouragement", "keywords": "brave, strong, smart, believe, confidence, strength"},
            {"quote_text": "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "author": "Ralph Waldo Emerson", "category": "wisdom", "keywords": "inner strength, past, future, within, potential"},
            {"quote_text": "Change is the only constant in life.", "author": "Heraclitus", "category": "change", "keywords": "change, constant, life, adapt, growth, evolution"},
            {"quote_text": "The only person you are destined to become is the person you decide to be.", "author": "Ralph Waldo Emerson", "category": "growth", "keywords": "destiny, decide, become, choice, growth, self-improvement"},
            {"quote_text": "Growth is painful. Change is painful. But nothing is as painful as staying stuck somewhere you don't belong.", "author": "Mandy Hale", "category": "growth", "keywords": "growth, change, painful, stuck, belong, transformation"},
            {"quote_text": "The best thing to hold onto in life is each other.", "author": "Audrey Hepburn", "category": "relationships", "keywords": "love, relationships, together, connection, support, friendship"},
            {"quote_text": "In the end, we will remember not the words of our enemies, but the silence of our friends.", "author": "Martin Luther King Jr.", "category": "relationships", "keywords": "friends, friendship, support, loyalty, relationships"},
            {"quote_text": "A friend is someone who knows all about you and still loves you.", "author": "Elbert Hubbard", "category": "friendship", "keywords": "friend, friendship, love, acceptance, relationships, support"},
            {"quote_text": "Imagination is more important than knowledge.", "author": "Albert Einstein", "category": "creativity", "keywords": "imagination, creativity, knowledge, innovation, ideas"},
            {"quote_text": "Creativity is intelligence having fun.", "author": "Albert Einstein", "category": "creativity", "keywords": "creativity, intelligence, fun, imagination, innovation"},
            {"quote_text": "The worst enemy to creativity is self-doubt.", "author": "Sylvia Plath", "category": "creativity", "keywords": "creativity, doubt, confidence, art, expression, imagination"},
            {"quote_text": "Peace comes from within. Do not seek it without.", "author": "Buddha", "category": "peace", "keywords": "peace, within, mindfulness, calm, serenity, meditation"},
            {"quote_text": "The present moment is the only time over which we have dominion.", "author": "Thích Nhất Hạnh", "category": "mindfulness", "keywords": "present, moment, mindfulness, now, awareness, meditation"},
            {"quote_text": "Smile, breathe, and go slowly.", "author": "Thích Nhất Hạnh", "category": "mindfulness", "keywords": "smile, breathe, slow, calm, peace, mindfulness, meditation"},
            {"quote_text": "No act of kindness, no matter how small, is ever wasted.", "author": "Aesop", "category": "kindness", "keywords": "kindness, compassion, small, help, generosity, caring"},
            {"quote_text": "Be kind whenever possible. It is always possible.", "author": "Dalai Lama", "category": "kindness", "keywords": "kind, kindness, possible, compassion, caring, love"},
        ]
        
        for q_data in quotes:
            quote = models.Quote(**q_data)
            db.add(quote)
        
        db.commit()
        print(f"✅ Database initialized with {len(questions)} questions and {len(quotes)} quotes")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

# Initialize sample data on startup
init_sample_data()

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
