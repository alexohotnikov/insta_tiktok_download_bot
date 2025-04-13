"""
Instagram handlers module for the bot.
"""
from aiogram import types, F
import logging
from .base import BaseHandler

logger = logging.getLogger(__name__)

class InstagramHandler(BaseHandler):
    """Handler for Instagram content."""
    
    def __init__(self, config):
        """Initialize Instagram handler."""
        super().__init__(config)
        self._register_handlers()
    
    def _register_handlers(self):
        """Register Instagram-related handlers."""
        @self.router.message(F.text.contains("instagram.com/reel/"))
        async def handle_reels(message: types.Message):
            url = message.text.strip()
            logger.info(f"User {message.from_user.id} sent reels link: {url}")
            await message.delete()
            status_msg = await message.answer("⚡️")

            try:
                video_path = self.instagram_downloader.download_reel(url, message.from_user.id)
                if video_path:
                    await self._send_video(message, video_path, url, status_msg)
                else:
                    await self._handle_error(message, status_msg)
                    
            except Exception as e:
                logger.error(f"Error handling reels: {e}")
                await self._handle_error(message, status_msg) 