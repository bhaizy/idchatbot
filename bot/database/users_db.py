"""
Users database layer for ID Chatbot.
Handles user registration, verification, counting, retrieval, and deletion.
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


async def add_user(user_id: int, name: str) -> bool:
    """
    Upsert user doc {_id: user_id, name: name} into the users collection.

    :param user_id: Telegram user ID.
    :param name: Telegram user's first name, full name, or username.
    :return: True if upserted/updated successfully, False otherwise.
    """
    try:
        await db.users.update_one(
            {"_id": user_id},
            {"$set": {"name": name, "user_id": user_id}},
            upsert=True,
        )
        return True
    except Exception as e:
        LOGGER.error(f"Error adding/updating user {user_id}: {e}")
        return False


async def is_user_exist(user_id: int) -> bool:
    """
    Check if a user exists in the database.

    :param user_id: Telegram user ID.
    :return: True if user exists, False otherwise.
    """
    try:
        user = await db.users.find_one({"_id": user_id})
        return bool(user)
    except Exception as e:
        LOGGER.error(f"Error checking user existence {user_id}: {e}")
        return False


async def total_users() -> int:
    """
    Get the total count of registered users.

    :return: Total number of users.
    """
    try:
        return await db.users.count_documents({})
    except Exception as e:
        LOGGER.error(f"Error counting users: {e}")
        return 0


async def get_all_users() -> AsyncCursorList:
    """
    Get an async cursor of all user _ids.
    Supports both async iteration (async for u in ...) and list iteration ([u['user_id'] for u in ...]).

    :return: AsyncCursorList containing {_id: user_id, user_id: user_id} documents.
    """
    try:
        cursor = db.users.find({}, {"_id": 1, "name": 1})
        docs = []
        async for doc in cursor:
            uid = doc.get("_id")
            docs.append({"_id": uid, "user_id": uid, "name": doc.get("name", "")})
        return AsyncCursorList(docs)
    except Exception as e:
        LOGGER.error(f"Error fetching all users cursor: {e}")
        return AsyncCursorList()


async def delete_user(user_id: int) -> bool:
    """
    Delete a user from the database.

    :param user_id: Telegram user ID to delete.
    :return: True if deleted, False otherwise.
    """
    try:
        result = await db.users.delete_one({"_id": user_id})
        return result.deleted_count > 0
    except Exception as e:
        LOGGER.error(f"Error deleting user {user_id}: {e}")
        return False
