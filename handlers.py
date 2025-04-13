import logging
import os
import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
from .utils.downloader import InstagramDownloader, TikTokDownloader
from .config import load_config

load_dotenv()

config = load_config()
router = Router()

class DownloadState(StatesGroup):
    waiting_for_url = State()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для скачивания видео из Instagram и TikTok. "
        "Просто отправь мне ссылку на видео, и я скачаю его для тебя."
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
async def handle_url(message: Message):
    url = message.text.strip()
    
    # Проверяем, является ли ссылка Instagram Reels
    if "instagram.com/reel/" in url:
        logging.info("Instagram Reels URL detected")
        instagram_downloader = InstagramDownloader(
            config.instagram.session_username,
            config.instagram.session_file,
            config.instagram.cookies_file
        )
        video_path = instagram_downloader.download_reel(url, message.from_user.id)
        
        if video_path:
            with open(video_path, 'rb') as video:
                await message.answer_video(video)
            os.remove(video_path)
        else:
            await message.answer("Не удалось скачать видео. Пожалуйста, проверьте ссылку и попробуйте снова.")
    
    # Проверяем, является ли ссылка TikTok
    elif "tiktok.com" in url:
        logging.info("TikTok URL detected")
        video_path = TikTokDownloader.download_video(url, message.from_user.id)
        
        if video_path:
            with open(video_path, 'rb') as video:
                await message.answer_video(video)
            os.remove(video_path)
        else:
            await message.answer("Не удалось скачать видео. Пожалуйста, проверьте ссылку и попробуйте снова.")
    
    else:
        await message.answer(
            "Пожалуйста, отправьте корректную ссылку на видео из Instagram Reels или TikTok."
        )

def register_handlers(dp):
    dp.include_router(router)
