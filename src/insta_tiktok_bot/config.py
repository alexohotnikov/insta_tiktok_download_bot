"""
Configuration module for the Instagram and TikTok download bot.
"""
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class BotConfig:
    """Bot configuration settings."""
    token: str
    link: str

@dataclass
class InstagramConfig:
    """Instagram configuration settings."""
    session_username: str
    session_file: str
    cookies_file: Optional[str] = None

@dataclass
class Config:
    """Main configuration class."""
    bot: BotConfig
    instagram: InstagramConfig
    download_dir: str = "downloads"

def load_config() -> Config:
    """
    Load configuration from environment variables.
    
    Returns:
        Config: Loaded configuration object.
        
    Raises:
        ValueError: If required environment variables are missing.
    """
    bot_token = os.getenv("BOT_TOKEN")
    bot_link = os.getenv("BOT_LINK")
    instagram_username = os.getenv("INSTAGRAM_SESSION_USERNAME")
    instagram_session_file = os.getenv("INSTAGRAM_SESSION_FILE")
    instagram_cookies = os.getenv("INSTAGRAM_COOKIES_FILE")

    if not all([bot_token, bot_link, instagram_username, instagram_session_file]):
        raise ValueError("Missing required environment variables")

    return Config(
        bot=BotConfig(token=bot_token, link=bot_link),
        instagram=InstagramConfig(
            session_username=instagram_username,
            session_file=instagram_session_file,
            cookies_file=instagram_cookies
        )
    ) 