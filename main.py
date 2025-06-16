import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import config
from database.db import create_tables
from middlewares.localization import LocalizationMiddleware
from handlers import start, payment, admin

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Create database tables
    create_tables()
    
    # Initialize bot and dispatcher
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Register middlewares
    dp.message.middleware(LocalizationMiddleware())
    dp.callback_query.middleware(LocalizationMiddleware())
    
    # Register routers
    dp.include_router(start.router)
    dp.include_router(payment.router)
    dp.include_router(admin.router)
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
