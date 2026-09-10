from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from bot import app

@app.on_message(filters.command("id"))
async def id_command(client, message: Message):
    text = f"👤 **User Info**\n"
    text += f"**First Name:** {message.from_user.first_name}\n"
    if message.from_user.username:
        text += f"**Username:** @{message.from_user.username}\n"
    text += f"**ID:** `{message.from_user.id}`\n\n"
    
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        text += f"💬 **Group Info**\n"
        text += f"**Title:** {message.chat.title}\n"
        text += f"**ID:** `{message.chat.id}`\n\n"
        
    if message.reply_to_message:
        replied = message.reply_to_message.from_user
        if replied:
            text += f"ℹ️ **Replied User Info**\n"
            text += f"**First Name:** {replied.first_name}\n"
            text += f"**ID:** `{replied.id}`\n"
            
    await message.reply_text(text)
