from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.types import FSInputFile
import os
import asyncio

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())
router = Router()

@router.message(lambda msg: msg.text == "/start")
async def start_handler(message: Message):
    await message.answer("Бот готов. Команды: /zip, /ping, /help")

@router.message(lambda msg: msg.text == "/ping")
async def ping_handler(message: Message):
    await message.answer("✅ Я на связи.")

@router.message(lambda msg: msg.text == "/help")
async def help_handler(message: Message):
    await message.answer("Команды:
/zip — получить последний ZIP
/ping — проверить связь
/help — помощь")

@router.message(lambda msg: msg.text == "/zip")
async def zip_handler(message: Message):
    zip_path = "latest.zip"
    if os.path.exists(zip_path):
        await message.answer_document(document=FSInputFile(zip_path))
    else:
        await message.answer("❌ ZIP-файл ещё не загружен. Свяжись с Алексом.")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())