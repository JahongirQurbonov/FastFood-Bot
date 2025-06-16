import asyncio
from aiogram import Bot

async def test_bot():
    # Token'ni to'g'ridan-to'g'ri yozamiz
    token = "8118098103:AAHGGyL4nsU-ENzMPr8LZwOBgx23m14lVNk"
    
    print(f"🔍 Test token: {token[:10]}...{token[-10:]}")
    
    try:
        bot = Bot(token=token)
        me = await bot.get_me()
        print(f"✅ Bot ishlayapti!")
        print(f"🤖 Bot nomi: {me.first_name}")
        print(f"📱 Username: @{me.username}")
        await bot.session.close()
        return True
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_bot())

