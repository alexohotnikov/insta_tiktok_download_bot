"""
Tests for configuration module.
"""
import os
import pytest
from src.insta_tiktok_bot.config import BotConfig, InstagramConfig, Config, load_config

def test_bot_config():
    """Test BotConfig creation."""
    config = BotConfig(
        token="test_token",
        link="test_link",
        need_password_check=True,
        version="0.3.0"
    )
    assert config.token == "test_token"
    assert config.link == "test_link"
    assert config.need_password_check is True
    assert config.version == "0.3.0"

def test_instagram_config():
    """Test InstagramConfig creation."""
    config = InstagramConfig(
        session_username="test_user",
        session_file="test_session.txt",
        cookies_file="test_cookies.txt"
    )
    assert config.session_username == "test_user"
    assert config.session_file == "test_session.txt"
    assert config.cookies_file == "test_cookies.txt"

def test_config_load_error():
    """Test config loading with missing environment variables."""
    with pytest.raises(ValueError):
        load_config() 