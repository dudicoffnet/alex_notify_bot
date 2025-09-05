import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile
import os
import logging
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BOT_TOKEN = os.getenv("BOT_TOKEN", "your_token_here")
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

@router.message(commands=["start", "ping"])
async def start_handler(message: Message):
    await message.answer("✅ Бот работает. Жду команду /report")

@router.message(commands=["report"])
async def report_handler(message: Message):
    file_path = await create_pdf_report()
    await message.answer_document(document=FSInputFile(file_path), caption="📄 Полный отчёт")

async def create_pdf_report():
    filename = f"report_20250905_225008.pdf"
    file_path = f"/tmp/{filename}"
    c = canvas.Canvas(file_path, pagesize=A4)
    c.setFont("Helvetica", 12)
    lines = '📅 Автоматический отчёт\nДата и время: 2025-09-05 22:50:08\n\n🌴 ФУКУОК:\n— Билеты: мониторинг Минск—Фукуок (через Стамбул, Дубай, Бангкок).  \n— Жильё: бунгало с кухней, отслеживание цен.  \n— Аренда байка, визовые нюансы, местная обстановка.\n\n🏚 СНОС ДОМА:\n— Адрес: Минск, ул. Мирная, д. 32.  \n— Мониторинг официальных планов и обсуждений.\n\n💸 ЗАРАБОТОК:\n— Airdrops: LayerZero, zkSync, StarkNet, Base и др.  \n— Мониторинг крипто-проектов и тестнетов.  \n— Медный порошок: потенциальная перепродажа.\n\n📦 ZIP-АРХИВЫ:\n— Проверка передачи архивов через Telegram-бота.  \n— Обязательная нумерация (v1, v2, …).\n\n🧠 ВЕЧЕРНИЙ ВОПРОС:\n— Что важно зафиксировать за день?\n\n✅ СТАТУСЫ ЗАДАЧ:\n— bot_sichas_prod: в работе, внедряется анкета, меню.  \n— alex_notify_bot: работает, идёт доработка содержимого отчёта.\n'.split("\n")
    y = 800
    for line in lines:
        c.drawString(50, y, line)
        y -= 18
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 800
    c.save()
    return file_path

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
