# Quick Start Guide 🚀

Get your Daily Question app running in 5 minutes!

## For Complete Beginners

### Step 1: Install Prerequisites

1. **Install Docker Desktop** (easiest option)
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop

### Step 2: Run the Application

Open your terminal and run these commands:

```bash
# Start all services
docker-compose up -d

# Wait 30 seconds for services to start, then initialize the database
docker-compose exec backend python init_db.py
```

### Step 3: Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs

## Without Docker (Manual Setup)

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment
cp .env.example .env

# 6. Create database (PostgreSQL must be running)
createdb dailyquestion_db

# 7. Initialize with sample data
python init_db.py

# 8. Start backend
uvicorn app.main:app --reload
```

Backend running at: http://localhost:8000

### Frontend Setup

Open a new terminal:

```bash
# 1. Navigate to frontend
cd frontend

# 2. Initialize React project
npm create vite@latest . -- --template react

# When prompted:
# - "Current directory is not empty. Remove existing files and continue?" → Yes
# - Select framework: React
# - Select variant: JavaScript

# 3. Install dependencies
npm install
npm install axios react-router-dom

# 4. Start frontend
npm run dev
```

Frontend running at: http://localhost:5173

## Testing the API

Visit http://localhost:8000/docs to see interactive API documentation.

Try these endpoints:

1. **Create a player**: POST `/api/players/`
   ```json
   {
     "username": "john_doe",
     "email": "john@example.com"
   }
   ```

2. **Get a random question**: GET `/api/questions/random/{player_id}`

3. **Submit an answer**: POST `/api/answers/`
   ```json
   {
     "player_id": "your-player-id",
     "question_id": 1,
     "answer_text": "My thoughtful answer"
   }
   ```

4. **Get matching quote**: GET `/api/quotes/match/{player_id}`

## Common Issues

### "Port already in use"
```bash
# Stop existing services
docker-compose down

# Or kill specific port
lsof -ti:8000 | xargs kill  # Backend
lsof -ti:5173 | xargs kill  # Frontend
```

### "Database connection failed"
```bash
# Check PostgreSQL is running
brew services list  # Mac
sudo systemctl status postgresql  # Linux

# Or use Docker
docker-compose up -d db
```

### "Module not found"
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## What's Next?

1. ✅ Backend API is running with 50+ questions and 30+ quotes
2. ✅ Database is initialized with sample data
3. 🎨 Customize the frontend (see frontend/src/)
4. 📝 Add your own questions and quotes (edit backend/init_db.py)
5. 🚀 Deploy to production (see deployment guides)

## Need Help?

- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for code details

**Enjoy building your first Python web app! 🎉**