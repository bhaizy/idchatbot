"""
ID Chatbot - Main Application Entry Point.
Loads all modules, starts the Pyrogram client, notifies the owner, and idles.
"""

import asyncio
import importlib
import pyrogram
from pyrogram import idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import (
    LOGGER,
    BOT_NAME,
    BOT_USERNAME,
    OWNER_ID,
    app,
    boot_time,
    config,
)

# Dynamically import list of module names
try:
    from bot.modules import ALL_MODULES
except ImportError:
    ALL_MODULES = []


async def main():
    """Start the bot, dynamically load all modules, and handle graceful shutdown."""
    LOGGER.info("Starting ID Chatbot...")

    # Load all module plugins dynamically
    loaded_modules = 0
    for module_name in ALL_MODULES:
        try:
            importlib.import_module(f"bot.modules.{module_name}")
            loaded_modules += 1
            LOGGER.info(f"Loaded module: {module_name}")
        except Exception as e:
            LOGGER.error(f"Failed to load module '{module_name}': {e}", exc_info=True)

    # Start Pyrogram client
    await app.start()

    me = await app.get_me()
    username = me.username or BOT_USERNAME or "IDChatbot"
    name = me.first_name or BOT_NAME or "ID Chatbot"

    # Startup banner
    banner = f"""
======================================================
  🤖 {name} (@{username}) is now ONLINE!
  📦 Loaded {loaded_modules} module(s)
  ⚡ Pyrogram Version: {pyrogram.__version__}
  👑 Owner ID: {OWNER_ID}
======================================================
"""
    print(banner)
    LOGGER.info(f"{name} (@{username}) started successfully!")

    # Send startup notification to OWNER_ID
    if OWNER_ID:
        try:
            buttons = []
            row = []
            if config.SUPPORT_CHANNEL:
                row.append(
                    InlineKeyboardButton(
                        "📢 Channel", url=config.SUPPORT_CHANNEL
                    )
                )
            if config.SUPPORT_GROUP:
                row.append(
                    InlineKeyboardButton(
                        "💬 Support", url=config.SUPPORT_GROUP
                    )
                )
            if row:
                buttons.append(row)

            reply_markup = InlineKeyboardMarkup(buttons) if buttons else None

            startup_text = (
                f"✨ **{name} Started Successfully!**\n\n"
                f"🤖 **Username:** @{username}\n"
                f"🆔 **Bot ID:** `{me.id}`\n"
                f"📦 **Loaded Modules:** `{loaded_modules}`\n"
                f"🚀 **Status:** Online & Ready!"
            )
            await app.send_message(
                chat_id=OWNER_ID,
                text=startup_text,
                reply_markup=reply_markup,
            )
            LOGGER.info(f"Startup notification sent to Owner ({OWNER_ID}).")
        except Exception as e:
            LOGGER.warning(f"Could not send startup message to OWNER_ID ({OWNER_ID}): {e}")

    # Keep bot running until interrupted
    await idle()

    # Graceful shutdown
    LOGGER.info("Stopping bot...")
    await app.stop()
    LOGGER.info("Bot stopped. Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        LOGGER.info("Bot process interrupted. Exiting...")
