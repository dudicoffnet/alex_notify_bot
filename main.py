
import os, asyncio, logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.base import router as base_router
from scheduler.jobs import setup_scheduler
from web.app import create_app
from aiohttp import web

load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("YOUR_CHAT_ID", "0"))
UPLOAD_SECRET = os.getenv("UPLOAD_SECRET", "please-change-me")
PORT = int(os.getenv("PORT", "8080"))

bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(base_router)

async def start_web():
    app = create_app(bot, CHAT_ID, UPLOAD_SECRET)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logging.info(f"Web server started on :{PORT}")

async def main():
    health_url = f"http://localhost:{PORT}/health"
    setup_scheduler(bot, CHAT_ID, health_url)
    await asyncio.gather(start_web(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
