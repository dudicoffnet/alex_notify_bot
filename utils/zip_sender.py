
from aiogram.types import FSInputFile

async def send_zip(message):
    zip_file = FSInputFile("alex_notify.zip")
    await message.answer_document(document=zip_file, caption="📦 Лови архив")
