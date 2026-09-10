"""
ID Chatbot - Core Bot Initialization.
Initializes logging, MongoDB client, Pyrogram client, and global constants.
"""

import logging
import time
from logging.handlers import RotatingFileHandler

from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client

from bot import config

# Record startup timestamp
boot_time = time.time()

# Configure logging (file + console, INFO level, pyrogram set to ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("bot.log", maxBytes=50_000_000, backupCount=10),
        logging.StreamHandler(),
    ],
)

# Suppress overly verbose logs from third-party libraries
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("motor").setLevel(logging.ERROR)

LOGGER = logging.getLogger("IDChatbot")

# MongoDB connection
if config.MONGO_URL:
    mongo = AsyncIOMotorClient(config.MONGO_URL)
else:
    LOGGER.warning("MONGO_URL not configured. Defaulting to local MongoDB URI.")
    mongo = AsyncIOMotorClient("mongodb://localhost:27017")

db = mongo.idchatbot

# Pyrogram Client instance
app = Client(
    "idchatbot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

# Exported constants
OWNER_ID = config.OWNER_ID
BOT_NAME = config.BOT_NAME
BOT_USERNAME = config.BOT_USERNAME
