
from aiogram import Router, types
from aiogram.filters import Command
from utils.zip_sender import send_zip

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот-уведомитель. Жди PDF утром и вечером.")

@router.message()
async def zip_trigger(message: types.Message):
    if "лови архив" in message.text.lower():
        await send_zip(message)
