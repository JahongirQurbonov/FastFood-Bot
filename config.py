import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    WEBAPP_URL: str = os.getenv("WEBAPP_URL", "https://jahongirqurbonov.github.io/FastFood-Bot/")
    PAYMENT_TOKEN: str = os.getenv("PAYMENT_TOKEN", "YOUR_PAYMENT_TOKEN_HERE")
    ADMIN_ID: int = int(os.getenv("ADMIN_ID", "123456789"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "fastfood_bot.db")
    
    # Localization
    DEFAULT_LANGUAGE: str = "uz"
    SUPPORTED_LANGUAGES: list = None
    
    def __post_init__(self):
        if self.SUPPORTED_LANGUAGES is None:
            self.SUPPORTED_LANGUAGES = ["uz", "ru", "en"]

config = Config()