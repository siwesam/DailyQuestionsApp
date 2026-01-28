# Quick Setup Guide: AI Quote System

## Prerequisites

- Python 3.9+
- PostgreSQL database (or SQLite for development)
- OpenAI or Anthropic API key

## Step-by-Step Setup

### 1. Install New Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- OpenAI and Anthropic clients
- Web scraping libraries (BeautifulSoup, requests)
- Additional HTTP clients

### 2. Get an AI API Key

**Option A: OpenAI (Recommended for beginners)**
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-`)

**Option B: Anthropic**
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key

### 3. Configure Environment Variables

Edit your `.env` file (or create from `.env.example`):

```bash
# Copy example if needed
cp backend/.env.example backend/.env
```

Add these lines to `.env`:

```env
# For OpenAI
OPENAI_API_KEY=sk-your-actual-key-here
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini

# OR for Anthropic
ANTHROPIC_API_KEY=your-anthropic-key-here
AI_PROVIDER=anthropic
AI_MODEL=claude-3-5-sonnet-20241022
```

**Important:** Never commit your `.env` file to version control!

### 4. Run Database Migration

This adds new fields to the quotes table without losing existing data:

```bash
cd backend
python migrations/add_ai_quote_fields.py
```

You should see:
```
Starting migration: Adding AI-related fields to quotes table...
✓ Added 'source' column
✓ Added 'is_ai_generated' column
✓ Added 'ai_relevance_reason' column
✓ Updated existing quotes
Migration completed successfully!
```

### 5. Verify Setup

Start your backend server:

```bash
cd backend
uvicorn app.main:app --reload
```

Test the AI quote endpoint:

```bash
# Replace {player_id} with an actual player ID from your database
curl http://localhost:8000/api/quotes/match/{player_id}?use_ai=true
```

### 6. (Optional) Seed Initial Quotes

If you don't have quotes yet:

```bash
cd backend
python init_db.py
```

## Testing the AI System

### Test 1: Basic AI Selection

1. Create a player and answer some questions
2. Request a quote:
   ```bash
   curl http://localhost:8000/api/quotes/match/{player_id}?use_ai=true
   ```
3. Check the response includes `ai_relevance_reason`

### Test 2: Fallback to Keyword Matching

Disable AI to test fallback:
```bash
curl http://localhost:8000/api/quotes/match/{player_id}?use_ai=false
```

### Test 3: New Quote Fetching

1. Answer questions with specific themes (e.g., about "career", "growth")
2. Request a quote
3. Check logs to see if new quotes were fetched from the internet

## Common Issues

### Issue: "OpenAI API key not found"

**Solution:** 
- Check `.env` file has `OPENAI_API_KEY=sk-...`
- Restart the backend server after adding the key
- Verify the key is valid on OpenAI dashboard

### Issue: "Migration failed"

**Solution:**
```bash
# Check if columns already exist
psql -d your_database -c "\d quotes"

# If needed, rollback and retry
python migrations/add_ai_quote_fields.py --downgrade
python migrations/add_ai_quote_fields.py
```

### Issue: "No quotes available"

**Solution:**
```bash
# Seed initial quotes
python backend/init_db.py

# Or add quotes manually via API
curl -X POST http://localhost:8000/api/quotes/ \
  -H "Content-Type: application/json" \
  -d '{
    "quote_text": "Your quote here",
    "author": "Author Name",
    "keywords": "keyword1, keyword2"
  }'
```

### Issue: Web scraping not working

**Solution:**
- Check internet connectivity
- Verify source websites are accessible
- Check logs for specific errors
- System will fall back to existing quotes if scraping fails

## Cost Management

### Monitor API Usage

**OpenAI:**
- Dashboard: https://platform.openai.com/usage
- Set usage limits in account settings

**Anthropic:**
- Dashboard: https://console.anthropic.com/settings/usage
- Monitor credits and usage

### Estimated Costs

**Per quote selection:**
- OpenAI (gpt-4o-mini): ~$0.001-0.003
- Anthropic (claude-3-5-sonnet): ~$0.01-0.03

**For 1000 daily active users:**
- OpenAI: ~$1-3 per day
- Anthropic: ~$10-30 per day

### Cost Optimization Tips

1. **Use gpt-4o-mini** for production (cheaper, still good quality)
2. **Cache AI analyses** for frequently accessed players
3. **Set rate limits** on the API endpoint
4. **Monitor usage** regularly

## Next Steps

1. ✅ Setup complete
2. Test with real player data
3. Monitor AI selection quality
4. Adjust relevance threshold if needed
5. Review AI-fetched quotes periodically

## Support

- Full documentation: See `AI_QUOTE_SYSTEM.md`
- Check logs: `backend/logs/`
- API documentation: http://localhost:8000/docs

---

Made with Bob