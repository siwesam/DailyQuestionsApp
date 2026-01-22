# 📋 Deployment Checklist

Use this checklist to deploy your Daily Questions App online.

## ✅ Pre-Deployment Checklist

### Code Preparation
- [ ] All code committed to Git
- [ ] `.gitignore` includes sensitive files
- [ ] Environment variables documented
- [ ] Database initialization script tested
- [ ] All dependencies in requirements.txt and package.json

### Security
- [ ] Generate new SECRET_KEY for production
- [ ] Update CORS origins to production domains
- [ ] Remove any hardcoded passwords or secrets
- [ ] Review and update .env.example

### Testing
- [ ] App runs locally without errors
- [ ] Registration works with password
- [ ] Login works with correct/incorrect passwords
- [ ] Questions load and answers save
- [ ] Quotes display correctly

---

## 🚀 Easiest Deployment Path (Recommended)

### Step 1: Push to GitHub (5 minutes)

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

**Checklist:**
- [ ] Code pushed to GitHub
- [ ] Repository is public or connected to deployment service

---

### Step 2: Deploy Backend on Render.com (10 minutes)

1. **Sign up:** https://render.com
   - [ ] Account created

2. **Create Web Service:**
   - [ ] Click "New +" → "Web Service"
   - [ ] Connect GitHub repository
   - [ ] Select repository

3. **Configure Service:**
   ```
   Name: daily-questions-api
   Environment: Python 3
   Build Command: cd backend && pip install -r requirements.txt
   Start Command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```
   - [ ] Configuration entered

4. **Add Environment Variables:**
   ```
   DATABASE_URL=sqlite:///./dailyquestion.db
   SECRET_KEY=<generate-new-secret-key>
   PYTHON_VERSION=3.11.0
   ```
   - [ ] Environment variables added
   - [ ] New SECRET_KEY generated

5. **Deploy:**
   - [ ] Click "Create Web Service"
   - [ ] Wait for deployment (5-10 minutes)
   - [ ] Note your backend URL: `https://YOUR-APP.onrender.com`
   - [ ] Database will auto-initialize on first startup! ✨

6. **Verify Deployment:**
   - [ ] Check deployment logs - should see "Database initialized with 50 questions and 32 quotes"
   - [ ] Test API: `curl https://YOUR-APP.onrender.com/api/players/`
   - [ ] Visit API docs: `https://YOUR-APP.onrender.com/docs`

**Note:** No shell access needed! The app automatically initializes the database on startup. 🎉

---

### Step 3: Deploy Frontend on Vercel (5 minutes)

1. **Sign up:** https://vercel.com
   - [ ] Account created
   - [ ] GitHub connected

2. **Import Project:**
   - [ ] Click "Add New..." → "Project"
   - [ ] Import your GitHub repository
   - [ ] Select repository

3. **Configure:**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```
   - [ ] Configuration set

4. **Add Environment Variable:**
   ```
   VITE_API_URL=https://YOUR-BACKEND.onrender.com
   ```
   - [ ] Environment variable added (use your Render URL)

5. **Deploy:**
   - [ ] Click "Deploy"
   - [ ] Wait for deployment (2-3 minutes)
   - [ ] Note your frontend URL: `https://YOUR-APP.vercel.app`

---

### Step 4: Test Your Deployed App (5 minutes)

1. **Open your frontend URL**
   - [ ] Frontend loads without errors
   - [ ] Can see player list/registration

2. **Test Registration:**
   - [ ] Register a new user with password
   - [ ] Registration successful
   - [ ] Redirected to questions

3. **Test Login:**
   - [ ] Go back to home
   - [ ] Click on your user
   - [ ] Enter password
   - [ ] Login successful

4. **Test Features:**
   - [ ] Can answer questions
   - [ ] Can get quotes
   - [ ] Can view answer history
   - [ ] "Get Another Quote" works

---

## 🎉 Deployment Complete!

Your app is now live at:
- **Frontend:** https://YOUR-APP.vercel.app
- **Backend API:** https://YOUR-BACKEND.onrender.com
- **API Docs:** https://YOUR-BACKEND.onrender.com/docs

---

## 📱 Share Your App

Share these URLs with friends:
- **App:** https://YOUR-APP.vercel.app
- **Test Account:** username: `testuser`, password: `test123`

---

## 🔧 Post-Deployment

### Monitor Your App
- [ ] Check Render logs for backend errors
- [ ] Check Vercel logs for frontend errors
- [ ] Test on mobile devices
- [ ] Test on different browsers

### Optional Improvements
- [ ] Set up custom domain
- [ ] Add Google Analytics
- [ ] Set up error tracking (Sentry)
- [ ] Upgrade to PostgreSQL database
- [ ] Add email notifications
- [ ] Set up automated backups

---

## 🆘 Troubleshooting

### Backend Issues:
- **500 Error:** Check Render logs, verify environment variables
- **Database Error:** Re-run `python init_db.py` in Render Shell
- **CORS Error:** Update CORS origins in backend config

### Frontend Issues:
- **API Connection Failed:** Verify VITE_API_URL is correct
- **Build Failed:** Check package.json and dependencies
- **Blank Page:** Check browser console for errors

### Common Fixes:
```bash
# Redeploy backend
git push origin main  # Render auto-deploys

# Redeploy frontend
vercel --prod

# Check backend health
curl https://YOUR-BACKEND.onrender.com/api/players/

# View backend logs
# Go to Render dashboard → Your service → Logs
```

---

## 📞 Need Help?

- **Render Support:** https://render.com/docs
- **Vercel Support:** https://vercel.com/docs
- **Check logs** in respective dashboards
- **Review DEPLOYMENT_GUIDE.md** for detailed instructions

---

**Estimated Total Time:** 25-30 minutes
**Total Cost:** $0 (Free tier)

Good luck with your deployment! 🚀