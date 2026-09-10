"""
Custom decorators for ID Chatbot handlers.
Provides authorization checks and role-based access control.
"""

from functools import wraps
from pyrogram.types import CallbackQuery, Message
from bot import LOGGER, OWNER_ID


def admin_only(func):
    """
    Decorator to restrict handler execution to the bot owner (OWNER_ID).
    If the caller is not the owner, replies with an unauthorized warning.
    """
    @wraps(func)
    async def wrapper(client, update, *args, **kwargs):
        user = getattr(update, "from_user", None)
        user_id = user.id if user else None

        if not user_id or user_id != OWNER_ID:
            if isinstance(update, Message):
                await update.reply_text(
                    "⛔ **Access Denied!**\n"
                    "You are not authorized to use this command. Only the bot owner can execute this."
                )
            elif isinstance(update, CallbackQuery):
                await update.answer(
                    "⛔ You are not authorized to perform this action.",
                    show_alert=True,
                )
            LOGGER.warning(
                f"Unauthorized access attempt to `{func.__name__}` by user ID: {user_id}"
            )
            return

        return await func(client, update, *args, **kwargs)

    return wrapper
