
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.token import TokenValidationError
from aiogram import Router
from aiogram.types import BotCommand
from aiogram.filters import CommandStart
from aiogram import F

from aiogram import types
import asyncio

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

router = Router()
dp.include_router(router)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Бот запущен и работает!")

async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except TokenValidationError:
        print("❌ Неверный токен. Проверь переменную окружения TOKEN.")

if __name__ == "__main__":
    asyncio.run(main())
