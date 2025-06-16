import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import config
from database.db import create_tables
from middlewares.localization import LocalizationMiddleware
from handlers import start, payment, admin, webapp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to start the bot."""
    try:
        # Create database tables
        logger.info("Creating database tables...")
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
        dp.include_router(webapp.router)
        
        logger.info("Bot started successfully!")
        
        # Start polling
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
