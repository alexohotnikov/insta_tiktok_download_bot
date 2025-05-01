"""
Tests for downloader module.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from src.insta_tiktok_bot.utils.downloader import InstagramDownloader

@pytest.fixture
def downloader():
    """Create InstagramDownloader instance for testing."""
    return InstagramDownloader("test_cookies.txt")

def test_instagram_downloader_init(downloader):
    """Test InstagramDownloader initialization."""
    assert isinstance(downloader, InstagramDownloader)
    assert downloader.cookies_file.endswith("test_cookies.txt")

@patch('yt_dlp.YoutubeDL')
def test_download_reel_success(mock_ytdl, downloader):
    """Test successful reel download."""
    mock_ytdl.return_value.__enter__.return_value.download.return_value = None
    
    # Мокаем os.path.exists для имитации успешного скачивания
    with patch('os.path.exists', return_value=True):
        result = downloader.download_reel("https://instagram.com/reel/test", 123)
        assert result is not None
        assert "instagram_reel_123.mp4" in result

@patch('yt_dlp.YoutubeDL')
def test_download_reel_failure(mock_ytdl, downloader):
    """Test failed reel download."""
    mock_ytdl.return_value.__enter__.return_value.download.side_effect = Exception("Download failed")
    
    result = downloader.download_reel("https://instagram.com/reel/test", 123)
    assert result is None

@patch('instaloader.Post')
def test_download_post_success(mock_post, downloader):
    """Test successful post download."""
    mock_post.from_shortcode.return_value.caption = "Test caption"
    
    with patch('instaloader.Instaloader'):
        result = downloader.download_post_with_instaloader("https://instagram.com/p/test", 123)
        assert result is not None
        assert isinstance(result, dict)
        assert "path" in result
        assert "caption" in result 