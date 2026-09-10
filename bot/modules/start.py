from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import app, BOT_NAME, BOT_USERNAME, LOGGER
from bot.database import users_db, chats_db
from pyrogram.enums import ChatType

START_TEXT = """
**Hello {first_name}! 👋**

I am {bot_name}, an advanced AI Chatbot powered by Google Gemini. 🤖
I can talk to you like a real friend, answer your questions, and much more!

Click on the Help button below to see what I can do! ✨
"""

START_PHOTO = "https://telegra.ph/file/b9b009cdd5ccefb33405b.jpg" # Placeholder

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("📚 Help", callback_data="help_main"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
            InlineKeyboardButton("💬 Support", url="https://t.me/idchatbot_support")
        ]
    ]
)

@app.on_message(filters.command("start") & filters.private)
async def start_private(client, message: Message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        
        # Save user to DB
        if not await users_db.is_user_exist(user_id):
            await users_db.add_user(user_id, first_name)
            LOGGER.info(f"New user started the bot: {user_id} - {first_name}")

        await message.reply_photo(
            photo=START_PHOTO,
            caption=START_TEXT.format(first_name=first_name, bot_name=BOT_NAME),
            reply_markup=START_BUTTONS
        )
    except Exception as e:
        LOGGER.error(f"Error in start_private: {e}")

@app.on_message(filters.command("start") & filters.group)
async def start_group(client, message: Message):
    try:
        chat_id = message.chat.id
        title = message.chat.title
        
        # Save chat to DB
        if not await chats_db.is_chat_exist(chat_id):
            await chats_db.add_chat(chat_id, title)
            LOGGER.info(f"Bot added to new group: {chat_id} - {title}")

        await message.reply_text("I am alive and ready to chat! 🤖")
    except Exception as e:
        LOGGER.error(f"Error in start_group: {e}")
