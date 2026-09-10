import asyncio
import time
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, PeerIdInvalid, ChatWriteForbidden, ChatAdminRequired

from bot import app, OWNER_ID, LOGGER
from bot.database.users_db import get_all_users, delete_user
from bot.database.chats_db import get_all_chats, delete_chat
from bot.helpers.utils import get_readable_time

broadcast_in_progress = False

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_command(client, message: Message):
    global broadcast_in_progress
    if broadcast_in_progress:
        return await message.reply_text("⏳ A broadcast is already in progress. Please wait for it to finish.")
        
    if not message.reply_to_message:
        return await message.reply_text("❌ Please reply to a message to broadcast it.")
        
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Users Only", callback_data="bcast_users")],
        [InlineKeyboardButton("📤 Groups Only", callback_data="bcast_groups")],
        [InlineKeyboardButton("📤 All (Users+Groups)", callback_data="bcast_all")]
    ])
    
    await message.reply_text("📢 Choose broadcast target:", reply_markup=keyboard, quote=True)


async def send_msg(target_id, message: Message):
    try:
        await message.copy(chat_id=target_id)
        return 200, None
    except FloodWait as e:
        return 420, e.value
    except (UserIsBlocked, InputUserDeactivated, PeerIdInvalid):
        return 400, "Blocked/Deleted"
    except (ChatWriteForbidden, ChatAdminRequired):
        return 403, "Left/Forbidden"
    except Exception as e:
        return 500, str(e)

@app.on_callback_query(filters.regex(r"^bcast_") & filters.user(OWNER_ID))
async def broadcast_callback(client, callback_query: CallbackQuery):
    global broadcast_in_progress
    if broadcast_in_progress:
        return await callback_query.answer("⏳ A broadcast is already in progress.", show_alert=True)
        
    target = callback_query.data.split("_")[1]
    
    if not callback_query.message.reply_to_message:
        return await callback_query.edit_message_text("❌ The original message was deleted.")
        
    msg_to_broadcast = callback_query.message.reply_to_message
    
    broadcast_in_progress = True
    await callback_query.edit_message_text("📢 Preparing broadcast...")
    
    users = []
    chats = []
    
    if target in ["users", "all"]:
        users = await get_all_users()
    if target in ["groups", "all"]:
        chats = await get_all_chats()
        
    all_targets = []
    if users:
        all_targets.extend([u['user_id'] for u in users])
    if chats:
        all_targets.extend([c['chat_id'] for c in chats])
        
    total = len(all_targets)
    if total == 0:
        broadcast_in_progress = False
        return await callback_query.edit_message_text("❌ No targets found in database.")
        
    status_msg = await callback_query.edit_message_text(f"📢 Broadcasting...\n\n✅ Sent: 0\n❌ Failed: 0\n🚫 Blocked: 0\n📊 Total: {total}\n⏱ Elapsed: 0s")
    
    sent = 0
    failed = 0
    blocked = 0
    
    start_time = time.time()
    
    for i, target_id in enumerate(all_targets, 1):
        status, error_info = await send_msg(target_id, msg_to_broadcast)
        
        if status == 200:
            sent += 1
        elif status == 420:
            LOGGER.info(f"FloodWait encountered. Sleeping for {error_info} seconds.")
            await asyncio.sleep(error_info)
            status, error_info = await send_msg(target_id, msg_to_broadcast)
            if status == 200:
                sent += 1
            else:
                failed += 1
        elif status in [400, 403]:
            blocked += 1
            if str(target_id).startswith("-100") or target_id < 0:
                await delete_chat(target_id)
            else:
                await delete_user(target_id)
        else:
            failed += 1
            
        if i % 10 == 0 or i == total:
            elapsed = time.time() - start_time
            readable_time = get_readable_time(elapsed)
            try:
                await status_msg.edit_text(
                    f"📢 Broadcasting...\n\n✅ Sent: {sent}\n❌ Failed: {failed}\n🚫 Blocked: {blocked}\n📊 Total: {total}\n⏱ Elapsed: {readable_time}"
                )
            except Exception:
                pass
                
        await asyncio.sleep(0.1)
        
    elapsed = time.time() - start_time
    readable_time = get_readable_time(elapsed)
    
    final_text = (
        f"✅ Broadcast Completed!\n\n"
        f"📊 Total: {total}\n"
        f"✅ Success: {sent}\n"
        f"❌ Failed: {failed}\n"
        f"🚫 Blocked/Deleted: {blocked}\n"
        f"⏱ Time: {readable_time}"
    )
    
    try:
        await status_msg.edit_text(final_text)
    except Exception:
        await client.send_message(OWNER_ID, final_text)
        
    broadcast_in_progress = False
