from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./dailyquestion.db"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI Configuration
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    ai_provider: str = "openai"  # "openai" or "anthropic"
    ai_model: str = "gpt-4o-mini"  # or "claude-3-5-sonnet-20241022"
    
    class Config:
        env_file = ".env"


settings = Settings()

# Made with Bob
