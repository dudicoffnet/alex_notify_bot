import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram import F
from aiogram.router import Router
from aiogram.filters import Command
import os

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Бот запущен и готов к работе.")

@router.message(Command("ping"))
async def ping_handler(message: types.Message):
    await message.answer("Я на связи.")

@router.message(Command("reportpdf"))
async def report_handler(message: types.Message):
    pdf_path = "storage/daily_report.pdf"
    if os.path.exists(pdf_path):
        await message.answer_document(FSInputFile(pdf_path))
    else:
        await message.answer("Файл отчёта не найден.")

@router.message(Command("sendzip"))
async def sendzip_handler(message: types.Message):
    zip_path = "storage/alex_notify_bot_v15_payload.zip"
    if os.path.exists(zip_path):
        await message.answer_document(FSInputFile(zip_path))
    else:
        await message.answer("ZIP-файл не найден.")

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())