"""
Base handlers module for the bot.
"""
import logging
import os
import re
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
from ..utils.downloader import InstagramDownloader, TikTokDownloader
from ..config import load_config
from typing import Optional, List

load_dotenv()

config = load_config()
router = Router()

class DownloadState(StatesGroup):
    waiting_for_url = State()

class SecurityState(StatesGroup):
    waiting_for_answer = State()

# Регулярные выражения для определения URL
INSTAGRAM_REELS_PATTERN = r'https?://(?:www\.)?instagram\.com/(?:reel/|reels/)[\w-]+/?'
TIKTOK_PATTERN = r'https?://(?:www\.)?(?:tiktok\.com/@[\w-]+/video/\d+|vt\.tiktok\.com/[\w-]+/?)/?'
INSTAGRAM_POST_PATTERN = r'https?://(?:www\.)?instagram\.com/p/[\w-]+/?'

# Создаем экземпляр InstagramDownloader
try:
    instagram_downloader = InstagramDownloader("cookies.txt")
except FileNotFoundError as e:
    logging.error(f"Failed to initialize InstagramDownloader: {e}")
    instagram_downloader = None

async def handle_url(message: Message, url: str) -> Optional[List[dict]]:
    """Обработка URL и скачивание медиа"""
    try:
        # Определяем тип URL
        if re.match(r'https?://(?:www\.)?instagram\.com/(?:reel|reels)/[\w-]+/?', url):
            if not instagram_downloader:
                await message.answer("Ошибка: не удалось инициализировать загрузчик Instagram")
                return None
            video_path = instagram_downloader.download_reel(url, message.from_user.id)
            return [{'type': 'video', 'path': video_path}] if video_path else None
        elif re.match(r'https?://(?:www\.)?instagram\.com/p/[\w-]+/?', url):
            if not instagram_downloader:
                await message.answer("Ошибка: не удалось инициализировать загрузчик Instagram")
                return None
            # Use download_post_with_instaloader for specific post download
            post_data = instagram_downloader.download_post_with_instaloader(url, message.from_user.id)
            if post_data:
                return [{'type': 'post', 'path': post_data['path'], 'caption': post_data.get('caption')}]
            return None
        elif re.match(TIKTOK_PATTERN, url):
            video_path = TikTokDownloader.download_video(url, message.from_user.id)
            return [{'type': 'video', 'path': video_path}] if video_path else None
        else:
            await message.answer("Неподдерживаемый URL")
            return None
    except Exception as e:
        logging.error(f"Error handling URL: {str(e)}")
        await message.answer(f"Произошла ошибка при обработке URL: {str(e)}")
        return None

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    # Check if user has already passed the security check
    user_data = await state.get_data()
    if user_data.get('passed_security_check', False):
        await message.answer("Вы уже прошли проверку безопасности. Можете использовать бота.")
        return

    await message.answer("Привет! Чтобы использовать бота, ответьте на вопрос: Какой номер дома?")
    await state.set_state(SecurityState.waiting_for_answer)

