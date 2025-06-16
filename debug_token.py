import os
from dotenv import load_dotenv

print("🔍 Token debug qilish...")

# .env faylini yuklash
load_dotenv()

# Token ni olish
token = os.getenv("BOT_TOKEN")

print(f"📁 .env fayli joylashuvi: {os.path.abspath('.env')}")
print(f"📄 .env fayli mavjudmi: {os.path.exists('.env')}")

if token:
    print(f"✅ Token topildi!")
    print(f"📏 Token uzunligi: {len(token)}")
    print(f"🔤 Token boshi: {token[:10]}...")
    print(f"🔤 Token oxiri: ...{token[-10:]}")
    
    # Token formatini tekshirish
    if ":" in token:
        parts = token.split(":")
        bot_id = parts[0]
        bot_hash = parts[1] if len(parts) > 1 else ""
        
        print(f"🤖 Bot ID: {bot_id}")
        print(f"🔑 Hash uzunligi: {len(bot_hash)}")
        print(f"🔢 Bot ID raqammi: {bot_id.isdigit()}")
        print(f"📏 Hash to'g'ri uzunlikmi (35): {len(bot_hash) == 35}")
        
        # Yashirin belgilarni tekshirish
        print(f"🔍 Token ichida yashirin belgilar:")
        for i, char in enumerate(token):
            if ord(char) < 32 or ord(char) > 126:
                print(f"   Pozitsiya {i}: ASCII {ord(char)}")
    else:
        print("❌ Token'da ':' belgisi yo'q!")
else:
    print("❌ Token topilmadi!")

# .env faylini o'qish
print("\n📖 .env fayli mazmuni:")
try:
    with open('.env', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            if 'BOT_TOKEN' in line:
                print(f"   {i}: {repr(line)}")  # repr() yashirin belgilarni ko'rsatadi
except Exception as e:
    print(f"❌ .env faylini o'qishda xatolik: {e}")
