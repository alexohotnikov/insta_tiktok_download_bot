"""
Tests for downloader module.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.insta_tiktok_bot.utils.downloader import InstagramDownloader

@pytest.fixture
def downloader():
    """Create InstagramDownloader instance for testing."""
    return InstagramDownloader()

@patch('yt_dlp.YoutubeDL')
def test_download_reel_success(mock_ytdl, downloader):
    """Test successful reel download."""
    mock_ytdl.return_value.__enter__.return_value.download.return_value = None
    
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