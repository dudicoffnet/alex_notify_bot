
from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Бот запущен и работает!")

@router.message(F.text == "/ping")
async def cmd_ping(message: Message, state: FSMContext):
    await message.answer("pong")

@router.message(F.text == "/sendzip")
async def cmd_sendzip(message: Message, state: FSMContext):
    await message.answer_document(
        open("payloads/alex_notify_bot_v27.zip", "rb"),
        caption="📦 Актуальный ZIP-архив: alex_notify_bot_v27.zip"
    )

@router.message(F.text == "/reportpdf")
async def cmd_reportpdf(message: Message, state: FSMContext):
    await message.answer_document(
        open("payloads/report.pdf", "rb"),
        caption="📝 PDF-отчёт: свежая версия"
    )

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
