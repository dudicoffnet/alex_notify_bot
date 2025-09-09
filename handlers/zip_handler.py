from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("sendzip"))
async def zip_handler(message: Message):
    await message.answer("📦 ZIP отправляется... (если не пришёл — Алекс разбирается)")