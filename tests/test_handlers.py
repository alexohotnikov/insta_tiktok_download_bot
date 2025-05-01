"""
Tests for message handlers.
"""
import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, User
from src.insta_tiktok_bot.handlers.base import process_answer

@pytest.fixture
def message():
    """Create mock message."""
    message = AsyncMock(spec=Message)
    message.from_user = AsyncMock(spec=User)
    message.from_user.id = 12345
    message.text = "2в"
    return message

@pytest.fixture
def state():
    """Create mock FSMContext."""
    state = AsyncMock()
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()
    return state

@pytest.mark.asyncio
async def test_process_answer_correct(message, state):
    """Test correct security answer processing."""
    await process_answer(message, state)
    
    state.update_data.assert_called_once_with(passed_security_check=True)
    state.set_state.assert_called_once_with(None)
    assert message.answer.call_count == 2  # Приветствие + changelog

@pytest.mark.asyncio
async def test_process_answer_incorrect(message, state):
    """Test incorrect security answer processing."""
    message.text = "неверный"
    await process_answer(message, state)
    
    state.update_data.assert_not_called()
    message.answer.assert_called_once_with("Ответ неверный. Попробуйте снова.") 