import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Token ni olish
token = os.getenv("BOT_TOKEN")

print(f"Token: {token}")

if token and token != "YOUR_BOT_TOKEN":
    print("✅ Token topildi!")
    
    # Token formatini tekshirish
    if ":" in token and len(token.split(":")) == 2:
        bot_id, bot_hash = token.split(":")
        if bot_id.isdigit() and len(bot_hash) == 35:
            print("✅ Token formati to'g'ri!")
        else:
            print("❌ Token formati noto'g'ri!")
    else:
        print("❌ Token formati noto'g'ri!")
else:
    print("❌ Token topilmadi yoki default qiymat!")

