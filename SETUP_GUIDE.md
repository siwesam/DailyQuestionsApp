# Setup Guide - Daily Question Web App

This guide will help you set up and run your first Python web application!

## 📋 Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16+**: [Download Node.js](https://nodejs.org/)
- **PostgreSQL 13+**: [Download PostgreSQL](https://www.postgresql.org/download/)
  - OR use Docker (recommended for beginners)
- **Git**: [Download Git](https://git-scm.com/downloads)

## 🚀 Quick Start (Recommended for Beginners)

### Option 1: Using Docker (Easiest)

If you have Docker installed, this is the simplest way to get started:

```bash
# 1. Make sure Docker is running

# 2. Start all services
docker-compose up -d

# 3. Wait for services to start (about 30 seconds)

# 4. Initialize the database with sample data
docker-compose exec backend python init_db.py

# 5. Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

That's it! Your app is running. Skip to the "Using the Application" section.

### Option 2: Local Development Setup

If you prefer to run everything locally without Docker:

#### Step 1: Set Up PostgreSQL Database

**On macOS (using Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
createdb dailyquestion_db
```

**On Windows:**
1. Download and install PostgreSQL from the official website
2. During installation, remember your password
3. Open pgAdmin or psql and create a database named `dailyquestion_db`

**On Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb dailyquestion_db
```

#### Step 2: Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file with your database credentials
# Use a text editor to open .env and update DATABASE_URL if needed

# Initialize database with sample data
python init_db.py

# Start the backend server
uvicorn app.main:app --reload
```

The backend will be running at `http://localhost:8000`

#### Step 3: Set Up Frontend

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Initialize React project with Vite
npm create vite@latest . -- --template react

# Install dependencies
npm install
npm install axios react-router-dom

# Start the development server
npm run dev
```

The frontend will be running at `http://localhost:5173`

## 🎯 Using the Application

### 1. Register a Player

1. Open your browser and go to `http://localhost:5173`
2. You'll see a registration form
3. Enter a username and email
4. Click "Register"

### 2. Answer Questions

1. After registration, you'll see a random question
2. Type your answer in the text box
3. Click "Submit Answer"
4. You'll be asked if you want to answer another question

### 3. View Your Quote

1. When you're done answering questions, click "No, show me my quote"
2. You'll see a personalized inspirational quote based on your answers
3. The quote is matched using keywords from your responses

### 4. View Answer History

1. Click on "View History" or navigate to the history page
2. See all your previous answers with the questions
3. Filter by date or search through your answers

## 🔧 API Documentation

Once the backend is running, you can explore the API:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints:

**Players:**
- `POST /api/players/` - Register new player
- `GET /api/players/` - List all players
- `GET /api/players/{id}` - Get player details

**Questions:**
- `GET /api/questions/random/{player_id}` - Get random question for player
- `GET /api/questions/` - List all questions

**Answers:**
- `POST /api/answers/` - Submit an answer
- `GET /api/answers/player/{player_id}` - Get player's answer history
- `GET /api/answers/player/{player_id}/today` - Get today's answers

**Quotes:**
- `GET /api/quotes/match/{player_id}` - Get matching quote for player

## 🧪 Testing the API

You can test the API using the Swagger UI or with curl:

```bash
# Create a player
curl -X POST "http://localhost:8000/api/players/" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com"}'

# Get a random question (replace {player_id} with actual ID)
curl "http://localhost:8000/api/questions/random/{player_id}"

# Submit an answer
curl -X POST "http://localhost:8000/api/answers/" \
  -H "Content-Type: application/json" \
  -d '{
    "player_id": "{player_id}",
    "question_id": 1,
    "answer_text": "This is my answer"
  }'

# Get matching quote
curl "http://localhost:8000/api/quotes/match/{player_id}"
```

## 🛠️ Troubleshooting

### Backend Issues

**Problem: "Module not found" errors**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: "Database connection error"**
```bash
# Check if PostgreSQL is running
# macOS:
brew services list
# Linux:
sudo systemctl status postgresql
# Windows: Check Services app

# Verify database exists
psql -l  # List all databases

# Check .env file has correct DATABASE_URL
```

**Problem: "Port 8000 already in use"**
```bash
# Find and kill the process
# macOS/Linux:
lsof -ti:8000 | xargs kill
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

**Problem: "Cannot connect to backend"**
- Make sure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify API_URL in frontend code

**Problem: "npm install fails"**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Docker Issues

**Problem: "Container won't start"**
```bash
# Check logs
docker-compose logs backend
docker-compose logs db

# Rebuild containers
docker-compose down
docker-compose up -d --build
```

**Problem: "Database not initialized"**
```bash
# Wait for database to be ready
docker-compose exec db pg_isready -U dailyquestion

# Run init script
docker-compose exec backend python init_db.py
```

## 📊 Database Management

### View Database Contents

```bash
# Connect to PostgreSQL
psql -U dailyquestion -d dailyquestion_db

# Or with Docker:
docker-compose exec db psql -U dailyquestion -d dailyquestion_db

# Useful SQL commands:
\dt                          # List all tables
SELECT * FROM players;       # View all players
SELECT * FROM questions;     # View all questions
SELECT * FROM answers;       # View all answers
SELECT * FROM quotes;        # View all quotes
\q                          # Quit
```

### Reset Database

```bash
# Drop and recreate database
dropdb dailyquestion_db
createdb dailyquestion_db

# Or with Docker:
docker-compose down -v
docker-compose up -d
docker-compose exec backend python init_db.py
```

## 🎨 Customization

### Add More Questions

Edit `backend/init_db.py` and add questions to the `questions` list:

```python
{
    "question_text": "Your new question here?",
    "category": "your_category"
}
```

Then run:
```bash
python init_db.py
```

### Add More Quotes

Edit `backend/init_db.py` and add quotes to the `quotes` list:

```python
{
    "quote_text": "Your inspirational quote",
    "author": "Author Name",
    "category": "motivation",
    "keywords": "keyword1, keyword2, keyword3"
}
```

### Modify Frontend Styling

- Edit `frontend/src/index.css` for global styles
- Edit component files in `frontend/src/components/` for component-specific styles
- Consider using Tailwind CSS for rapid styling

## 🚀 Next Steps

Now that your app is running, you can:

1. **Customize the UI**: Modify React components to match your design preferences
2. **Add Features**: Implement user authentication, social sharing, or analytics
3. **Deploy**: Deploy to Heroku, Railway, or your preferred hosting platform
4. **Learn More**: Explore FastAPI and React documentation to enhance your skills

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Docker Documentation](https://docs.docker.com/)

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review the error messages carefully
3. Check the logs: `docker-compose logs` or terminal output
4. Consult the documentation for specific technologies
5. Search for the error message online

## 🎉 Congratulations!

You've successfully set up your first Python web application! This is a great foundation for learning full-stack development. Keep experimenting and building!

---

**Happy Coding! 🚀**