from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(Text(equals="/start"))
async def cmd_start(message: Message):
    await message.answer("Бот запущен. Используй /report или /zip")

@router.message(Text(equals="/report"))
async def cmd_report(message: Message):
    await message.answer("📄 Пока что здесь будет твой PDF-отчёт. В разработке.")