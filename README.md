# Daily Question Web App 🎯

A full-stack web application where players answer random questions daily and receive personalized inspirational quotes based on their responses.

## 🌟 Features

- **Player Management**: Register and manage player profiles
- **Daily Questions**: Answer multiple random questions each day
- **Smart Question Selection**: Avoids repeating questions within 30 days
- **Answer History**: View all your previous answers
- **Personalized Quotes**: Get inspirational quotes matched to your answers
- **Modern UI**: Clean, responsive interface built with React/Vue.js
- **RESTful API**: Well-documented FastAPI backend
- **PostgreSQL Database**: Robust data storage
- **Docker Support**: Easy deployment with Docker Compose

## 🏗️ Architecture

```
┌─────────────┐      ┌─────────────┐      ┌──────────────┐
│   React/    │ HTTP │   FastAPI   │ SQL  │  PostgreSQL  │
│   Vue.js    │◄────►│   Backend   │◄────►│   Database   │
│  Frontend   │      │     API     │      │              │
└─────────────┘      └─────────────┘      └──────────────┘
```

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+ (or Docker)
- Git

## 🚀 Quick Start with Docker

The easiest way to run the application:

```bash
# Clone the repository
git clone <repository-url>
cd DummyPythonApp

# Start all services
docker-compose up -d

# Initialize database with sample data
docker-compose exec backend python init_db.py

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 💻 Local Development Setup

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

Example `.env` file:
```env
DATABASE_URL=postgresql://dailyquestion:password123@localhost:5432/dailyquestion_db
SECRET_KEY=your-secret-key-here
```

5. **Start PostgreSQL** (if not using Docker)
```bash
# macOS with Homebrew
brew services start postgresql

# Linux
sudo systemctl start postgresql

# Or use Docker
docker run --name postgres-db -e POSTGRES_PASSWORD=password123 -p 5432:5432 -d postgres:15
```

6. **Initialize database**
```bash
python init_db.py
```

7. **Run the backend server**
```bash
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
# or
yarn install
```

3. **Start development server**
```bash
npm run dev
# or
yarn dev
```

Frontend will be available at `http://localhost:5173`

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Players
- `POST /api/players/` - Create new player
- `GET /api/players/` - List all players
- `GET /api/players/{id}` - Get player details
- `PUT /api/players/{id}` - Update player
- `DELETE /api/players/{id}` - Delete player

#### Questions
- `GET /api/questions/random/{player_id}` - Get random question for player
- `GET /api/questions/` - List all questions
- `POST /api/questions/` - Create new question

#### Answers
- `POST /api/answers/` - Submit answer
- `GET /api/answers/player/{player_id}` - Get player's answer history
- `GET /api/answers/player/{player_id}/today` - Get today's answers

#### Quotes
- `GET /api/quotes/match/{player_id}` - Get matching quote for player
- `GET /api/quotes/` - List all quotes
- `POST /api/quotes/` - Create new quote

## 🎮 Usage Flow

1. **Register**: Create a new player account with username and email
2. **Get Question**: Receive a random question you haven't answered recently
3. **Submit Answer**: Type and submit your answer
4. **Continue or Finish**: Choose to answer more questions or finish
5. **View Quote**: If finished, see a personalized inspirational quote
6. **View History**: Browse all your previous answers anytime

## 🗄️ Database Schema

### Tables

