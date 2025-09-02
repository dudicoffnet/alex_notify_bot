from aiogram.filters import Text
from aiogram import Router
from aiogram.types import Message, FSInputFile
import os

router = Router()

@router.message(Text(equals="/zip"))
async def cmd_zip(message: Message):
    zip_path = "storage/exports/sample.zip"
    if os.path.exists(zip_path):
        await message.answer_document(FSInputFile(zip_path))
    else:
        await message.answer("❌ ZIP-файл не найден.")