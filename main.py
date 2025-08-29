import asyncio
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import zipfile
import httpx

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

async def send_file(file_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as f:
            await client.post(url, data={"chat_id": ADMIN_ID, "caption": caption}, files={"document": f})

def generate_pdf():
    filename = "report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Утренний автоотчёт от Алекса")
    c.drawString(100, 730, f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.save()
    return filename

def generate_zip():
    filename = "backup.zip"
    with zipfile.ZipFile(filename, "w") as zipf:
        zipf.writestr("readme.txt", f"Автоархив от {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return filename

async def scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "10:00":
            pdf = generate_pdf()
            await send_file(pdf, "Ежедневный PDF-отчёт")
        if now == "23:00":
            zf = generate_zip()
            await send_file(zf, "Ежедневный ZIP-архив")
        # heartbeat каждые 5 минут
        if datetime.now().minute % 5 == 0:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
            try:
                async with httpx.AsyncClient() as client:
                    await client.get(url)
            except Exception:
                pass
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(scheduler())
