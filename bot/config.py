"""
Configuration settings for ID Chatbot.
Loads environment variables from .env file or system environment.
Supports both direct attribute access and Config class access.
"""

from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Credentials
BOT_TOKEN = getenv("BOT_TOKEN", None)
API_ID = int(getenv("API_ID", 0) or 0)
API_HASH = getenv("API_HASH", None)

# Database & External Services
MONGO_URL = getenv("MONGO_URL", None)
OWNER_ID = int(getenv("OWNER_ID", 0) or 0)
GEMINI_API_KEY = getenv("GEMINI_API_KEY", None)

# Community & Support Links
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/idchatbot_support")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/idchatbot_channel")

# Bot Identity
BOT_NAME = getenv("BOT_NAME", "ID Chatbot")
BOT_USERNAME = getenv("BOT_USERNAME", "")


class Config:
    """Config class wrapper for modules importing Config directly."""
    BOT_TOKEN = BOT_TOKEN
    API_ID = API_ID
    API_HASH = API_HASH
    MONGO_URL = MONGO_URL
    OWNER_ID = OWNER_ID
    GEMINI_API_KEY = GEMINI_API_KEY
    SUPPORT_GROUP = SUPPORT_GROUP
    SUPPORT_CHANNEL = SUPPORT_CHANNEL
    BOT_NAME = BOT_NAME
    BOT_USERNAME = BOT_USERNAME
