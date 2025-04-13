"""
Base handlers module for the bot.
"""
import logging
import os
import re
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
from ..utils.downloader import InstagramDownloader, TikTokDownloader
from ..config import load_config
from typing import Optional

load_dotenv()

config = load_config()
router = Router()

class DownloadState(StatesGroup):
    waiting_for_url = State()

# Регулярные выражения для определения URL
INSTAGRAM_REELS_PATTERN = r'https?://(?:www\.)?instagram\.com/(?:reel/|reels/)[\w-]+/?'
TIKTOK_PATTERN = r'https?://(?:www\.)?(?:tiktok\.com/@[\w-]+/video/\d+|vt\.tiktok\.com/[\w-]+/?)/?'

# Создаем экземпляр InstagramDownloader
try:
    instagram_downloader = InstagramDownloader("cookies.txt")
except FileNotFoundError as e:
    logging.error(f"Failed to initialize InstagramDownloader: {e}")
    instagram_downloader = None

async def handle_url(message: Message, url: str) -> Optional[str]:
    """Обработка URL и скачивание видео"""
    try:
        # Определяем тип URL
        if re.match(INSTAGRAM_REELS_PATTERN, url):
            if not instagram_downloader:
                await message.answer("Ошибка: не удалось инициализировать загрузчик Instagram")
                return None
            return instagram_downloader.download_reel(url, message.from_user.id)
        elif re.match(TIKTOK_PATTERN, url):
            return TikTokDownloader.download_video(url, message.from_user.id)
        else:
            await message.answer("Неподдерживаемый URL")
            return None
    except Exception as e:
        logging.error(f"Error handling URL: {str(e)}")
        await message.answer(f"Произошла ошибка при обработке URL: {str(e)}")
        return None

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "Привет! Отправь мне ссылку на видео из Instagram Reels или TikTok, "
        "и я скачаю его для тебя."
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Как использовать бота:\n\n"
        "1. Отправь мне ссылку на видео из Instagram или TikTok\n"
        "2. Я скачаю видео и отправлю его тебе\n\n"
        "Поддерживаемые форматы:\n"
        "- Instagram Reels\n"
        "- TikTok видео"
    )

@router.message(F.text)
async def handle_message(message: Message):
    """Обработчик текстовых сообщений"""
    url = message.text.strip()
    
    # Проверяем, является ли текст URL
    if not (re.match(INSTAGRAM_REELS_PATTERN, url) or re.match(TIKTOK_PATTERN, url)):
        await message.answer("Пожалуйста, отправьте корректную ссылку на видео из Instagram Reels или TikTok")
        return
    
    try:
        # Удаляем сообщение с URL
        await message.delete()
        
        # Отправляем эмодзи молнии и сохраняем сообщение
        loading_msg = await message.answer("⚡️")
        
        # Скачиваем видео
        video_path = await handle_url(message, url)
        if not video_path:
            return
        
        try:
            # Отправляем видео с подписью
            video = FSInputFile(video_path)
            platform = "Insta" if "instagram.com" in url else "ТикТок"
            caption = f"🎬 Приятного просмотра!\n\n<a href='{url}'>🔗 Оригинал на {platform}</a>"
            await message.answer_video(video, caption=caption, parse_mode="HTML")
        except Exception as e:
            logging.error(f"Error sending video: {str(e)}")
            await message.answer(f"Произошла ошибка при отправке видео: {str(e)}")
        finally:
            # Удаляем временный файл
            try:
                os.remove(video_path)
            except Exception as e:
                logging.error(f"Error deleting video file: {str(e)}")
            
            # Удаляем сообщение с молнией
            try:
                await loading_msg.delete()
            except Exception as e:
                logging.error(f"Error deleting loading message: {str(e)}")
                
    except Exception as e:
        logging.error(f"Error in message handler: {str(e)}")
        await message.answer(f"Произошла ошибка: {str(e)}") 