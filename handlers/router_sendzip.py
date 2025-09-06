
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import FSInputFile

router_sendzip = Router()

@router_sendzip.message(Command("sendzip"))
async def send_zip(message: Message):
    file = FSInputFile("storage/alex_notify_bot_v12_payload.zip")
    await message.answer_document(file, caption="📦 Готовый ZIP-файл от Алекса")
