"""
Settings and Chat History database layer for ID Chatbot.
Handles chatbot toggle states, language preferences, and rolling conversational memory.
"""

from typing import List, Dict, Any
from bot import db, LOGGER


async def set_chatbot(chat_id: int, status: bool) -> bool:
    """
    Enable or disable chatbot functionality for a specific chat.

    :param chat_id: Telegram chat ID.
    :param status: True to enable chatbot, False to disable.
    :return: True if updated successfully, False otherwise.
    """
    try:
        await db.settings.update_one(
            {"_id": chat_id},
            {"$set": {"chatbot": bool(status)}},
            upsert=True,
        )
        return True
    except Exception as e:
        LOGGER.error(f"Error setting chatbot status for chat {chat_id}: {e}")
        return False


async def get_chatbot(chat_id: int) -> bool:
    """
    Get the chatbot enabled/disabled status for a chat. Defaults to True.

    :param chat_id: Telegram chat ID.
    :return: Boolean indicating whether chatbot is active (default True).
    """
    try:
        doc = await db.settings.find_one({"_id": chat_id}, {"chatbot": 1})
        if doc and "chatbot" in doc:
            return bool(doc["chatbot"])
        return True
    except Exception as e:
        LOGGER.error(f"Error getting chatbot status for chat {chat_id}: {e}")
        return True


async def set_language(chat_id: int, lang: str) -> bool:
    """
    Set preferred language for a specific chat.

    :param chat_id: Telegram chat ID.
    :param lang: Language code (e.g., 'en', 'es', 'hi').
    :return: True if updated successfully, False otherwise.
    """
    try:
        await db.settings.update_one(
            {"_id": chat_id},
            {"$set": {"language": str(lang).lower().strip()}},
            upsert=True,
        )
        return True
    except Exception as e:
        LOGGER.error(f"Error setting language for chat {chat_id}: {e}")
        return False


async def get_language(chat_id: int) -> str:
    """
    Get preferred language for a specific chat. Defaults to 'en'.

    :param chat_id: Telegram chat ID.
    :return: Language code string (default 'en').
    """
    try:
        doc = await db.settings.find_one({"_id": chat_id}, {"language": 1})
        if doc and "language" in doc and doc["language"]:
            return str(doc["language"])
        return "en"
    except Exception as e:
        LOGGER.error(f"Error getting language for chat {chat_id}: {e}")
        return "en"


async def add_chat_history(chat_id: int, user_id: int, role: str, content: str) -> bool:
    """
    Append a message entry {role, content} to conversational history,
    automatically keeping only the last 30 messages.

    :param chat_id: Telegram chat ID.
    :param user_id: Telegram user ID.
    :param role: Message sender role ('user', 'model', 'assistant').
    :param content: Message text content.
    :return: True if added successfully, False otherwise.
    """
    try:
        await db.chat_history.update_one(
            {"_id": f"{chat_id}_{user_id}"},
            {
                "$set": {"chat_id": chat_id, "user_id": user_id},
                "$push": {
                    "history": {
                        "$each": [{"role": role, "content": content}],
                        "$slice": -30,
                    }
                },
            },
            upsert=True,
        )
        return True
    except Exception as e:
        LOGGER.error(f"Error adding chat history for chat {chat_id}, user {user_id}: {e}")
        return False


async def get_chat_history(chat_id: int, user_id: int) -> List[Dict[str, Any]]:
    """
    Retrieve message history list for a user in a chat.

    :param chat_id: Telegram chat ID.
    :param user_id: Telegram user ID.
    :return: List of dictionaries with keys 'role' and 'content'.
    """
    try:
        doc = await db.chat_history.find_one(
            {"_id": f"{chat_id}_{user_id}"},
            {"history": 1},
        )
        if doc and "history" in doc and isinstance(doc["history"], list):
            return doc["history"]
        return []
    except Exception as e:
        LOGGER.error(f"Error retrieving chat history for chat {chat_id}, user {user_id}: {e}")
        return []


async def clear_chat_history(chat_id: int, user_id: int) -> bool:
    """
    Clear all conversational message history for a user in a chat.

    :param chat_id: Telegram chat ID.
    :param user_id: Telegram user ID.
    :return: True if cleared successfully, False otherwise.
    """
    try:
        await db.chat_history.delete_one({"_id": f"{chat_id}_{user_id}"})
        return True
    except Exception as e:
        LOGGER.error(f"Error clearing chat history for chat {chat_id}, user {user_id}: {e}")
        return False
