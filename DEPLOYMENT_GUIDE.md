# 🚀 Deployment Guide - Daily Questions App

This guide covers multiple options for deploying your Python web app online.

## Table of Contents
1. [Quick Deploy Options (Free)](#quick-deploy-options-free)
2. [Production Deployment](#production-deployment)
3. [Environment Configuration](#environment-configuration)
4. [Post-Deployment Steps](#post-deployment-steps)

---

## Quick Deploy Options (Free)

### Option 1: Render.com (Recommended for Beginners)

**Pros:** Free tier, easy setup, automatic HTTPS, supports both frontend and backend

#### Backend Deployment on Render:

1. **Create a Render account** at https://render.com

2. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

3. **Create a new Web Service on Render:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** daily-questions-api
     - **Environment:** Python 3
     - **Build Command:** `cd backend && pip install -r requirements.txt`
     - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type:** Free

4. **Add Environment Variables:**
   - `DATABASE_URL`: `sqlite:///./dailyquestion.db` (or use PostgreSQL)
   - `SECRET_KEY`: Generate a secure random string
   - `PYTHON_VERSION`: `3.11.0`

5. **Initialize Database:**
   - After deployment, use Render's Shell to run:
   ```bash
   cd backend && python init_db.py
   ```

#### Frontend Deployment on Render:

1. **Create a new Static Site:**
   - Click "New +" → "Static Site"
   - Connect same GitHub repository
   - Configure:
     - **Name:** daily-questions-app
     - **Build Command:** `cd frontend && npm install && npm run build`
     - **Publish Directory:** `frontend/dist`

2. **Add Environment Variable:**
   - `VITE_API_URL`: Your backend URL (e.g., `https://daily-questions-api.onrender.com`)

---

### Option 2: Railway.app

**Pros:** Simple deployment, free tier, automatic HTTPS

1. **Sign up at** https://railway.app

2. **Deploy Backend:**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python
   - Add environment variables in Settings
   - Backend will be available at: `https://your-app.up.railway.app`

3. **Deploy Frontend:**
   - Create another service for frontend
   - Set build command: `cd frontend && npm install && npm run build`
   - Set start command: `npx serve -s frontend/dist`

---

### Option 3: Vercel (Frontend) + Render (Backend)

**Best for:** Separate frontend/backend deployment

#### Backend on Render (see Option 1)

#### Frontend on Vercel:

1. **Sign up at** https://vercel.com

2. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

3. **Deploy:**
   ```bash
   cd frontend
   vercel
   ```

4. **Configure:**
   - Set environment variable: `VITE_API_URL` to your backend URL
   - Vercel will provide a URL like: `https://your-app.vercel.app`

---

## Production Deployment

### Option 4: DigitalOcean / AWS / Google Cloud

For production with more control:

#### 1. Prepare for Production:

**Update backend/app/config.py:**
```python
class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./dailyquestion.db")
    secret_key: str = os.getenv("SECRET_KEY", "change-this-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Production settings
    cors_origins: list = ["https://your-frontend-domain.com"]
    
    class Config:
        env_file = ".env"
```

**Update backend/app/main.py CORS:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Use from config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2. Use PostgreSQL (Recommended for Production):

**Update requirements.txt:**
```
psycopg2-binary==2.9.9
```

**Update DATABASE_URL:**
```
postgresql://user:password@host:5432/database_name
```

#### 3. Deploy with Docker:

We already have Docker files! Use them:

```bash
# Build and run with Docker Compose
docker-compose up -d
```

#### 4. Set up on a VPS (DigitalOcean Droplet):

```bash
# SSH into your server
ssh root@your-server-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone your repository
git clone YOUR_REPO_URL
cd DummyPythonApp

# Set environment variables
nano .env
# Add: DATABASE_URL, SECRET_KEY, etc.

# Run with Docker Compose
docker-compose up -d

# Set up Nginx as reverse proxy
sudo apt install nginx
sudo nano /etc/nginx/sites-available/dailyquestions
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site and restart Nginx
sudo ln -s /etc/nginx/sites-available/dailyquestions /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Set up SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Environment Configuration

### Production Environment Variables:

Create `.env` file in backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Security
SECRET_KEY=your-super-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["https://your-frontend-domain.com"]
```

### Generate Secure SECRET_KEY:

```python
import secrets
print(secrets.token_urlsafe(32))
```

Or in terminal:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Post-Deployment Steps

### 1. Initialize Database:

```bash
# On your server or in Render Shell
cd backend
python init_db.py
```

### 2. Test Your Deployment:

```bash
# Test backend
curl https://your-backend-url.com/api/players/

# Test frontend
# Open https://your-frontend-url.com in browser
```

### 3. Monitor Your App:

- Check logs in Render/Railway dashboard
- Set up error tracking (e.g., Sentry)
- Monitor database size

### 4. Set Up Backups:

```bash
# Backup SQLite database
cp backend/dailyquestion.db backend/dailyquestion.db.backup

# For PostgreSQL
pg_dump DATABASE_URL > backup.sql
```

---

## Recommended: Easiest Path to Deploy

**For your first deployment, I recommend:**

1. **Backend:** Render.com (Free tier)
   - Automatic HTTPS
   - Easy database management
   - Simple environment variables

2. **Frontend:** Vercel (Free tier)
   - Automatic deployments from Git
   - Global CDN
   - Perfect for React apps

**Total cost:** $0/month for hobby projects!

---

## Quick Start Commands:

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Ready for deployment"
git branch -M main
git remote add origin YOUR_GITHUB_URL
git push -u origin main

# 2. Deploy backend on Render.com (via web interface)

# 3. Deploy frontend on Vercel
cd frontend
npm install -g vercel
vercel

# 4. Update frontend environment variable
# Set VITE_API_URL to your Render backend URL

# 5. Redeploy frontend
vercel --prod
```

---

## Need Help?

- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app

Your app is now ready to be deployed online! 🚀