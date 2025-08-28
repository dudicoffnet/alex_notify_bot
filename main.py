
import asyncio
import httpx
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import zipfile

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("ADMIN_ID")

# Подключение шрифта с поддержкой кириллицы
pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))

async def send_file(file_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, "rb") as f:
        files = {"document": (file_path, f)}
        data = {"chat_id": CHAT_ID, "caption": caption}
        async with httpx.AsyncClient() as client:
            await client.post(url, data=data, files=files)

def generate_pdf(report_type="Утренний отчёт"):
    path = "report.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    c.setFont("DejaVuSans", 16)
    c.drawString(50, height - 50, f"{report_type} — {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    c.setFont("DejaVuSans", 12)

    # Три основных блока
    c.drawString(50, height - 100, "🏠 Снос дома (ул. Мирная, 32, Минск):")
    c.drawString(70, height - 120, "• Данных пока нет / обновления подтянутся автоматически")

    c.drawString(50, height - 160, "✈️ Фукуок (перелёты, жильё, байк, еда, визы):")
    c.drawString(70, height - 180, "• Данных пока нет / обновления подтянутся автоматически")

    c.drawString(50, height - 220, "💰 Возможные заработки и новые схемы:")
    c.drawString(70, height - 240, "• Данных пока нет / обновления подтянутся автоматически")

    c.drawString(50, 50, "🧠 Отчёт сгенерирован автоматически ботом-уведомителем")
    c.save()
    return path

async def handle_force():
    pdf = generate_pdf("Отчёт по запросу (/force)")
    await send_file(pdf, "📄 Отчёт сгенерирован по команде")

async def listen_for_force():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    offset = 0
    while True:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, params={"offset": offset + 1})
            updates = r.json().get("result", [])
            for update in updates:
                offset = update["update_id"]
                if "message" in update:
                    text = update["message"].get("text", "")
                    chat = str(update["message"]["chat"]["id"])
                    if text.strip() == "/force" and chat == CHAT_ID:
                        await handle_force()
        await asyncio.sleep(5)

async def scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "10:00":
            pdf = generate_pdf("Утренний отчёт")
            await send_file(pdf, "📄 Утренний отчёт")
        elif now == "23:00":
            pdf = generate_pdf("Вечерний отчёт")
            await send_file(pdf, "📄 Вечерний отчёт")
        await asyncio.sleep(60)

async def main():
    await asyncio.gather(
        scheduler(),
        listen_for_force()
    )

if __name__ == "__main__":
    asyncio.run(main())
