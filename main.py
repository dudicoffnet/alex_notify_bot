from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram import types
from utils.send_zip import send_zip_file
from utils.send_pdf import send_pdf_file
import asyncio
import os


bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
router = Router()

@router.message(F.text == '/ping')
async def ping_handler(message: Message):
    await message.answer("Я на связи")

@router.message(F.text == '/sendzip')
async def zip_handler(message: Message):
    await send_zip_file(message)

@router.message(F.text == '/report')
async def pdf_handler(message: Message):
    await send_pdf_file(message)

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())