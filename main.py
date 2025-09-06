
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
import asyncio
import os

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("✅ Бот запущен и готов к работе.")

@router.message(Command("ping"))
async def ping_handler(message: types.Message):
    await message.answer("🏓 Pong!")

@router.message(Command("reportpdf"))
async def report_pdf(message: types.Message):
    file_path = "storage/daily_report.pdf"
    if os.path.exists(file_path):
        await message.answer_document(FSInputFile(file_path))
    else:
        await message.answer("❌ Отчёт не найден.")

@router.message(Command("sendzip"))
async def send_zip(message: types.Message):
    file_path = "storage/alex_notify_bot_v15_payload.zip"
    if os.path.exists(file_path):
        await message.answer_document(FSInputFile(file_path))
    else:
        await message.answer("❌ ZIP не найден.")

dp.include_router(router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
