
import os
from aiogram import types

async def send_zip(message: types.Message):
    zip_path = "alex_notify.zip"
    with open(zip_path, "rb") as f:
        await message.answer_document(document=f, caption="📦 Лови архив")
