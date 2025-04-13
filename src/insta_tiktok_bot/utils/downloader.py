"""
Utility functions for downloading content from Instagram and TikTok.
"""
import os
import logging
import re
import requests
import tempfile
import subprocess
from pathlib import Path
from typing import Optional
from tiktok_downloader import snaptik
import gallery_dl
from gallery_dl import config
from gallery_dl.job import DownloadJob
from gallery_dl.exception import NoExtractorError
import yt_dlp


logger = logging.getLogger(__name__)

class InstagramDownloader:
    """Class for handling Instagram downloads."""
    
    def __init__(self, cookies_file: str):
        # Получаем абсолютный путь к куки-файлу
        project_root = Path(__file__).parent.parent.parent.parent
        self.cookies_file = str(project_root / cookies_file)
        
        # Проверяем существование куки-файла
        if not os.path.exists(self.cookies_file):
            logger.error(f"Cookies file not found at {self.cookies_file}")
            raise FileNotFoundError(f"Cookies file not found at {self.cookies_file}")
        
        logger.info(f"Using cookies file: {self.cookies_file}")

    def download_reel(self, url: str, user_id: int) -> Optional[str]:
        try:
            logger.info(f"Starting download for URL: {url}")
            
            # Создаем временную директорию для загрузки
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, f"instagram_reel_{user_id}.mp4")
            
            # Настраиваем yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': output_path,
                'cookiefile': self.cookies_file,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            # Пытаемся скачать видео
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                if os.path.exists(output_path):
                    logger.info(f"Video downloaded successfully: {output_path}")
                    return output_path
                else:
                    logger.error("No video file found after download")
                    return None
                    
            except Exception as e:
                logger.error(f"Error during download: {str(e)}")
                return None
                
        except Exception as e:
            logger.error(f"Error in download_reel: {str(e)}")
            return None
        finally:
            # Очищаем временные файлы, кроме скачанного видео
            try:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file != os.path.basename(output_path):
                            os.remove(os.path.join(root, file))
            except Exception as e:
                logger.error(f"Error cleaning up temp files: {str(e)}")

class TikTokDownloader:
    """Class for handling TikTok downloads."""
    
    @staticmethod
    def download_video(url: str, user_id: int) -> Optional[str]:
        """
        Download TikTok video.
        
        Args:
            url: TikTok video URL
            user_id: Telegram user ID
            
        Returns:
            str: Path to downloaded video file
        """
        try:
            # Создаем временную директорию для загрузки
            temp_dir = tempfile.mkdtemp()
            output_path = os.path.join(temp_dir, f"tiktok_{user_id}.mp4")
            
            # Настраиваем yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': output_path,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            # Пытаемся скачать видео
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                if os.path.exists(output_path):
                    logger.info(f"Video downloaded successfully: {output_path}")
                    return output_path
                else:
                    logger.error("No video file found after download")
                    return None
                    
            except Exception as e:
                logger.error(f"Error during download: {str(e)}")
                return None
                
        except Exception as e:
            logger.error(f"Error in download_video: {str(e)}")
            return None
        finally:
            # Очищаем временные файлы, кроме скачанного видео
            try:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file != os.path.basename(output_path):
                            os.remove(os.path.join(root, file))
            except Exception as e:
                logger.error(f"Error cleaning up temp files: {str(e)}") 