@router.message(SecurityState.waiting_for_answer)
async def process_answer(message: Message, state: FSMContext):
    """Обработчик ответа на вопрос безопасности"""
    answer = message.text.strip().lower()  # Convert answer to lowercase
    if answer == "2в":  # Compare with lowercase correct answer
        await state.update_data(passed_security_check=True)
        await message.answer("Ответ верный! Теперь вы можете использовать бота.")
        # Do not clear the state completely, just reset the current state
        await state.set_state(None)
    else:
        await message.answer("Ответ неверный. Попробуйте снова.")

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
async def handle_message(message: Message, state: FSMContext):
    """Обработчик текстовых сообщений"""
    # Check if user has passed the security check
    user_data = await state.get_data()
    if not user_data.get('passed_security_check', False):
        await message.answer("Вы должны ответить на вопрос безопасности, чтобы использовать бота.\nВведите /start чтобы начать")
        return

    url = message.text.strip()
    
    # Проверяем, является ли текст URL
    if not (re.match(INSTAGRAM_REELS_PATTERN, url) or re.match(TIKTOK_PATTERN, url) or re.match(INSTAGRAM_POST_PATTERN, url)):
        await message.answer("Пожалуйста, отправьте корректную ссылку на видео из Instagram Reels или TikTok")
        return
    
    try:
        # Удаляем сообщение с URL
        await message.delete()
        
        # Отправляем эмодзи молнии и сохраняем сообщение
        loading_msg = await message.answer("⚡️")
        
        # Скачиваем видео
        download_results = await handle_url(message, url)
        if not download_results:
            return
        
        try:
            # Обрабатываем результаты загрузки
            for result in download_results:
                if result['type'] == 'video':
                    video_path = result['path']
                    # Ensure the video file exists before sending
                    if not os.path.exists(video_path):
                        logging.error(f"Video file does not exist: {video_path}")
                        await message.answer("Ошибка: видеофайл не найден.")
                        continue

                    try:
                        # Send video with caption
                        video = FSInputFile(video_path)
                        platform = "Insta" if "instagram.com" in url else "ТикТок"
                        caption = f"🎬 Приятного просмотра!\n\n<a href='{url}'>🔗 Оригинал на {platform}</a>"
                        await message.answer_video(video, caption=caption, parse_mode="HTML")
                    except Exception as e:
                        logging.error(f"Error sending video: {str(e)}")
                        await message.answer(f"Произошла ошибка при отправке видео: {str(e)}")
                    
                    # Ensure the file is not in use before deleting
                    try:
                        os.remove(video_path)
                    except Exception as e:
                        logging.error(f"Error deleting video file: {str(e)}")
                        await message.answer(f"Ошибка при удалении видеофайла: {str(e)}")
                elif result['type'] == 'post':
                    post_path = result['path']
                    post_caption = result.get('caption')
                    # Collect all photo paths
                    photo_paths = []
                    for root, _, files in os.walk(post_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                                photo_paths.append(file_path)

                    # Create media group
                    media_group = []
                    for i, photo_path in enumerate(photo_paths):
                        try:
                            # Verify file existence and log file size
                            if not os.path.exists(photo_path):
                                logging.error(f"File does not exist: {photo_path}")
                                await message.answer(f"Ошибка: файл не найден: {photo_path}")
                                continue

                            file_size = os.path.getsize(photo_path)
                            logging.info(f"File size: {file_size} bytes")

                            # Check if file size exceeds Telegram's limit
                            if file_size > 20 * 1024 * 1024:  # 20 MB limit
                                logging.error(f"File size exceeds limit: {photo_path}")
                                await message.answer(f"Ошибка: файл слишком большой для отправки: {photo_path}")
                                continue

                            logging.info(f"Adding file to media group: {photo_path}")

                            # Add to media group with caption only for the first photo
                            if i == 0 and post_caption:
                                caption = f"{post_caption}\n\n<a href='{url}'>🔗 Оригинал в Instagram</a>"
                                media_group.append(InputMediaPhoto(media=FSInputFile(photo_path), caption=caption, parse_mode="HTML"))
                            else:
                                media_group.append(InputMediaPhoto(media=FSInputFile(photo_path)))
                        except Exception as e:
                            logging.error(f"Error preparing photo for media group: {str(e)}")
                            await message.answer(f"Произошла ошибка при подготовке фото: {str(e)}")

                    # Send media group
                    if media_group:
                        try:
                            await message.answer_media_group(media_group)
                        except Exception as e:
                            logging.error(f"Error sending media group: {str(e)}")
                            await message.answer(f"Произошла ошибка при отправке группы медиа: {str(e)}")
        except Exception as e:
            logging.error(f"Error processing download results: {str(e)}")
            await message.answer(f"Произошла ошибка при обработке результатов загрузки: {str(e)}")
        finally:
            # Удаляем временные файлы
            for result in download_results:
                try:
                    if result['type'] == 'post':
                        # For posts, we need to remove all files in the directory first
                        post_path = result['path']
                        if os.path.exists(post_path):
                            for root, _, files in os.walk(post_path):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    try:
                                        os.remove(file_path)
                                    except Exception as e:
                                        logging.error(f"Error deleting file {file_path}: {str(e)}")
                            # Remove the directory itself
                            try:
                                os.rmdir(post_path)
                            except Exception as e:
                                logging.error(f"Error removing directory {post_path}: {str(e)}")
                    else:
                        # For videos, just remove the file
                        if os.path.exists(result['path']):
                            os.remove(result['path'])
                except Exception as e:
                    logging.error(f"Error deleting file: {str(e)}")
            
            # Удаляем сообщение с молнией
            try:
                await loading_msg.delete()
            except Exception as e:
                logging.error(f"Error deleting loading message: {str(e)}")
                
    except Exception as e:
        logging.error(f"Error in message handler: {str(e)}")
        await message.answer(f"Произошла ошибка: {str(e)}") 