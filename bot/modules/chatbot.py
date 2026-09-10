import google.generativeai as genai
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ChatType
from bot import app, BOT_NAME, LOGGER
from bot.config import Config
from bot.database import settings_db

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)

# Generation config
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
}

SYSTEM_PROMPT = f"You are a friendly, casual AI assistant in a Telegram chat. You reply like a real human friend — use casual language, sometimes use emojis, keep replies concise (2-4 sentences usually). You can be funny, sarcastic, and have personality. If someone talks in Hindi/Hinglish, reply in the same language. Never say you are an AI unless directly asked. Your name is {BOT_NAME}."

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_PROMPT
)

@app.on_message(filters.command(["chatbot", f"chatbot@{Config.BOT_USERNAME}"]))
async def chatbot_toggle(client, message: Message):
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        # Check if user is admin or owner
        user_id = message.from_user.id
        if user_id != Config.OWNER_ID:
            member = await message.chat.get_member(user_id)
            if not member.privileges:
                return await message.reply_text("You must be an admin to use this command.")

    if len(message.command) < 2:
        return await message.reply_text("Usage: /chatbot [on|off]")
    
    state = message.command[1].lower()
    if state == "on":
        await settings_db.set_chatbot(message.chat.id, True)
        await message.reply_text("✅ Chatbot enabled for this chat.")
    elif state == "off":
        await settings_db.set_chatbot(message.chat.id, False)
        await message.reply_text("❌ Chatbot disabled for this chat.")
    else:
        await message.reply_text("Usage: /chatbot [on|off]")

@app.on_message(filters.command(["lang", f"lang@{Config.BOT_USERNAME}"]))
async def lang_command(client, message: Message):
    if len(message.command) < 2:
        current_lang = await settings_db.get_language(message.chat.id)
        return await message.reply_text(f"Usage: /lang <language>\nCurrent language preference: {current_lang or 'Not set'}")
    
    lang = " ".join(message.command[1:])
    await settings_db.set_language(message.chat.id, lang)
    await message.reply_text(f"✅ Language preference set to: {lang}")

@app.on_message(filters.command(["reset", f"reset@{Config.BOT_USERNAME}"]))
async def reset_command(client, message: Message):
    await settings_db.clear_chat_history(message.chat.id, message.from_user.id)
    await message.reply_text("🧹 Conversation history cleared.")

@app.on_message(filters.text & ~filters.command(["start", "help", "chatbot", "lang", "reset"]) & ~filters.bot)
async def chatbot_handler(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    text = message.text

    if not text or user_id == 0:
        return

    # Check if chatbot is enabled
    is_enabled = await settings_db.get_chatbot(chat_id)
    if not is_enabled:
        return

    # Group chat logic: only reply if mentioned or replied to
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        is_reply = message.reply_to_message and message.reply_to_message.from_user.id == client.me.id
        is_mentioned = getattr(client.me, "username", "") in text if getattr(client.me, "username", "") else False
        
        if not (is_reply or is_mentioned):
            return

    try:
        await client.send_chat_action(chat_id, ChatAction.TYPING)

        # Build history format for Gemini API
        db_history = await settings_db.get_chat_history(chat_id, user_id)
        gemini_history = []
        for role, content in db_history:
            gemini_role = "user" if role == "user" else "model"
            gemini_history.append({"role": gemini_role, "parts": [content]})
        
        # Add user's language preference if set
        lang_pref = await settings_db.get_language(chat_id)
        if lang_pref and lang_pref.lower() != "english":
            prompt_text = f"[Reply strictly in {lang_pref} language/style] {text}"
        else:
            prompt_text = text

        chat_session = model.start_chat(history=gemini_history)
        response = await chat_session.send_message_async(prompt_text)
        
        reply_text = response.text
        if reply_text:
            await message.reply_text(reply_text, quote=True)
            # Save to history
            await settings_db.add_chat_history(chat_id, user_id, "user", text)
            await settings_db.add_chat_history(chat_id, user_id, "bot", reply_text)

    except Exception as e:
        LOGGER.error(f"Error in chatbot: {e}")
        # Send error silently in logs or inform user slightly
        if message.chat.type == ChatType.PRIVATE or (message.reply_to_message and message.reply_to_message.from_user.id == client.me.id):
            await message.reply_text("Oops! I'm having some trouble right now. Please try again later. 🤕", quote=True)
