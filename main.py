import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.strategy import FSMStrategy

from handlers.commands import register_commands
from utils.send_zip import send_zip_file

import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(lambda msg: msg.text == "/start")
async def start_handler(message: Message):
    await message.answer("Я на СВЯЗИ")

@dp.message(lambda msg: msg.text == "/ping")
async def ping_handler(message: Message):
    await message.answer("pong")

@dp.message(lambda msg: msg.text == "/reportpdf")
async def report_pdf_handler(message: Message):
    await message.answer("PDF отчёты по команде пока не активированы.")

@dp.message(lambda msg: msg.text == "/sendzip")
async def zip_handler(message: Message):
    await send_zip_file(message)

register_commands(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())