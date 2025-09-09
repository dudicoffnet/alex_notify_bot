import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.types import FSInputFile
from io import BytesIO
import zipfile

TOKEN = "your_token_here"
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

@router.message(lambda m: m.text == "/start")
async def start_handler(message: Message):
    await message.answer("✅ Бот работает. Жду команду /sendzip")

@router.message(lambda m: m.text == "/sendzip")
async def send_zip_handler(message: Message):
    await message.answer("📦 ZIP отправляется... (если не пришёл — Алекс разбирается)")
    mem_zip = BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("info.txt", "Этот ZIP создан в памяти и отправлен ботом.")
    mem_zip.seek(0)
    await bot.send_document(message.chat.id, document=mem_zip, filename="alex_notify_bot_payload.zip")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
