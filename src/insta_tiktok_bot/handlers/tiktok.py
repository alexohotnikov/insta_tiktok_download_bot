"""
TikTok handlers module for the bot.
"""
from aiogram import types, F
import logging
from .base import BaseHandler
from ..utils.downloader import TikTokDownloader

logger = logging.getLogger(__name__)

class TikTokHandler(BaseHandler):
    """Handler for TikTok content."""
    
    def __init__(self, config):
        """Initialize TikTok handler."""
        super().__init__(config)
        self._register_handlers()
    
    def _register_handlers(self):
        """Register TikTok-related handlers."""
        @self.router.message(F.text.contains("tiktok.com/"))
        async def handle_tiktok(message: types.Message):
            url = message.text.strip()
            logger.info(f"User {message.from_user.id} sent TikTok link: {url}")
            await message.delete()
            status_msg = await message.answer("⚡️")

            try:
                video_path = TikTokDownloader.download_video(url, message.from_user.id)
                if video_path:
                    await self._send_video(message, video_path, url, status_msg)
                else:
                    await self._handle_error(message, status_msg)
                    
            except Exception as e:
                logger.error(f"Error handling TikTok: {e}")
                await self._handle_error(message, status_msg) 