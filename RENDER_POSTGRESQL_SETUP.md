# 🐘 Setting Up PostgreSQL on Render

Your players were deleted because **Render's free tier uses ephemeral storage** - SQLite database files are lost when the service restarts or redeploys. PostgreSQL on Render provides persistent storage.

## Step-by-Step Setup Guide

### Step 1: Create PostgreSQL Database on Render

1. **Go to Render Dashboard:** https://dashboard.render.com/
2. **Click "New +"** → Select **"PostgreSQL"**
3. **Configure Database:**
   - **Name:** `dailyquestion-db`
   - **Database:** `dailyquestion_db`
   - **User:** `dailyquestion` (auto-generated)
   - **Region:** Choose closest to your users
   - **Instance Type:** **Free** (0 GB RAM, expires in 90 days but can be renewed)
4. **Click "Create Database"**
5. **Wait for database to be created** (takes ~2 minutes)

### Step 2: Get Database Connection String

1. **In your PostgreSQL database dashboard**, scroll down to **"Connections"**
2. **Copy the "Internal Database URL"** (starts with `postgresql://`)
   - It looks like: `postgresql://user:password@host/database`
   - Example: `postgresql://dailyquestion:abc123xyz@dpg-xxxxx.oregon-postgres.render.com/dailyquestion_db`

### Step 3: Update Your Backend Service Environment Variables

1. **Go to your backend service:** https://dashboard.render.com/web/YOUR_SERVICE_ID
2. **Click "Environment"** in the left sidebar
3. **Find or Add `DATABASE_URL` variable:**
   - **Key:** `DATABASE_URL`
   - **Value:** Paste the Internal Database URL you copied
4. **Click "Save Changes"**

### Step 4: Redeploy Backend

1. **In your backend service**, click **"Manual Deploy"** → **"Deploy latest commit"**
2. **Wait for deployment to complete** (~2-3 minutes)
3. **Check logs** to ensure no errors

### Step 5: Initialize PostgreSQL Database

You need to run the initialization script to create tables and add sample data.

**Option A: Using Render Shell (Recommended)**

1. **In your backend service**, click **"Shell"** tab
2. **Run the initialization command:**
   ```bash
   python init_db.py
   ```
3. **You should see:**
   ```
   Creating database tables...
   Adding sample questions...
   ✓ Added 50 questions
   Adding sample quotes...
   ✓ Added 30 quotes
   ✅ Database initialized successfully!
   ```

**Option B: Using API Endpoint (Alternative)**

Create a temporary initialization endpoint (remove after use):

1. Add this to `backend/app/main.py`:
   ```python
   @app.get("/init-db")
   async def initialize_database():
       from .database import SessionLocal, engine
       from . import models
       
       models.Base.metadata.create_all(bind=engine)
       
       # Run init_db logic here
       return {"message": "Database initialized"}
   ```

2. Visit: `https://dailyquestionsapp.onrender.com/init-db`
3. Remove the endpoint after initialization

### Step 6: Verify Database

Test that your database is working:

```bash
# Check players (should be empty initially)
curl https://dailyquestionsapp.onrender.com/api/players/

# Check questions (should return 50 questions)
curl https://dailyquestionsapp.onrender.com/api/questions/
```

### Step 7: Test Registration

1. **Go to your frontend:** https://daily-questions-app.vercel.app/
2. **Register a new player**
3. **Check if player persists:**
   ```bash
   curl https://dailyquestionsapp.onrender.com/api/players/
   ```

## Important Notes

### ⚠️ Free Tier Limitations

- **PostgreSQL Free Tier expires after 90 days** but can be renewed
- **Database size limit:** 1 GB
- **Connections:** Limited to 97 concurrent connections
- **Backups:** Not included in free tier

### 🔄 Database Persistence

With PostgreSQL:
- ✅ Data persists across service restarts
- ✅ Data persists across redeployments
- ✅ Data is backed up by Render (paid plans)

### 🔐 Security Best Practices

1. **Never commit database URLs to Git**
2. **Use environment variables** for all sensitive data
3. **Rotate credentials** periodically
4. **Use Internal Database URL** (not External) for better security

## Troubleshooting

### Issue: "Could not connect to database"

**Solution:** Check that:
1. DATABASE_URL is correctly set in environment variables
2. You're using the **Internal Database URL** (not External)
3. Backend service has been redeployed after adding DATABASE_URL

### Issue: "Table does not exist"

**Solution:** Run the initialization script:
```bash
python init_db.py
```

### Issue: "Database connection timeout"

**Solution:** 
1. Check database status in Render dashboard
2. Ensure database is in the same region as backend service
3. Wait a few minutes and try again

## Migration from SQLite to PostgreSQL

Your code already supports both! The `database_url` in config automatically handles the connection type.

**SQLite URL format:**
```
sqlite:///./dailyquestion.db
```

**PostgreSQL URL format:**
```
postgresql://user:password@host:5432/database
```

## Next Steps

After PostgreSQL is set up:

1. ✅ Register test players on deployed app
2. ✅ Verify data persists after service restart
3. ✅ Set up Vercel environment variable: `VITE_API_URL=https://dailyquestionsapp.onrender.com`
4. ✅ Test full application flow

## Need Help?

- **Render PostgreSQL Docs:** https://render.com/docs/databases
- **SQLAlchemy PostgreSQL:** https://docs.sqlalchemy.org/en/20/dialects/postgresql.html

---

**Made with Bob** 🤖