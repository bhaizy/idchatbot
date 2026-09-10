import time
from pyrogram import filters
from pyrogram.types import Message
from bot import app

@app.on_message(filters.command("ping"))
async def ping_command(client, message: Message):
    start = time.time()
    msg = await message.reply_text("🏓 Pong!")
    end = time.time()
    
    latency = round((end - start) * 1000)
    await msg.edit_text(f"🏓 Pong! {latency}ms")
