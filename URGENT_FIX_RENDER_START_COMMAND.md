# URGENT: Update Render Start Command

## The Problem
The startup script isn't running because Render is still using the old start command.

## The Solution - Update Start Command in Render

### Step-by-Step Instructions:

1. **Go to Render Dashboard**
   - Open https://dashboard.render.com
   - Log in to your account

2. **Find Your Backend Service**
   - Click on your backend web service (the FastAPI app)

3. **Go to Settings**
   - Click on **"Settings"** in the left sidebar

4. **Find Build & Deploy Section**
   - Scroll down to the **"Build & Deploy"** section

5. **Update Start Command**
   - Find the field labeled **"Start Command"**
   - It currently probably says:
     ```
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Change it to:**
     ```
     cd backend && chmod +x startup.sh && ./startup.sh
     ```

6. **Save Changes**
   - Click the **"Save Changes"** button at the bottom
   - Render will automatically trigger a new deployment

7. **Watch the Logs**
   - Go to the **"Logs"** tab
   - You should now see:
     ```
     ==========================================
     Starting application initialization...
     ==========================================
     Creating database tables...
     ✓ Tables created successfully
     Running database migrations...
     Starting migration: Adding AI-related fields to quotes table...
     Detected PostgreSQL database
     ✓ Added 'source' column
     ✓ Added 'is_ai_generated' column  
     ✓ Added 'ai_relevance_reason' column
     ✓ Updated existing quotes
     Migration completed successfully!
     Checking database initialization...
     Database already has 50 questions. Skipping initialization.
     ==========================================
     Starting FastAPI application...
     ==========================================
     ```

8. **Test Your App**
   - Wait for deployment to complete (2-5 minutes)
   - Go to your app and try to get a quote
   - It should work now!

## Visual Guide

```
Render Dashboard
  └─ Your Backend Service
      └─ Settings (left sidebar)
          └─ Build & Deploy section
              └─ Start Command field
                  └─ Change to: cd backend && chmod +x startup.sh && ./startup.sh
                      └─ Click "Save Changes"
```

## What This Does

The new start command:
1. `cd backend` - Changes to the backend directory
2. `chmod +x startup.sh` - Makes the script executable
3. `./startup.sh` - Runs the startup script which:
   - Creates database tables
   - Runs migrations to add AI quote columns
   - Initializes database with questions
   - Starts the FastAPI application

## Troubleshooting

### "Command not found" error
- Make sure you're using `./startup.sh` not just `startup.sh`
- The `chmod +x` should make it executable

### Still not seeing migration logs
- Double-check you saved the changes
- Make sure the deployment completed
- Check you're looking at the latest logs (refresh the page)

### Migration fails
- Share the error message
- We can run it manually from your local machine

## Alternative: Manual Migration (If Needed)

If the automatic migration still doesn't work, you can run it manually:

1. Get your production DATABASE_URL from Render:
   - Go to your PostgreSQL database in Render
   - Copy the "External Database URL"

2. Run from your local machine:
   ```bash
   export DATABASE_URL="your-production-database-url-here"
   cd backend
   python migrations/add_ai_quote_fields.py
   unset DATABASE_URL
   ```

This will add the missing columns directly to your production database.