# 🔧 Fix Vercel Deployment - Environment Variable

Your app is almost working! You just need to configure the backend URL in Vercel.

## Problem
The frontend doesn't know where your backend is located, so it's getting 404 errors.

## Solution (2 minutes)

### Step 1: Add Environment Variable in Vercel

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Click on your `daily-questions-app` project

2. **Open Settings**
   - Click "Settings" tab at the top
   - Click "Environment Variables" in the left sidebar

3. **Add the Backend URL**
   - Click "Add New" button
   - Fill in:
     - **Key:** `VITE_API_URL`
     - **Value:** `https://dailyquestionsapp.onrender.com`
     - **Environments:** Check all three (Production, Preview, Development)
   - Click "Save"

### Step 2: Redeploy Frontend

1. **Go to Deployments Tab**
   - Click "Deployments" at the top
   - Find the latest deployment (should be at the top)

2. **Trigger Redeploy**
   - Click the three dots "..." on the right side
   - Click "Redeploy"
   - Confirm by clicking "Redeploy" again

3. **Wait for Deployment**
   - Should take 1-2 minutes
   - You'll see "Building..." then "Ready"

### Step 3: Test Your App

1. **Visit Your App**
   - Go to: https://daily-questions-app.vercel.app
   - Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

2. **Test Registration**
   - Register a new player with username and password
   - Should work now!

3. **Test Questions**
   - Answer a question
   - Click "Get Your Personalized Quote"
   - Should show a quote! 🎉

---

## Why This Happened

The frontend code uses this line:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

Without the `VITE_API_URL` environment variable, it defaults to `localhost:8000`, which doesn't exist in production.

---

## Verification

After redeployment, open browser console (F12) and check:
- Network tab should show requests to `https://dailyquestionsapp.onrender.com`
- No more 404 errors
- Successful API responses

---

## Still Having Issues?

If you still see errors after following these steps:

1. **Check Backend is Running**
   - Visit: https://dailyquestionsapp.onrender.com/docs
   - Should see API documentation

2. **Check Environment Variable**
   - In Vercel Settings → Environment Variables
   - Verify `VITE_API_URL` is set correctly
   - Make sure it's enabled for "Production"

3. **Clear Browser Cache**
   - Hard refresh: `Ctrl+Shift+R` or `Cmd+Shift+R`
   - Or open in incognito/private window

4. **Check Browser Console**
   - Press F12
   - Look for error messages
   - Share them if you need more help

---

**Your app will be fully functional after this! 🚀**