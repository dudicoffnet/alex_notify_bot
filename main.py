import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

router = Router()
router_sendzip = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("🤖 Бот запущен. Я готов присылать ZIP и PDF по твоей команде.")

@router.message(F.text == "/ping")
async def ping_handler(message: Message):
    await message.answer("🔴 Я на связи.")

@router.message(F.text == "/reportpdf")
async def report_handler(message: Message):
    try:
        file = FSInputFile("storage/daily_report.pdf")
        await message.answer_document(file, caption="🗂 Твой свежий отчёт")
    except Exception as e:
        await message.answer(f"Не удалось отправить PDF: {e}")

@router_sendzip.message(Command("sendzip"))
async def sendzip_handler(message: Message):
    path = "storage/alex_notify_bot_v12_payload.zip"
    try:
        file = FSInputFile(path)
        await message.answer_document(file, caption="📦 Лови ZIP")
    except Exception as e:
        await message.answer(f"ZIP не отправлен: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher(fsm_strategy=FSMStrategy.CHAT)
    dp.include_router(router)
    dp.include_router(router_sendzip)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
