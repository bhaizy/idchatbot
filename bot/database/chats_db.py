"""
Chats database layer for ID Chatbot.
Handles group and channel registration, verification, counting, retrieval, and deletion.
"""

from typing import List, Dict, Any, Optional
from bot import db, LOGGER


class AsyncCursorList(list):
    """
    Custom list wrapper that provides an async cursor interface
    while remaining fully iterable and indexable as a standard Python list.
    """
    def __aiter__(self):
        return self._async_gen()

    async def _async_gen(self):
        for item in self:
            yield item

    async def to_list(self, length: Optional[int] = None) -> list:
        if length is not None:
            return list(self[:length])
        return list(self)


async def add_chat(chat_id: int, title: str) -> bool:
    """
    Upsert chat doc {_id: chat_id, title: title} into the chats collection.

    :param chat_id: Telegram chat ID (group/supergroup/channel).
    :param title: Title/name of the chat.
    :return: True if upserted/updated successfully, False otherwise.
    """
    try:
        await db.chats.update_one(
            {"_id": chat_id},
            {"$set": {"title": title, "chat_id": chat_id}},
            upsert=True,
        )
        return True
    except Exception as e:
        LOGGER.error(f"Error adding/updating chat {chat_id}: {e}")
        return False


async def is_chat_exist(chat_id: int) -> bool:
    """
    Check if a chat exists in the database.

    :param chat_id: Telegram chat ID.
    :return: True if chat exists, False otherwise.
    """
    try:
        chat = await db.chats.find_one({"_id": chat_id})
        return bool(chat)
    except Exception as e:
        LOGGER.error(f"Error checking chat existence {chat_id}: {e}")
        return False


async def total_chats() -> int:
    """
    Get the total count of registered chats.

    :return: Total number of chats.
    """
    try:
        return await db.chats.count_documents({})
    except Exception as e:
        LOGGER.error(f"Error counting chats: {e}")
        return 0


async def get_all_chats() -> AsyncCursorList:
    """
    Get an async cursor of all chat _ids.
    Supports both async iteration (async for c in ...) and list iteration ([c['chat_id'] for c in ...]).

    :return: AsyncCursorList containing {_id: chat_id, chat_id: chat_id} documents.
    """
    try:
        cursor = db.chats.find({}, {"_id": 1, "title": 1})
        docs = []
        async for doc in cursor:
            cid = doc.get("_id")
            docs.append({"_id": cid, "chat_id": cid, "title": doc.get("title", "")})
        return AsyncCursorList(docs)
    except Exception as e:
        LOGGER.error(f"Error fetching all chats cursor: {e}")
        return AsyncCursorList()


async def delete_chat(chat_id: int) -> bool:
    """
    Delete a chat from the database.

    :param chat_id: Telegram chat ID to delete.
    :return: True if deleted, False otherwise.
    """
    try:
        result = await db.chats.delete_one({"_id": chat_id})
        return result.deleted_count > 0
    except Exception as e:
        LOGGER.error(f"Error deleting chat {chat_id}: {e}")
        return False
