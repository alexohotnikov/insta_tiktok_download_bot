"""
Main module for the Instagram and TikTok download bot.
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from .handlers import router
from .config import load_config

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Load configuration
config = load_config()

async def main():
    """Main function to start the bot."""
    try:
        # Initialize bot and dispatcher
        bot = Bot(token=config.bot.token)
        dp = Dispatcher()
        
        # Register handlers
        dp.include_router(router)
        
        # Start polling
        logging.info("Starting bot...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logging.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 