**players**
- `id` (UUID, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `created_at` (Timestamp)
- `last_active` (Timestamp)

**questions**
- `id` (Integer, Primary Key)
- `question_text` (Text)
- `category` (String)
- `created_at` (Timestamp)

**answers**
- `id` (Integer, Primary Key)
- `player_id` (UUID, Foreign Key)
- `question_id` (Integer, Foreign Key)
- `answer_text` (Text)
- `answered_at` (Timestamp)
- `answer_date` (Date)

**quotes**
- `id` (Integer, Primary Key)
- `quote_text` (Text)
- `author` (String)
- `category` (String)
- `keywords` (Text)
- `created_at` (Timestamp)

**answer_quotes**
- `id` (Integer, Primary Key)
- `answer_id` (Integer, Foreign Key)
- `quote_id` (Integer, Foreign Key)
- `relevance_score` (Float)
- `matched_at` (Timestamp)

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
# or
yarn test
```

## 📦 Project Structure

```
DummyPythonApp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database connection
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── crud.py              # Database operations
│   │   ├── config.py            # Configuration
│   │   ├── routers/             # API endpoints
│   │   │   ├── players.py
│   │   │   ├── questions.py
│   │   │   ├── answers.py
│   │   │   └── quotes.py
│   │   └── utils/               # Helper functions
│   ├── tests/                   # Backend tests
│   ├── requirements.txt
│   ├── .env.example
│   └── init_db.py
├── frontend/
│   ├── src/
│   │   ├── components/          # React/Vue components
│   │   ├── services/            # API service
│   │   ├── pages/               # Page components
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── README.md
├── PLAN.md
├── ARCHITECTURE.md
└── IMPLEMENTATION_GUIDE.md
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Configuration

Edit `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild containers
docker-compose up -d --build

# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec db psql -U dailyquestion -d dailyquestion_db
```

## 🛠️ Troubleshooting

### Backend Issues

**Database connection error**
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in `.env`
- Ensure database exists: `createdb dailyquestion_db`

**Module not found**
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

**Port already in use**
- Change port in uvicorn command: `--port 8001`
- Or kill process using port: `lsof -ti:8000 | xargs kill`

### Frontend Issues

**CORS errors**
- Verify backend CORS settings in `main.py`
- Check API_BASE_URL in `api.js`

**Dependencies error**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

**Build fails**
- Clear cache: `npm cache clean --force`
- Update Node.js to latest LTS version

### Docker Issues

**Container won't start**
- Check logs: `docker-compose logs backend`
- Verify ports are available
- Rebuild: `docker-compose up -d --build`

**Database initialization fails**
- Wait for PostgreSQL to be ready
- Run init script manually: `docker-compose exec backend python init_db.py`

## 📈 Performance Tips

1. **Database Indexing**: Already configured on frequently queried columns
2. **Connection Pooling**: SQLAlchemy handles this automatically
3. **Caching**: Consider adding Redis for frequently accessed data
4. **Pagination**: Implemented in list endpoints
5. **Query Optimization**: Use eager loading for related data

## 🔐 Security Considerations

- Environment variables for sensitive data
- SQL injection prevention via SQLAlchemy ORM
- Input validation with Pydantic
- CORS properly configured
- Consider adding authentication for production

## 🚀 Deployment

### Production Checklist

- [ ] Set strong SECRET_KEY
- [ ] Use production database
- [ ] Enable HTTPS
- [ ] Set up proper CORS origins
- [ ] Configure environment variables
- [ ] Set up database backups
- [ ] Enable logging and monitoring
- [ ] Add rate limiting
- [ ] Optimize Docker images
- [ ] Set up CI/CD pipeline

### Deployment Options

1. **Docker Compose** (Recommended for small deployments)
2. **Kubernetes** (For scalable deployments)
3. **Cloud Platforms**: AWS, Google Cloud, Azure
4. **Platform as a Service**: Heroku, Railway, Render

## 📝 Sample Data

The `init_db.py` script includes:
- 50+ diverse questions across categories
- 30+ inspirational quotes with keywords
- Sample player data (optional)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React/Vue.js communities
- PostgreSQL team
- All contributors

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at `/docs`

## 🗺️ Roadmap

- [ ] User authentication with JWT
- [ ] Email notifications
- [ ] Social features (share answers)
- [ ] Mobile app (React Native)
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] AI-powered quote matching
- [ ] Streak tracking
- [ ] Custom question creation

## 📊 Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Pydantic (Data validation)
- Uvicorn (ASGI server)

**Frontend:**
- React/Vue.js (UI framework)
- Axios (HTTP client)
- React Query/Pinia (State management)
- Tailwind CSS (Styling)
- Vite (Build tool)

**DevOps:**
- Docker & Docker Compose
- PostgreSQL container
- Multi-stage builds

---

**Happy Coding! 🎉**

For detailed implementation guidance, see [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)

For architecture details, see [ARCHITECTURE.md](ARCHITECTURE.md)

For project planning, see [PLAN.md](PLAN.md)