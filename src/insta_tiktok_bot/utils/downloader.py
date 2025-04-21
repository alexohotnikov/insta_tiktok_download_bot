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
from typing import Optional, List
from tiktok_downloader import snaptik
import gallery_dl
from gallery_dl import config
from gallery_dl.job import DownloadJob
from gallery_dl.exception import NoExtractorError
import yt_dlp
from instaloader import Instaloader, Post


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
            project_root = Path(__file__).parent.parent.parent.parent
            temp_dir = os.path.join(project_root, 'temp_downloads')
            os.makedirs(temp_dir, exist_ok=True)
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

    def download_media(self, url: str, user_id: int) -> Optional[List[str]]:
        try:
            logger.info(f"Starting download for URL: {url}")
            
            # Создаем временную директорию для загрузки
            project_root = Path(__file__).parent.parent.parent.parent
            temp_dir = os.path.join(project_root, 'temp_downloads')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Настраиваем yt-dlp
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'cookiefile': self.cookies_file,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            # Пытаемся скачать медиа
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Собираем все скачанные файлы
                media_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
                if media_files:
                    logger.info(f"Media downloaded successfully: {media_files}")
                    return media_files
                else:
                    logger.error("No media files found after download")
                    return None
                    
            except Exception as e:
                logger.error(f"Error during download: {str(e)}")
                return None
                
        except Exception as e:
            logger.error(f"Error in download_media: {str(e)}")
            return None
        finally:
            # Очищаем временные файлы, кроме скачанных медиа
            try:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file not in media_files:
                            os.remove(os.path.join(root, file))
            except Exception as e:
                logger.error(f"Error cleaning up temp files: {str(e)}")
         

    def download_post_with_scraper(self, post_url: str, user_id: int) -> Optional[str]:
        try:
            logger.info(f"Starting download for Instagram post URL: {post_url}")
            
            # Create a temporary directory for download
            project_root = Path(__file__).parent.parent.parent.parent
            temp_dir = os.path.join(project_root, 'temp_downloads')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Extract username and shortcode from URL
            parts = post_url.split('/')
            username = parts[3]
            shortcode = parts[4]
            
            # Run instagram-scraper command
            command = [
                '--destination', temp_dir,
                '--media-types', 'image,video',
                '--quiet',
                '--include-location',
                '--media-metadata',
                '--latest-stamps',
                '--template', '{shortcode}'
            ]
            
            try:
                subprocess.run(command, check=True)
                # Check if the specific post is downloaded
                downloaded_files = [f for f in os.listdir(temp_dir) if shortcode in f]
                if downloaded_files:
                    logger.info(f"Post downloaded successfully to: {temp_dir}")
                    return temp_dir
                else:
                    logger.error("Specific post not found in downloaded files")
                    return None
            except subprocess.CalledProcessError as e:
                logger.error(f"Error during post download with instagram-scraper: {str(e)}")
                return None
        except Exception as e:
            logger.error(f"Error in download_post_with_scraper: {str(e)}")
            return None
        finally:
            # Clean up temporary files, except the downloaded post
            try:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if shortcode not in file:
                            os.remove(os.path.join(root, file))
            except Exception as e:
                logger.error(f"Error cleaning up temp files: {str(e)}")

    def download_post_with_instaloader(self, post_url: str, user_id: int) -> Optional[dict]:
        try:
            logger.info(f"Starting download for Instagram post URL: {post_url}")
            
            # Create a temporary directory for download
            project_root = Path(__file__).parent.parent.parent.parent
            temp_dir = os.path.join(project_root, 'temp_downloads')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Initialize Instaloader
            loader = Instaloader(dirname_pattern=temp_dir, quiet=True)
            
            # Extract shortcode from URL
            shortcode = post_url.split('/')[-2]
            
            # Download the post
            try:
                post = Post.from_shortcode(loader.context, shortcode)
                loader.download_post(post, target=f"instagram_post_{user_id}")
                logger.info(f"Post downloaded successfully to: {temp_dir}")
                return {
                    'path': temp_dir,
                    'caption': post.caption if post.caption else None
                }
            except Exception as e:
                logger.error(f"Error during post download with instaloader: {str(e)}")
                return None
        except Exception as e:
            logger.error(f"Error in download_post_with_instaloader: {str(e)}")
            return None

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
            project_root = Path(__file__).parent.parent.parent.parent
            temp_dir = os.path.join(project_root, 'temp_downloads')
            os.makedirs(temp_dir, exist_ok=True)
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