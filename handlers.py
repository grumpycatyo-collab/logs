import os
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from storage import save_log
from dotenv import load_dotenv

load_dotenv()
LOG_CHAT_ID = os.getenv("LOG_CHAT_ID")

user_tries = {}
MAX_TRIES = 3


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "sup? Send me:\nname\ns or f.\n 's' or 'f' should be from a new line. (s - success, f - fail)\n\nmy boy you have 3 tries to play with the bot until your rejections would go to the group"
    )


async def chatid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Chat ID: {update.effective_chat.id}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """How to log:

1. Send a message with 2 lines:
   - Line 1: name
   - Line 2: s (success) or f (fail)

Example:
Anna
s

Commands:
/start - Start the bot
/help - Show this help
/chatid - Get current chat ID"""
    await update.message.reply_text(help_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    lines = text.split("\n")

    if len(lines) < 2:
        await update.message.reply_text("Need 2 lines:\nname\ns or f")
        return

    name = lines[0].strip()
    status_letter = lines[1].strip().lower()

    if status_letter not in ("s", "f"):
        await update.message.reply_text("Line 2 must be 's' or 'f'")
        return

    status = "success" if status_letter == "s" else "fail"
    user = update.effective_user

    entry = {
        "name": name,
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "submitted_by": {
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name
        }
    }

    save_log(entry)

    user_id = user.id
    tries = user_tries.get(user_id, 0) + 1
    user_tries[user_id] = tries

    if tries <= MAX_TRIES:
        remaining = MAX_TRIES - tries
        await update.message.reply_text(f"Practice mode! {remaining} tries left before it goes to the group.")
    else:
        await update.message.reply_text("Logged!")
        record = f"{name} - {status}\nby @{user.username or user.first_name}\n{entry['timestamp']}"
        await context.bot.send_message(chat_id=LOG_CHAT_ID, text=record)
