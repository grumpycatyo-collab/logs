import os
import logging
import asyncio
from aiohttp import web
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, chatid, help_command, handle_message

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HEALTH_PORT = int(os.getenv("HEALTH_PORT", 8080))


async def health(request):
    return web.Response(text="ok")


async def run_health_server():
    app = web.Application()
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", HEALTH_PORT)
    await site.start()
    logger.info(f"Health endpoint running on port {HEALTH_PORT}")


def main() -> None:
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("chatid", chatid))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_health_server())

    logger.info("Bot started")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
