
import asyncio
import httpx
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import zipfile

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("ADMIN_ID")

async def send_file(file_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, "rb") as f:
        files = {"document": (file_path, f)}
        data = {"chat_id": CHAT_ID, "caption": caption}
        async with httpx.AsyncClient() as client:
            await client.post(url, data=data, files=files)

def generate_pdf():
    path = "report.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "📄 УТРО. АВТООТЧЁТ ОТ АЛЕКСА")
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"🕒 Время генерации: {now}")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 120, "🟢 Статус: Бот активен")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 150, "🔧 Все системы работают штатно")
    c.drawString(50, height - 170, "📊 Будет сгенерирован ZIP-архив вечером")
    c.drawString(50, 50, "🧠 Отчёт сгенерирован автоматически")
    c.save()
    return path

def generate_zip():
    zip_filename = "backup.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in os.listdir():
            if file.endswith(".py") or file.endswith(".txt"):
                zipf.write(file)
    return zip_filename

async def scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "10:00":
            pdf = generate_pdf()
            await send_file(pdf, "📄 Утренний отчёт")
        elif now == "23:00":
            zip_path = generate_zip()
            await send_file(zip_path, "📦 Вечерний архив")
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(scheduler())
