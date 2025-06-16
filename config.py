import os
from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
    WEBAPP_URL: str = os.getenv("WEBAPP_URL", "https://your-webapp.netlify.app")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/fastfood_bot")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Admin user IDs
    ADMIN_IDS: List[int] = [123456789]  # Replace with actual admin user IDs
    
    # Payment provider token
    PAYMENT_PROVIDER_TOKEN: str = os.getenv("PAYMENT_PROVIDER_TOKEN", "YOUR_PAYMENT_TOKEN")
    
    # Supported languages
    LANGUAGES = {
        "uz": "🇺🇿 O'zbek",
        "ru": "🇷🇺 Русский", 
        "en": "🇬🇧 English"
    }

config = Config()
