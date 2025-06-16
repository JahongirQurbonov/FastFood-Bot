# Oddiy test fayli
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

# Test bot
async def test_bot():
    try:
        bot = Bot(token="TEST_TOKEN")
        dp = Dispatcher()
        
        @dp.message(CommandStart())
        async def start_handler(message: Message):
            await message.answer("Bot ishlayapti! ✅")
        
        print("✅ Aiogram muvaffaqiyatli import qilindi!")
        return True
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_bot())
