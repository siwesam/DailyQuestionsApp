"""
AI Quote Agent Configuration
Allows runtime configuration of agent behavior
"""
from pydantic import BaseModel, Field
from typing import Literal, Optional


class AgentConfig(BaseModel):
    """Configuration for AI Quote Agent behavior"""
    
    # Quote source preferences
    quote_source: Literal["database_only", "web_only", "hybrid"] = Field(
        default="hybrid",
        description="Where to source quotes from: database_only, web_only, or hybrid (try database first, fetch from web if needed)"
    )
    
    # AI model settings
    use_ai: bool = Field(
        default=True,
        description="Whether to use AI for quote selection (if False, uses simple keyword matching)"
    )
    
    ai_provider: Literal["openai", "anthropic"] = Field(
        default="openai",
        description="AI provider to use"
    )
    
    ai_model: str = Field(
        default="gpt-3.5-turbo",
        description="AI model to use (e.g., gpt-3.5-turbo, gpt-4, claude-3-sonnet)"
    )
    
    # Quote selection thresholds
    relevance_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum relevance score (0.0-1.0) to accept a quote from database before fetching from web"
    )
    
    # Analysis settings
    analysis_days: int = Field(
        default=7,
        ge=1,
        le=30,
        description="Number of days of recent answers to analyze"
    )
    
    max_quotes_to_evaluate: int = Field(
        default=100,
        ge=10,
        le=500,
        description="Maximum number of database quotes to evaluate"
    )
    
    # Web scraping settings
    enable_web_scraping: bool = Field(
        default=True,
        description="Whether to allow fetching quotes from the web"
    )
    
    max_web_quotes: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of quotes to fetch from web per request"
    )
    
    # Logging
    verbose_logging: bool = Field(
        default=True,
        description="Whether to log detailed AI process information"
    )


# Global configuration instance
_agent_config = AgentConfig()


def get_agent_config() -> AgentConfig:
    """Get current agent configuration"""
    return _agent_config


def update_agent_config(config: AgentConfig) -> AgentConfig:
    """Update agent configuration"""
    global _agent_config
    _agent_config = config
    return _agent_config


def reset_agent_config() -> AgentConfig:
    """Reset agent configuration to defaults"""
    global _agent_config
    _agent_config = AgentConfig()
    return _agent_config

# Made with Bob
