import asyncio
from aiogram import Bot

async def test_direct_token():
    # Token'ni to'g'ridan-to'g'ri yozing
    token = "8118098103:AAHGGyL4nsU-ENzMPr8LZwOBgx23m14lVNk"
    
    try:
        bot = Bot(token=token)
        me = await bot.get_me()
        print(f"✅ Bot ishlayapti: @{me.username}")
        await bot.session.close()
    except Exception as e:
        print(f"❌ Xatolik: {e}")

if __name__ == "__main__":
    asyncio.run(test_direct_token())
