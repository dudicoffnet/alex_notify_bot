from aiogram import Router, types
from aiogram.filters import Command
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("🤖 Бот-уведомитель запущен. Ожидайте отчётов.")

@router.message(Command("report"))
async def report_cmd(msg: types.Message):
    pdf_path = "storage/exports/test_report.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setFont("Helvetica", 14)
    c.drawString(100, 750, "Это тестовый PDF-отчёт от бота")
    c.save()
    await msg.answer_document(types.FSInputFile(pdf_path), caption="📄 Ваш PDF-отчёт")
