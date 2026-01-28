"""
AI Quote Agent - Intelligently selects or generates quotes based on player answers.
"""
import json
import logging
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session

from ..config import settings
from ..models import Quote, Answer
from ..schemas import QuoteCreate
from .. import crud
from .quote_scraper import quote_scraper

logger = logging.getLogger(__name__)


class AIQuoteAgent:
    """
    AI agent that intelligently selects quotes from the database or fetches new ones
    from the internet based on relevance to player's answers.
    """
    
    def __init__(self):
        self.provider = settings.ai_provider
        self.model = settings.ai_model
        self._client = None
    
    def _get_client(self):
        """Lazy initialization of AI client."""
        if self._client is None:
            if self.provider == "openai":
                try:
                    from openai import OpenAI
                    self._client = OpenAI(api_key=settings.openai_api_key)
                except Exception as e:
                    logger.error(f"Failed to initialize OpenAI client: {e}")
                    raise
            elif self.provider == "anthropic":
                try:
                    from anthropic import Anthropic
                    self._client = Anthropic(api_key=settings.anthropic_api_key)
                except Exception as e:
                    logger.error(f"Failed to initialize Anthropic client: {e}")
                    raise
            else:
                raise ValueError(f"Unsupported AI provider: {self.provider}")
        return self._client
    
    def _call_ai(self, system_prompt: str, user_prompt: str, log_callback=None) -> str:
        """
        Call the AI provider with the given prompts.
        
        Args:
            system_prompt: System instructions for the AI
            user_prompt: User query/request
            log_callback: Optional callback function for logging progress
            
        Returns:
            AI response as string
        """
        import time
        start_time = time.time()
        
        try:
            client = self._get_client()
            
            # Log the request
            logger.info(f"=== AI Call Start ===")
            logger.info(f"Provider: {self.provider}")
            logger.info(f"Model: {self.model}")
            logger.info(f"System Prompt: {system_prompt[:200]}...")
            logger.info(f"User Prompt: {user_prompt[:200]}...")
            
            if log_callback:
                log_callback(f"🤖 Calling {self.provider} API ({self.model})...")
            
            if self.provider == "openai":
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                ai_response = response.choices[0].message.content
                tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0
                
            elif self.provider == "anthropic":
                response = client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7
                )
                ai_response = response.content[0].text
                tokens_used = response.usage.input_tokens + response.usage.output_tokens if hasattr(response, 'usage') else 0
            
            duration = time.time() - start_time
            
            # Log the response
            logger.info(f"AI Response: {ai_response[:200]}...")
            logger.info(f"Tokens used: {tokens_used}")
            logger.info(f"Duration: {duration:.2f}s")
            logger.info(f"=== AI Call End ===")
            
            if log_callback:
                log_callback(f"✅ AI responded in {duration:.1f}s ({tokens_used} tokens)")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error calling AI provider: {e}")
            if log_callback:
                log_callback(f"❌ AI call failed: {str(e)}")
            raise
    
    def analyze_player_context(self, db: Session, player_id: str, log_callback=None) -> Dict[str, any]:
        """
        Analyze player's recent answers to understand their context and themes.
        
        Args:
            db: Database session
            player_id: Player ID
            log_callback: Optional callback for progress logging
            
        Returns:
            Dictionary with analysis results including themes, keywords, and sentiment
        """
        # Get recent answers (last 7 days)
        recent_answers = crud.get_player_recent_answers(db, player_id, days=7)
        
        if not recent_answers:
            return {
                "themes": [],
                "keywords": [],
                "sentiment": "neutral",
                "answer_count": 0
            }
        
        if log_callback:
            log_callback(f"📊 Analyzing {len(recent_answers)} recent answers...")
        
        # Prepare answer texts with questions for context
        answer_contexts = []
        for answer in recent_answers:
            question = crud.get_question(db, answer.question_id)
            if question:
                answer_contexts.append({
                    "question": question.question_text,
                    "answer": answer.answer_text,
                    "date": answer.answer_date.isoformat()
                })
        
        # Use AI to analyze the context
        system_prompt = """You are an expert at analyzing personal reflections and identifying themes,
        keywords, and emotional tones. Analyze the provided question-answer pairs and extract:
        1. Main themes (3-5 themes)
        2. Key topics/keywords (5-10 keywords)
        3. Overall sentiment (positive, negative, neutral, mixed)
        
        Return your analysis as a JSON object with keys: themes, keywords, sentiment."""
        
        user_prompt = f"""Analyze these recent reflections:

{json.dumps(answer_contexts, indent=2)}

Provide a JSON analysis of the main themes, keywords, and sentiment."""
        
        try:
            ai_response = self._call_ai(system_prompt, user_prompt, log_callback)
            # Parse JSON response
            analysis = json.loads(ai_response)
            analysis["answer_count"] = len(recent_answers)
            
            if log_callback:
                log_callback(f"🎯 Found themes: {', '.join(analysis.get('themes', [])[:3])}")
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing player context: {e}")
            if log_callback:
                log_callback(f"⚠️ Analysis failed, using fallback")
            # Return basic analysis as fallback
            return {
                "themes": ["reflection", "personal growth"],
                "keywords": [word for answer in recent_answers for word in answer.answer_text.lower().split()[:3]],
                "sentiment": "neutral",
                "answer_count": len(recent_answers)
            }
    
    def evaluate_existing_quotes(
        self, 
        db: Session, 
        player_context: Dict[str, any]
    ) -> List[Tuple[Quote, float, str]]:
        """
        Evaluate existing quotes in the database for relevance to player context.
        
        Args:
            db: Database session
            player_context: Player context analysis from analyze_player_context
            
        Returns:
            List of tuples (quote, relevance_score, reason)
        """
        existing_quotes = crud.get_quotes(db, skip=0, limit=100)
        
        if not existing_quotes:
            return []
        
        # Prepare quotes for AI evaluation
        quotes_data = [
            {
                "id": q.id,
                "text": q.quote_text,
                "author": q.author,
                "keywords": q.keywords
            }
            for q in existing_quotes
        ]
        
        system_prompt = """You are an expert at matching inspirational quotes to personal contexts.
        Given a person's themes, keywords, and sentiment, evaluate how relevant each quote is.
        
        For each quote, provide:
        1. A relevance score (0.0 to 1.0, where 1.0 is highly relevant)
        2. A brief reason explaining the relevance
        
        Return a JSON array with objects containing: quote_id, score, reason."""
        
        user_prompt = f"""Player Context:
Themes: {', '.join(player_context.get('themes', []))}
Keywords: {', '.join(player_context.get('keywords', []))}
Sentiment: {player_context.get('sentiment', 'neutral')}

Quotes to evaluate:
{json.dumps(quotes_data, indent=2)}

Evaluate each quote's relevance and return JSON array."""
        
        try:
            ai_response = self._call_ai(system_prompt, user_prompt)
            evaluations = json.loads(ai_response)
            
            # Match evaluations back to quote objects
            results = []
            for eval_item in evaluations:
                quote_id = eval_item.get("quote_id")
                score = float(eval_item.get("score", 0.0))
                reason = eval_item.get("reason", "")
                
                # Find the quote object
                quote = next((q for q in existing_quotes if q.id == quote_id), None)
                if quote:
                    results.append((quote, score, reason))
            
            # Sort by score descending
            results.sort(key=lambda x: x[1], reverse=True)
            return results
            
        except Exception as e:
            logger.error(f"Error evaluating existing quotes: {e}")
            # Fallback to simple keyword matching
            return [(q, 0.5, "Fallback matching") for q in existing_quotes[:5]]
    
    def should_fetch_new_quotes(
        self, 
        best_existing_score: float, 
        threshold: float = 0.7
    ) -> bool:
        """
        Decide if we should fetch new quotes from the internet.
        
        Args:
            best_existing_score: Best relevance score from existing quotes
            threshold: Minimum score threshold (default 0.7)
            
        Returns:
            True if we should fetch new quotes, False otherwise
        """
        return best_existing_score < threshold
    
    def generate_search_topics(
        self, 
        player_context: Dict[str, any]
    ) -> List[str]:
        """
        Generate search topics for fetching new quotes based on player context.
        
        Args:
            player_context: Player context analysis
            
        Returns:
            List of search topics
        """
        system_prompt = """You are an expert at identifying relevant topics for inspirational quotes.
        Given a person's themes and keywords, suggest 3-5 specific topics that would yield 
        relevant and meaningful quotes.
        
        Return a JSON array of topic strings."""
        
        user_prompt = f"""Player Context:
Themes: {', '.join(player_context.get('themes', []))}
Keywords: {', '.join(player_context.get('keywords', []))}
Sentiment: {player_context.get('sentiment', 'neutral')}

Generate 3-5 specific topics for finding relevant quotes. Return as JSON array."""
        
        try:
            ai_response = self._call_ai(system_prompt, user_prompt)
            topics = json.loads(ai_response)
            return topics[:5]  # Limit to 5 topics
        except Exception as e:
            logger.error(f"Error generating search topics: {e}")
            # Fallback to themes
            return player_context.get('themes', ['inspiration', 'motivation'])[:3]
    
    def select_best_quote(
        self,
        db: Session,
        player_id: str,
        log_callback=None
    ) -> Tuple[Quote, float, str]:
        """
        Main method: Select the best quote for a player, either from existing quotes
        or by fetching new ones from the internet.
        
        Args:
            db: Database session
            player_id: Player ID
            log_callback: Optional callback for progress logging
            
        Returns:
            Tuple of (quote, relevance_score, reason)
        """
        logger.info(f"AI Quote Agent selecting quote for player: {player_id}")
        
        # Step 1: Analyze player context
        if log_callback:
            log_callback("🔍 Step 1: Analyzing your personality...")
        player_context = self.analyze_player_context(db, player_id, log_callback)
        logger.info(f"Player context: {player_context}")
        
        # Step 2: Evaluate existing quotes
        evaluated_quotes = self.evaluate_existing_quotes(db, player_context)
        
        if evaluated_quotes:
            best_quote, best_score, best_reason = evaluated_quotes[0]
            logger.info(f"Best existing quote score: {best_score}")
            
            # Step 3: Decide if we need to fetch new quotes
            if self.should_fetch_new_quotes(best_score):
                logger.info("Existing quotes not relevant enough, fetching new ones...")
                
                # Generate search topics
                topics = self.generate_search_topics(player_context)
                logger.info(f"Search topics: {topics}")
                
                # Fetch new quotes
                new_quotes_data = []
                for topic in topics[:2]:  # Limit to 2 topics to avoid too many requests
                    fetched = quote_scraper.fetch_quotes_by_topic(topic, max_quotes=3)
                    new_quotes_data.extend(fetched)
                
                if new_quotes_data:
                    # Save new quotes to database and evaluate them
                    new_quote_objects = []
                    for quote_data in new_quotes_data:
                        # Extract keywords from themes
                        keywords = ', '.join(player_context.get('themes', []))
                        
                        quote_create = QuoteCreate(
                            quote_text=quote_data['text'],
                            author=quote_data['author'],
                            category=topics[0] if topics else 'general',
                            keywords=keywords,
                            source=quote_data['source'],
                            is_ai_generated=1,
                            ai_relevance_reason=f"Fetched for themes: {', '.join(topics)}"
                        )
                        
                        new_quote = crud.create_quote(db, quote_create)
                        new_quote_objects.append(new_quote)
                    
                    logger.info(f"Saved {len(new_quote_objects)} new quotes to database")
                    
                    # Evaluate new quotes
                    new_evaluated = self.evaluate_existing_quotes(db, player_context)
                    
                    # Compare with existing best
                    if new_evaluated and new_evaluated[0][1] > best_score:
                        best_quote, best_score, best_reason = new_evaluated[0]
                        logger.info(f"Selected new quote with score: {best_score}")
            
            return (best_quote, best_score, best_reason)
        
        else:
            # No existing quotes, fetch new ones
            logger.info("No existing quotes, fetching from internet...")
            topics = self.generate_search_topics(player_context)
            
            new_quotes_data = []
            for topic in topics[:2]:
                fetched = quote_scraper.fetch_quotes_by_topic(topic, max_quotes=3)
                new_quotes_data.extend(fetched)
            
            if new_quotes_data:
                # Save first quote and return it
                quote_data = new_quotes_data[0]
                keywords = ', '.join(player_context.get('themes', []))
                
                quote_create = QuoteCreate(
                    quote_text=quote_data['text'],
                    author=quote_data['author'],
                    category=topics[0] if topics else 'general',
                    keywords=keywords,
                    source=quote_data['source'],
                    is_ai_generated=1,
                    ai_relevance_reason=f"Fetched for themes: {', '.join(topics)}"
                )
                
                new_quote = crud.create_quote(db, quote_create)
                return (new_quote, 0.8, f"New quote fetched for: {topics[0]}")
            
            # Ultimate fallback
            raise Exception("No quotes available and unable to fetch new ones")


# Singleton instance
ai_quote_agent = AIQuoteAgent()

# Made with Bob