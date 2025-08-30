from aiogram import Router, types
from aiogram.filters import Command
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("🤖 Бот запущен. Я готов к работе.")

@router.message(Command("report"))
async def report_cmd(msg: types.Message):
    os.makedirs("storage/exports", exist_ok=True)
    path = "storage/exports/test_report.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Это тестовый PDF-отчёт от бота.")
    c.save()
    await msg.answer_document(types.FSInputFile(path), caption="📄 Готово")
