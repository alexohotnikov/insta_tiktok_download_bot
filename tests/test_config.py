"""
Tests for configuration module.
"""
import os
import pytest
from src.insta_tiktok_bot.config import BotConfig, Config, load_config

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

@pytest.fixture(autouse=True)
def clean_env():
    """Clean environment variables before each test."""
    old_env = dict(os.environ)
    os.environ.clear()
    yield
    os.environ.clear()
    os.environ.update(old_env)

def test_config_load_error():
    """Test config loading with missing environment variables."""
    os.environ["BOT_LINK"] = "test_link"
    os.environ["NEED_PASSWORD_CHECK"] = "false"
    os.environ["BOT_VERSION"] = "0.3.0"
    with pytest.raises(ValueError, match="Missing required environment variables"):
        load_config() 