# Deployment Environment Variables Setup Guide

## Setting Up Environment Variables on Render

### Step 1: Access Your Render Dashboard

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Log in to your account
3. Find your backend web service (the one running your FastAPI app)

### Step 2: Navigate to Environment Variables

1. Click on your backend service name
2. In the left sidebar, click on **"Environment"**
3. You'll see a section called **"Environment Variables"**

### Step 3: Add Required Environment Variables

Add the following environment variables one by one by clicking **"Add Environment Variable"**:

#### Required Variables:

1. **DATABASE_URL**
   - Key: `DATABASE_URL`
   - Value: Your PostgreSQL connection string from Render
   - Format: `postgresql://user:password@host:port/database`
   - Example: `postgresql://myuser:mypassword@dpg-xxxxx.oregon-postgres.render.com/mydb`

2. **OPENAI_API_KEY**
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key (starts with `sk-`)
   - Get it from: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Example: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: A secure random string for JWT token signing
   - Generate one using: `openssl rand -hex 32`
   - Example: `09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7`

4. **FRONTEND_URL**
   - Key: `FRONTEND_URL`
   - Value: Your Vercel frontend URL
   - Example: `https://your-app-name.vercel.app`

#### Optional Variables (with defaults):

5. **ALGORITHM**
   - Key: `ALGORITHM`
   - Value: `HS256`
   - (This is the default, only add if you want to change it)

6. **ACCESS_TOKEN_EXPIRE_MINUTES**
   - Key: `ACCESS_TOKEN_EXPIRE_MINUTES`
   - Value: `30`
   - (This is the default, only add if you want to change it)

### Step 4: Save and Deploy

1. After adding all variables, click **"Save Changes"**
2. Render will automatically redeploy your service with the new environment variables
3. Wait for the deployment to complete (usually 2-5 minutes)

### Step 5: Verify Environment Variables

You can verify the variables are set correctly by:

1. Checking the **"Logs"** tab in your Render service
2. Looking for any startup errors related to missing environment variables
3. Testing your API endpoints at `https://your-backend-url.onrender.com/docs`

## Setting Up Environment Variables on Vercel (Frontend)

### Step 1: Access Your Vercel Dashboard

1. Go to [https://vercel.com/dashboard](https://vercel.com/dashboard)
2. Find your frontend project
3. Click on it to open the project settings

### Step 2: Navigate to Environment Variables

1. Click on **"Settings"** in the top navigation
2. Click on **"Environment Variables"** in the left sidebar

### Step 3: Add Frontend Environment Variables

Add the following environment variable:

1. **VITE_API_URL**
   - Key: `VITE_API_URL`
   - Value: Your Render backend URL
   - Example: `https://your-backend-name.onrender.com`
   - Environment: Select **"Production"**, **"Preview"**, and **"Development"**

### Step 4: Redeploy

1. After adding the variable, go to the **"Deployments"** tab
2. Click on the three dots (...) next to the latest deployment
3. Click **"Redeploy"**
4. Wait for the deployment to complete

## Quick Reference: All Environment Variables

### Backend (Render)
```
DATABASE_URL=postgresql://user:password@host:port/database
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SECRET_KEY=your-secret-key-here
FRONTEND_URL=https://your-app-name.vercel.app
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (Vercel)
```
VITE_API_URL=https://your-backend-name.onrender.com
```

## How to Get Your OpenAI API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **"Create new secret key"**
4. Give it a name (e.g., "DailyQuestions App")
5. Copy the key immediately (you won't be able to see it again)
6. Add it to your Render environment variables

## How to Generate a Secure SECRET_KEY

Run this command in your terminal:
```bash
openssl rand -hex 32
```

Or use Python:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Troubleshooting

### Backend won't start after adding variables
- Check the Render logs for specific error messages
- Verify DATABASE_URL format is correct
- Ensure OPENAI_API_KEY starts with `sk-`

### Frontend can't connect to backend
- Verify VITE_API_URL doesn't have a trailing slash
- Check that FRONTEND_URL in backend matches your Vercel URL
- Verify CORS settings in backend allow your frontend URL

### OpenAI API errors
- Verify your OpenAI API key is valid
- Check you have credits in your OpenAI account
- Ensure the key has the correct permissions

## Security Notes

⚠️ **IMPORTANT**: 
- Never commit `.env` files to Git
- Never share your API keys publicly
- Rotate your SECRET_KEY periodically
- Use different keys for development and production
- Monitor your OpenAI API usage to avoid unexpected charges

## Next Steps

After setting up environment variables:

1. Run the database migration on production:
   ```bash
   # Connect to your Render shell
   python backend/migrations/add_ai_quote_fields.py
   ```

2. Test the AI quote matching feature:
   - Answer some questions in your app
   - Check if quotes are being matched correctly
   - Monitor the logs for any errors

3. Monitor your OpenAI API usage:
   - Go to [https://platform.openai.com/usage](https://platform.openai.com/usage)
   - Set up usage alerts if needed