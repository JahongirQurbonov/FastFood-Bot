import os
from dotenv import load_dotenv

print("🔍 Config debug qilish...")

# .env faylini yuklash
load_dotenv()

# Barcha environment variables
print("📋 Barcha BOT_TOKEN environment variables:")
for key, value in os.environ.items():
    if 'BOT' in key or 'TOKEN' in key:
        print(f"   {key}: {value[:10]}...{value[-10:] if len(value) > 20 else value}")

# To'g'ridan-to'g'ri .env dan o'qish
print("\n📖 .env faylidan to'g'ridan-to'g'ri o'qish:")
try:
    with open('.env', 'r') as f:
        for line_num, line in enumerate(f, 1):
            if 'BOT_TOKEN' in line:
                print(f"   Line {line_num}: {line.strip()}")
                # Token'ni ajratib olish
                if '=' in line:
                    token = line.split('=', 1)[1].strip()
                    print(f"   Extracted token: {token}")
except Exception as e:
    print(f"❌ Xatolik: {e}")

# Config import test
print("\n🔧 Config import test:")
try:
    from config import config
    print(f"✅ Config import muvaffaqiyatli!")
    print(f"📝 Config.BOT_TOKEN: {config.BOT_TOKEN[:10]}...{config.BOT_TOKEN[-10:]}")
    print(f"📏 Token uzunligi: {len(config.BOT_TOKEN)}")
except Exception as e:
    print(f"❌ Config import xatoligi: {e}")
