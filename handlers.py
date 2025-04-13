from aiogram import types, Router, F
import requests
import instaloader
import os
from config import SAVEIG_API, INSTAGRAM_SESSION_USERNAME, INSTAGRAM_SESSION_FILE, BOT_LINK
import logging
from tiktok_downloader import snaptik


logging.basicConfig(level=logging.INFO)

router = Router()

loader = instaloader.Instaloader(dirname_pattern='downloads', filename_pattern='reels')

loader.load_session_from_file(INSTAGRAM_SESSION_USERNAME, INSTAGRAM_SESSION_FILE)

@router.message(F.text == "/start")
async def start_command(message: types.Message):
    logging.info(f"User {message.from_user.id} started the bot.")
    await message.answer("Привет! 👋\nОтправь мне ссылку на Instagram Reels или TikTok, и я скачаю его для тебя.")

@router.message(F.text.contains("instagram.com/reel/"))
async def handle_reels(message: types.Message):
    url = message.text.strip()
    logging.info(f"User {message.from_user.id} sent reels link: {url}")
    await message.delete()
    status_msg = await message.answer("⚡️")

    try:
        logging.info("Starting Instaloader to download the reel...")
        import re
        shortcode_match = re.search(r"instagram\.com/reel/([^/?#&]+)", url)
        shortcode = shortcode_match.group(1) if shortcode_match else None
        logging.info(f"Shortcode: {shortcode}")
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        target_folder = f"downloads/reels_{shortcode}"
        filename_pattern = f"reels_{shortcode}_{message.from_user.id}"
        loader.dirname_pattern = target_folder
        loader.filename_pattern = filename_pattern
        loader.download_post(post, target=target_folder)
        logging.info("Download completed using Instaloader.")

        video_path = None
        for root, dirs, files in os.walk(target_folder):
            for file in files:
                if file.endswith('.mp4'):
                    video_path = os.path.join(root, file)
                    break

        if not video_path:
            raise Exception("Video file not found")

        await status_msg.delete()
        caption = f"🎥 Вот ваше видео 🍿\n\n<a href=\"{BOT_LINK}\">@{BOT_LINK.split('/')[-1]}</a> | <a href=\"{url}\">Original Media</a>"
        await message.answer_video(types.FSInputFile(video_path), caption=caption, parse_mode="HTML")
        logging.info(f"Deleting video file: {video_path}")
        os.remove(video_path)

    except Exception as e:
        logging.error(f"Error downloading reels: {e}")
        await status_msg.delete()
        await message.answer("❌ Не удалось скачать видео.\nПопробуй другую ссылку.")

@router.message(F.text.contains("tiktok.com/"))
async def handle_tiktok(message: types.Message):
    url = message.text.strip()
    logging.info(f"User {message.from_user.id} sent TikTok link: {url}")
    await message.delete()
    status_msg = await message.answer("⚡️")

    try:
        logging.info("Starting TikTok download...")
        video = snaptik(url)
        video[0].download(f"downloads/tiktok_{message.from_user.id}.mp4")
        logging.info("Download completed")

        video_path = f"downloads/tiktok_{message.from_user.id}.mp4"
        if not os.path.exists(video_path):
            raise Exception("Video file not found")

        await status_msg.delete()
        caption = f"🎥 Вот ваше видео 🍿\n\n<a href=\"{BOT_LINK}\">@{BOT_LINK.split('/')[-1]}</a> | <a href=\"{url}\">Original Media</a>"
        await message.answer_video(types.FSInputFile(video_path), caption=caption, parse_mode="HTML")
        logging.info(f"Deleting video file: {video_path}")
        os.remove(video_path)

    except Exception as e:
        logging.error(f"Error downloading TikTok: {e}")
        await status_msg.delete()
        await message.answer("❌ Не удалось скачать видео.\nПопробуй другую ссылку.")

@router.message()
async def invalid_message(message: types.Message):
    logging.info(f"User {message.from_user.id} sent invalid message: {message.text}")
    await message.answer("⚠️ Отправь, пожалуйста, ссылку на Instagram Reels или TikTok.")

def register_handlers(dp):
    dp.include_router(router)
