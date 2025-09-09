from aiogram import Router
from aiogram.types import Message, FSInputFile
from utils.zip_sender import zip_project

router = Router()

@router.message(lambda msg: msg.text == "/sendzip")
async def cmd_sendzip(message: Message):
    zip_path = zip_project()
    await message.answer_document(FSInputFile(zip_path), caption="📦 Лови ZIP")