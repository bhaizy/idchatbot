import time
from pyrogram import filters
from pyrogram.types import Message
from bot import app, OWNER_ID, boot_time
from bot.database.users_db import total_users
from bot.database.chats_db import total_chats
from bot.helpers.utils import get_readable_time

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats_command(client, message: Message):
    start = time.time()
    msg = await message.reply_text("🔄 Fetching statistics...")
    end = time.time()
    
    ping_latency = round((end - start) * 1000)
    
    users_count = await total_users()
    chats_count = await total_chats()
    uptime = get_readable_time(time.time() - boot_time)
    
    stats_text = (
        f"📊 **Bot Statistics**\n\n"
        f"👥 Total Users: {users_count}\n"
        f"💬 Total Groups: {chats_count}\n"
        f"⏱ Uptime: {uptime}\n"
        f"🏓 Ping: {ping_latency}ms"
    )
    
    await msg.edit_text(stats_text)
