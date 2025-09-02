
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
import os

router = Router()

ZIP_PATH = "alex_notify.zip"

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот-уведомитель. Жди PDF утром и вечером.")

@router.message(Command("pushzip"))
async def pushzip_handler(message: types.Message):
    if not os.path.exists(ZIP_PATH):
        await message.answer("❌ ZIP-файл не найден.")
        return
    zip_file = FSInputFile(ZIP_PATH)
    await message.answer_document(document=zip_file, caption="📦 Новый архив от Алекса (pushzip)")
