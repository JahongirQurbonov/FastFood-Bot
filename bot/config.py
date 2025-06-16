import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if BOT_TOKEN:
    BOT_TOKEN = BOT_TOKEN.strip('"').strip("'")
    print(f"✅ Token yuklandi: {BOT_TOKEN[:10]}...")
else:
    print("❌ Token topilmadi!")
    exit(1)

class Config:
    BOT_TOKEN = BOT_TOKEN
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///fastfood.db')
    
    # Admin ID'lar
    ADMIN_IDS = [123456789]  # O'z Telegram ID'ingizni yozing
    
    # Web App URL'lari
    WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://fast-food-bot-omega.vercel.app')
    
    # To'lov provider token (UZS uchun)
    # Click, Payme yoki boshqa UZS provider tokenini qo'ying
    PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN', '284685063:TEST:your_uzs_test_token')
    
    # Boshqa sozlamalar
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    WEBAPP_HOST = os.getenv('WEBAPP_HOST', 'localhost')
    WEBAPP_PORT = int(os.getenv('WEBAPP_PORT', 8000))
    
    # Kanallar
    CHANNELS = os.getenv('CHANNELS', '').split(',') if os.getenv('CHANNELS') else []

config = Config()
