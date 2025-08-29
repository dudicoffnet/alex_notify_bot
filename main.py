import asyncio
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import zipfile
import httpx

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

async def send_file(file_path, caption):
    url = f"{TELEGRAM_API}/sendDocument"
    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as f:
            await client.post(url, data={"chat_id": ADMIN_ID, "caption": caption}, files={"document": f})

def generate_pdf():
    filename = "report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Автоотчёт от Алекса")
    c.drawString(100, 730, f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.save()
    return filename

def generate_zip():
    filename = "backup.zip"
    with zipfile.ZipFile(filename, "w") as zipf:
        zipf.writestr("readme.txt", f"Автоархив от {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return filename

async def handle_force():
    pdf = generate_pdf()
    await send_file(pdf, "PDF-отчёт по команде /force")
    zf = generate_zip()
    await send_file(zf, "ZIP-архив по команде /force")

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
            url = f"{TELEGRAM_API}/getMe"
            try:
                async with httpx.AsyncClient() as client:
                    await client.get(url)
            except Exception:
                pass
        await asyncio.sleep(60)

async def poll_updates():
    offset = 0
    while True:
        url = f"{TELEGRAM_API}/getUpdates"
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, params={"offset": offset+1, "timeout":30})
                data = resp.json()
                for update in data.get("result", []):
                    offset = update["update_id"]
                    if "message" in update and "text" in update["message"]:
                        if update["message"]["text"].strip() == "/force":
                            await handle_force()
        except Exception:
            pass

async def main():
    await asyncio.gather(
        scheduler(),
        poll_updates()
    )

if __name__ == "__main__":
    asyncio.run(main())
