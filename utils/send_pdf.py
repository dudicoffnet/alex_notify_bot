from aiogram.types import Message
from reportlab.pdfgen import canvas
import datetime

def generate_pdf(path):
    c = canvas.Canvas(path)
    c.setFont("Helvetica", 14)
    c.drawString(100, 750, f"Отчёт сгенерирован: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 730, "Тестовый отчёт — всё работает ✅")
    c.save()

async def send_pdf_file(message: Message):
    path = "daily_report.pdf"
    generate_pdf(path)
    with open(path, "rb") as pdf:
        await message.answer_document(pdf, caption="PDF отчёт")