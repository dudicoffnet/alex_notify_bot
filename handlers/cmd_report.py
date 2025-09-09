from aiogram import Router
from aiogram.types import Message, FSInputFile
from utils.pdf_gen import generate_pdf

router = Router()

@router.message(lambda msg: msg.text == "/report")
async def cmd_report(message: Message):
    path = generate_pdf()
    await message.answer_document(FSInputFile(path), caption="📦 Твой свежий отчёт")