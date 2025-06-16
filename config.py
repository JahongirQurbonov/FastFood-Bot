import os
from dotenv import load_dotenv

# .env faylini majburiy yuklash (environment variable'larni override qilish)
load_dotenv(override=True)

class Config:
    def __init__(self):
        # .env faylidan to'g'ridan-to'g'ri o'qish
        self.BOT_TOKEN = self._get_token_from_env_file()
        self.WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-webapp.netlify.app")
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///fastfood_bot.db")
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN", "YOUR_PAYMENT_TOKEN")
        
        # Admin IDs
        admin_ids_str = os.getenv("ADMIN_IDS", "123456789")
        try:
            self.ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(",") if x.strip()]
        except:
            self.ADMIN_IDS = [123456789]
        
        # Languages
        self.LANGUAGES = {
            "uz": "🇺🇿 O'zbek",
            "ru": "🇷🇺 Русский", 
            "en": "🇬🇧 English"
        }
    
    def _get_token_from_env_file(self):
        """To'g'ridan-to'g'ri .env faylidan token o'qish"""
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('BOT_TOKEN='):
                        return line.split('=', 1)[1].strip()
        except:
            pass
        return os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")

config = Config()

# Debug print
if __name__ == "__main__":
    print(f"BOT_TOKEN: {config.BOT_TOKEN[:10]}...{config.BOT_TOKEN[-10:]}")
    print(f"ADMIN_IDS: {config.ADMIN_IDS}")
