
from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile
from aiogram import Router
import asyncio
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# === ENV ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# === CORE ===
TZ = ZoneInfo("Europe/Minsk")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# Регистрируем шрифт
pdfmetrics.registerFont(TTFont("CustomFont", "fonts/CustomFont.ttf"))

def build_pdf(path: str):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("CustomFont", 16)
    c.drawString(50, y, "Ежедневный отчёт")
    y -= 20
    c.setFont("CustomFont", 10)
    c.drawString(50, y, f"Дата/время: {datetime.now(TZ).strftime('%d.%m.%Y %H:%M')} (Europe/Minsk)")
    y -= 30
    sections = [
        ("Статус проектов", [
            "Бот-уведомитель: работает",
            "Фукуок: мониторинг билетов",
            "Бот «Сейчас»: в работе"
        ]),
        ("Задачи на день", [
            "Проверка авто-таймеров",
            "Подготовка шаблонов для роликов"
        ]),
        ("Примечания", [
            "Отчёт сформирован автоматически ботом."
        ])
    ]
    for title, items in sections:
        c.setFont("CustomFont", 12)
        c.drawString(50, y, title)
        y -= 18
        c.setFont("CustomFont", 10)
        for it in items:
            c.drawString(60, y, f"• {it}")
            y -= 14
        y -= 10
        if y < 80:
            c.showPage()
            y = height - 50
    c.showPage()
    c.save()

async def send_report_pdf():
    path = "report.pdf"
    build_pdf(path)
    await bot.send_document(ADMIN_ID, FSInputFile(path))

@router.message(F.text == "/pdfreport")
async def h_pdf(message: Message):
    await send_report_pdf()
    await message.answer("📄 PDF-отчёт отправлен.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
