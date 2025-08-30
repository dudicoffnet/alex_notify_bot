from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("🤖 Бот работает. Добро пожаловать!")

@router.message(Command("ping"))
async def ping_cmd(msg: types.Message):
    await msg.answer("🏓 Pong")
