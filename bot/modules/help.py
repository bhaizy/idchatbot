from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import app

HELP_TEXT = """
**📚 Help Menu**

Welcome to the Help Menu! Choose a category below to see available commands.
"""

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("General", callback_data="help_general"),
            InlineKeyboardButton("AI Chat", callback_data="help_ai")
        ],
        [
            InlineKeyboardButton("Admin", callback_data="help_admin"),
            InlineKeyboardButton("Group", callback_data="help_group")
        ],
        [
            InlineKeyboardButton("❌ Close", callback_data="close")
        ]
    ]
)

@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    await message.reply_text(
        text=HELP_TEXT,
        reply_markup=HELP_BUTTONS
    )
