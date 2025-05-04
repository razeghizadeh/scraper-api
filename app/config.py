import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Scraper API"
    DEBUG: bool = False
    MAX_RETRIES: int = 3
    REQUEST_TIMEOUT: int = 30
    USER_AGENT: str = "Mozilla/5.0 (compatible; ScraperAPI/1.0; +https://github.com/yourusername/scraper-api)"
    
    # تنظیمات Render.com از متغیرهای محیطی می‌گیرد
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    
    class Config:
        env_file = ".env"

settings = Settings()
