from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot import app, BOT_NAME, BOT_USERNAME

ABOUT_TEXT = f"""
**ℹ️ About {BOT_NAME}**

An advanced AI Chatbot powered by Google Gemini and Pyrogram.

🤖 **Bot:** {BOT_NAME}
🐍 **Python:** 3.11
⚡ **Framework:** Pyrogram
📦 **Database:** MongoDB
"""

HELP_MAIN_TEXT = """
**📚 Help Menu**

Welcome to the Help Menu! Choose a category below to see available commands.
"""

HELP_MAIN_BUTTONS = InlineKeyboardMarkup(
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

HOME_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("📚 Help", callback_data="help_main"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ]
    ]
)

BACK_BUTTON = [[InlineKeyboardButton("⬅️ Back", callback_data="help_main")]]

@app.on_callback_query(filters.regex("^home$"))
async def cb_home(client, query: CallbackQuery):
    await query.message.edit_text(
        text=f"**Hello {query.from_user.first_name}! 👋**\n\nI am {BOT_NAME}, an advanced AI Chatbot powered by Google Gemini. 🤖\nI can talk to you like a real friend, answer your questions, and much more!\n\nClick on the Help button below to see what I can do! ✨",
        reply_markup=HOME_BUTTONS
    )
    await query.answer()

@app.on_callback_query(filters.regex("^about$"))
async def cb_about(client, query: CallbackQuery):
    await query.message.edit_text(
        text=ABOUT_TEXT,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="home")]])
    )
    await query.answer()

@app.on_callback_query(filters.regex("^help_main$"))
async def cb_help_main(client, query: CallbackQuery):
    await query.message.edit_text(
        text=HELP_MAIN_TEXT,
        reply_markup=HELP_MAIN_BUTTONS
    )
    await query.answer()

@app.on_callback_query(filters.regex("^help_general$"))
async def cb_help_general(client, query: CallbackQuery):
    text = "**📚 General Commands**\n\n/start - Start the bot\n/help - Show help menu\n/id - Get chat/user ID\n/ping - Check bot latency"
    await query.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(BACK_BUTTON))
    await query.answer()

@app.on_callback_query(filters.regex("^help_ai$"))
async def cb_help_ai(client, query: CallbackQuery):
    text = "**🤖 AI Chat Commands**\n\n/chatbot [on|off] - Enable/Disable AI chat\n/lang <language> - Set response language\n/reset - Clear conversation history"
    await query.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(BACK_BUTTON))
    await query.answer()

@app.on_callback_query(filters.regex("^help_admin$"))
async def cb_help_admin(client, query: CallbackQuery):
    text = "**👑 Admin Commands (Owner Only)**\n\n/broadcast - Broadcast a message\n/stats - Check bot statistics\n/admin - Admin panel"
    await query.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(BACK_BUTTON))
    await query.answer()

@app.on_callback_query(filters.regex("^help_group$"))
async def cb_help_group(client, query: CallbackQuery):
    text = "**👥 Group Commands**\n\n/chatbot [on|off] - Enable/Disable AI in group\n/lang - Set group AI language"
    await query.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(BACK_BUTTON))
    await query.answer()

@app.on_callback_query(filters.regex("^close$"))
async def cb_close(client, query: CallbackQuery):
    await query.message.delete()
    try:
        await query.answer()
    except:
        pass
