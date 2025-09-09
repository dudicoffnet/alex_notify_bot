import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.strategy import FSMStrategy
import logging
import os

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("🤖 Бот запущен. Я готов присылать ZIP и PDF по твоей команде.")

@router.message(F.text == "/ping")
async def ping_handler(message: Message):
    await message.answer("🏓 Я на связи.")

@router.message(F.text == "/zip")
async def zip_handler(message: Message):
    zip_path = "storage/alex_notify_bot_v20.zip"
    if os.path.exists(zip_path):
        await message.answer_document(document=open(zip_path, "rb"), caption="📦 Лови архив")
    else:
        await message.answer("❌ Архив пока не загружен.")

@router.message(F.text == "/report")
async def report_handler(message: Message):
    await message.answer_document(document=open("storage/daily_report.pdf", "rb"), caption="🗂 Твой свежий отчёт")

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot=bot, fsm_strategy=FSMStrategy.CHAT)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
