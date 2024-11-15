#
# conftest.py
#


import discord
from discord.ext import commands
import pytest


@pytest.fixture
def bot():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)
    return bot

@pytest.fixture
def mock_send(mocker):
    return mocker.AsyncMock()

@pytest.fixture
def mock_reply(mocker):
    return mocker.AsyncMock()

@pytest.fixture
def mock_user(mocker):
    user = mocker.MagicMock(spec=discord.User)
    user.id = 1234567890
    user.name = "TestUser"
    user.mention = "@TestUser"
    user.display_name = "TestUserDisplayName"
    return user

@pytest.fixture
def mock_ctx(bot, mock_send, mock_reply, mock_user):
    class MockContext:
        def __init__(self, bot):
            self.bot = bot
            self.send = mock_send
            self.reply = mock_reply
            self.author = mock_user
    
    return MockContext(bot)
