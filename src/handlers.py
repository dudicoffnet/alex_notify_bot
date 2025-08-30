# Хендлеры
from aiogram import Router, types
from aiogram.filters import Command
import os
from datetime import datetime

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("🤖 Бот-уведомитель запущен. Ожидайте отчётов.")