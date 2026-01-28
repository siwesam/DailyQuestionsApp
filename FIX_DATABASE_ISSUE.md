# 🔧 Fix: Database Keeps Getting Deleted

## The Problem

Your players keep disappearing because **Render's free tier deletes SQLite files** when the service restarts or goes to sleep (after 15 minutes of inactivity).

## The Solution: Switch to PostgreSQL

Your backend code **already auto-initializes** the database on startup, so this is easy!

---

## Step-by-Step Fix (No Shell Access Needed!)

### Step 1: Create PostgreSQL Database on Render

1. Go to: https://dashboard.render.com/
2. Click **"New +"** → Select **"PostgreSQL"**
3. Fill in:
   - **Name:** `dailyquestion-db`
   - **Database:** `dailyquestion_db`
   - **Region:** Oregon (US West) or closest to you
   - **PostgreSQL Version:** 16 (latest)
   - **Instance Type:** **Free**
4. Click **"Create Database"**
5. Wait ~2 minutes for it to be ready

### Step 2: Copy Database URL

1. In your new PostgreSQL database page, scroll to **"Connections"** section
2. Find **"Internal Database URL"**
3. Click the **copy icon** to copy the full URL
   - It looks like: `postgresql://dailyquestion_user:abc123xyz@dpg-xxxxx-a.oregon-postgres.render.com/dailyquestion_db`

### Step 3: Update Backend Environment Variable

1. Go to your backend service: https://dashboard.render.com/web/YOUR_SERVICE
2. Click **"Environment"** in the left sidebar
3. Find the `DATABASE_URL` variable (or add it if missing):
   - **Key:** `DATABASE_URL`
   - **Value:** Paste the Internal Database URL you copied
4. Click **"Save Changes"**

### Step 4: Redeploy Backend

1. Still in your backend service, click **"Manual Deploy"** dropdown (top right)
2. Select **"Deploy latest commit"**
3. Wait for deployment to complete (~2-3 minutes)
4. **Watch the logs** - you should see:
   ```
   Initializing database with sample data...
   ✅ Database initialized with 50 questions and 32 quotes
   ```

### Step 5: Verify It Works

Test your API:

```bash
# Check questions (should return 50 questions)
curl https://dailyquestionsapp.onrender.com/api/questions/

# Check players (should be empty initially)
curl https://dailyquestionsapp.onrender.com/api/players/
```

### Step 6: Update Frontend (If Needed)

If your frontend isn't connecting to the backend:

1. Go to: https://vercel.com/wesam-ibraheems-projects/daily-questions-app/settings/environment-variables
2. Add or update:
   - **Key:** `VITE_API_URL`
   - **Value:** `https://dailyquestionsapp.onrender.com`
3. Go to **Deployments** tab
4. Click **"..."** on latest deployment → **"Redeploy"**

### Step 7: Test Your App!

1. Go to: https://daily-questions-app.vercel.app/
2. Register a new player
3. Answer some questions
4. **Restart your Render backend** (to test persistence):
   - Go to backend service
   - Click "Manual Deploy" → "Clear build cache & deploy"
5. Check if your player still exists:
   ```bash
   curl https://dailyquestionsapp.onrender.com/api/players/
   ```

✅ **Your player should still be there!**

---

## Why This Works

### Before (SQLite):
- ❌ File stored on Render's temporary disk
- ❌ Deleted when service restarts/sleeps
- ❌ Data lost forever

### After (PostgreSQL):
- ✅ Data stored in separate database service
- ✅ Persists across restarts
- ✅ Persists across redeployments
- ✅ Free tier (90 days, renewable)

---

## Important Notes

### Auto-Initialization
Your backend automatically:
- Creates all database tables on startup
- Adds 50 sample questions
- Adds 32 inspirational quotes
- **Only if the database is empty** (won't duplicate data)

### Free Tier Limits
- **PostgreSQL Free:** 1 GB storage, 90 days (renewable)
- **Render Web Service Free:** Sleeps after 15 min inactivity
- **Total Cost:** $0/month

### Database URL Format
- **SQLite (old):** `sqlite:///./dailyquestion.db`
- **PostgreSQL (new):** `postgresql://user:pass@host:5432/database`

Your code automatically detects which one to use!

---

## Troubleshooting

### "Database not initializing"
**Check logs** in Render dashboard. Look for:
- ✅ `Database initialized with 50 questions`
- ❌ Any error messages

### "Can't connect to database"
1. Verify `DATABASE_URL` is set correctly
2. Use **Internal Database URL** (not External)
3. Redeploy backend after changing environment variables

### "Still losing data"
1. Confirm you're using PostgreSQL URL (starts with `postgresql://`)
2. Check PostgreSQL database status in Render dashboard
3. Verify backend logs show successful initialization

---

## Next Steps After Setup

1. ✅ Test player registration
2. ✅ Answer some questions
3. ✅ Check if data persists after restart
4. ✅ Share your app with friends!

---

**Your database will now persist forever!** 🎉

Made with Bob 🤖