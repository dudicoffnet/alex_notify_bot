from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(lambda msg: msg.text == "/ping")
async def cmd_ping(message: Message):
    await message.answer("📣 Pong!")