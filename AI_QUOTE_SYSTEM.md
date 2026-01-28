# AI Quote Selection System

## Overview

The Daily Question App now features an intelligent AI-powered quote selection system that can:
- Analyze player's recent answers to understand their context and themes
- Evaluate existing quotes for relevance
- Automatically fetch new quotes from the internet when existing ones aren't relevant enough
- Provide explanations for why quotes were selected

## Architecture

### Components

1. **AI Quote Agent** (`backend/app/services/ai_quote_agent.py`)
   - Main orchestrator for intelligent quote selection
   - Analyzes player context using AI
   - Evaluates quote relevance
   - Decides when to fetch new quotes

2. **Quote Scraper** (`backend/app/services/quote_scraper.py`)
   - Fetches quotes from online sources (BrainyQuote, Goodreads)
   - Handles web scraping with proper error handling
   - Rate limiting to be respectful to source websites

3. **Enhanced Database Schema**
   - New fields in `quotes` table:
     - `source`: URL or 'manual' for quote origin
     - `is_ai_generated`: Flag (0=manual, 1=AI-fetched)
     - `ai_relevance_reason`: AI's explanation for relevance

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New dependencies added:
- `openai==1.12.0` - OpenAI API client
- `anthropic==0.18.1` - Anthropic API client
- `beautifulsoup4==4.12.3` - Web scraping
- `requests==2.31.0` - HTTP requests
- `lxml==5.1.0` - HTML parsing
- `httpx==0.26.0` - Async HTTP client

### 2. Configure AI Provider

Add to your `.env` file:

```env
# AI Configuration
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini
```

**Supported Providers:**
- `openai` with models: `gpt-4o-mini`, `gpt-4o`, `gpt-4-turbo`
- `anthropic` with models: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`

### 3. Run Database Migration

```bash
cd backend
python migrations/add_ai_quote_fields.py
```

This will add the new fields to the `quotes` table without losing existing data.

## How It Works

### Quote Selection Flow

1. **Player Context Analysis**
   - Retrieves player's answers from the last 7 days
   - AI analyzes answers to extract:
     - Main themes (3-5 themes)
     - Key topics/keywords (5-10 keywords)
     - Overall sentiment (positive, negative, neutral, mixed)

2. **Existing Quote Evaluation**
   - AI evaluates all existing quotes in the database
   - Assigns relevance scores (0.0 to 1.0)
   - Provides reasoning for each score

3. **Decision Point**
   - If best existing quote score >= 0.7: Use that quote
   - If best existing quote score < 0.7: Fetch new quotes

4. **New Quote Fetching** (when needed)
   - AI generates 3-5 search topics based on player context
   - Scraper fetches quotes from multiple sources
   - New quotes are saved to database
   - AI evaluates new quotes
   - Best quote is selected

5. **Response**
   - Returns selected quote with:
     - Quote text and author
     - Relevance score
     - AI's explanation for why it's relevant

## API Usage

### Get AI-Selected Quote

```http
GET /api/quotes/match/{player_id}?use_ai=true
```

**Parameters:**
- `player_id` (required): Player's unique ID
- `use_ai` (optional, default=true): Enable AI selection

**Response:**
```json
{
  "id": 123,
  "quote_text": "The only way to do great work is to love what you do.",
  "author": "Steve Jobs",
  "category": "motivation",
  "keywords": "work, passion, excellence",
  "created_at": "2024-01-28T10:00:00Z",
  "source": "https://www.brainyquote.com/topics/motivation-quotes",
  "is_ai_generated": 1,
  "ai_relevance_reason": "This quote aligns with your recent reflections on finding purpose in your career and pursuing meaningful work.",
  "relevance_score": 0.92
}
```

### Fallback to Simple Matching

```http
GET /api/quotes/match/{player_id}?use_ai=false
```

Falls back to keyword-based matching if AI is disabled or fails.

## Configuration Options

### AI Provider Selection

**OpenAI (Recommended for cost-effectiveness):**
```env
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini  # Fast and affordable
```

**Anthropic (Recommended for quality):**
```env
AI_PROVIDER=anthropic
AI_MODEL=claude-3-5-sonnet-20241022  # High quality analysis
```

### Relevance Threshold

The system fetches new quotes when existing ones score below 0.7. To adjust this, modify `should_fetch_new_quotes()` in `ai_quote_agent.py`:

```python
def should_fetch_new_quotes(self, best_existing_score: float, threshold: float = 0.7):
    return best_existing_score < threshold
```

## Cost Considerations

### AI API Costs

**OpenAI (gpt-4o-mini):**
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens
- Estimated cost per quote selection: $0.001-0.003

**Anthropic (claude-3-5-sonnet):**
- ~$3.00 per 1M input tokens
- ~$15.00 per 1M output tokens
- Estimated cost per quote selection: $0.01-0.03

### Web Scraping

- Free (respects robots.txt and rate limits)
- Adds 1-2 second delay between requests
- Fetches max 5 quotes per topic

## Monitoring and Logging

The system logs important events:

```python
logger.info(f"AI Quote Agent selecting quote for player: {player_id}")
logger.info(f"Player context: {player_context}")
logger.info(f"Best existing quote score: {best_score}")
logger.info(f"Fetching new quotes from internet...")
logger.error(f"AI quote selection failed: {e}")
```

Check logs for:
- Quote selection decisions
- AI API errors
- Web scraping issues
- Fallback activations

## Error Handling

The system has multiple fallback layers:

1. **AI Failure**: Falls back to keyword matching
2. **Web Scraping Failure**: Uses existing quotes only
3. **No Quotes Available**: Returns appropriate error message

## Best Practices

### 1. Seed Initial Quotes

Start with a diverse set of manual quotes:

```bash
python backend/init_db.py
```

This ensures the system has quotes to work with initially.

### 2. Monitor AI Costs

Track API usage in your AI provider dashboard:
- OpenAI: https://platform.openai.com/usage
- Anthropic: https://console.anthropic.com/settings/usage

### 3. Rate Limiting

The scraper includes delays to avoid overwhelming source websites. Don't modify these without good reason.

### 4. Quote Quality

Periodically review AI-fetched quotes:

```sql
SELECT * FROM quotes WHERE is_ai_generated = 1 ORDER BY created_at DESC LIMIT 20;
```

Remove low-quality quotes if needed.

## Troubleshooting

### AI Selection Not Working

1. Check API keys are set correctly in `.env`
2. Verify API key has sufficient credits
3. Check logs for specific error messages
4. Test with `use_ai=false` to verify fallback works

### Web Scraping Failures

1. Check internet connectivity
2. Verify source websites are accessible
3. Check if website structure has changed
4. Review scraper logs for specific errors

### Database Migration Issues

If migration fails:

```bash
# Rollback
python backend/migrations/add_ai_quote_fields.py --downgrade

# Try again
python backend/migrations/add_ai_quote_fields.py
```

## Future Enhancements

Potential improvements:
- [ ] Add more quote sources
- [ ] Implement caching for AI analyses
- [ ] Add user feedback on quote relevance
- [ ] Support multiple languages
- [ ] Add quote categories/tags
- [ ] Implement A/B testing for AI vs. keyword matching

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Rate Limiting**: Implement rate limiting on the API endpoint
3. **Input Validation**: Player answers are sanitized before AI processing
4. **Web Scraping**: Respects robots.txt and terms of service

## Support

For issues or questions:
1. Check logs in `backend/logs/`
2. Review this documentation
3. Check API provider status pages
4. Contact development team

---

Made with Bob - AI-Powered Quote Selection System