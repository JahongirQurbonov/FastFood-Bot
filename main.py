import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from database.models import db
from handlers import start, menu, cart

async def main():
    # Logging sozlash
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        # Ma'lumotlar bazasini ishga tushirish
        logger.info("Initializing database...")
        await db.init_db()
        logger.info("Database initialized successfully!")
        
        # Bot va dispatcher yaratish
        bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher(storage=MemoryStorage())
        
        # Handlerlarni ro'yxatdan o'tkazish
        dp.include_router(start.router)
        dp.include_router(menu.router)
        dp.include_router(cart.router)
        
        logger.info("Bot started successfully!")
        
        # Botni ishga tushirish
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
