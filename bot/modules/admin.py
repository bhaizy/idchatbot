from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

from bot import app, OWNER_ID, boot_time
from bot.database.users_db import total_users
from bot.database.chats_db import total_chats
from bot.helpers.utils import get_readable_time
import time

@app.on_message(filters.command("admin") & filters.user(OWNER_ID))
async def admin_command(client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats"), InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🤖 AI Settings", callback_data="admin_ai"), InlineKeyboardButton("🔧 Settings", callback_data="admin_settings")],
        [InlineKeyboardButton("❌ Close", callback_data="admin_close")]
    ])
    
    await message.reply_text("🛡️ **Admin Panel**\n\nWelcome to the control panel. Select an option below:", reply_markup=keyboard)

@app.on_callback_query(filters.regex("^admin_") & filters.user(OWNER_ID))
async def admin_callbacks(client, callback_query: CallbackQuery):
    data = callback_query.data
    
    if data == "admin_stats":
        users_count = await total_users()
        chats_count = await total_chats()
        uptime = get_readable_time(time.time() - boot_time)
        
        text = f"📊 **Bot Statistics**\n\n👥 Total Users: {users_count}\n💬 Total Groups: {chats_count}\n⏱ Uptime: {uptime}"
        await callback_query.answer()
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="admin_back")]]))
        
    elif data == "admin_broadcast":
        text = "📢 **Broadcast Module**\n\nTo broadcast a message:\n1. Send the message to this chat.\n2. Reply to that message with `/broadcast`.\n3. Follow the inline buttons."
        await callback_query.answer()
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="admin_back")]]))
        
    elif data == "admin_ai":
        text = "🤖 **AI Settings**\n\nCurrently using Gemini API for AI processing.\nStatus: Active"
        await callback_query.answer()
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="admin_back")]]))
        
    elif data == "admin_settings":
        text = "🔧 **Settings**\n\nGlobal bot settings will appear here."
        await callback_query.answer()
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="admin_back")]]))
        
    elif data == "admin_back":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats"), InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
            [InlineKeyboardButton("🤖 AI Settings", callback_data="admin_ai"), InlineKeyboardButton("🔧 Settings", callback_data="admin_settings")],
            [InlineKeyboardButton("❌ Close", callback_data="admin_close")]
        ])
        await callback_query.answer()
        await callback_query.edit_message_text("🛡️ **Admin Panel**\n\nWelcome to the control panel. Select an option below:", reply_markup=keyboard)
        
    elif data == "admin_close":
        await callback_query.message.delete()
