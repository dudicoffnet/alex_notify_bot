
from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile
from aiogram import Router
import asyncio
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from aiohttp import web
import aiohttp
import json

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "change_me")
PORT = int(os.getenv("PORT", "8080"))

TZ = ZoneInfo("Europe/Minsk")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)
scheduler = AsyncIOScheduler(timezone=TZ)

SCHEDULE_FILE = "schedule.json"

# Register font
PDF_FONT = "Helvetica"
try:
    pdfmetrics.registerFont(TTFont("CustomFont", "fonts/CustomFont.ttf"))
    PDF_FONT = "CustomFont"
except Exception:
    pass

def load_schedule():
    default = {"morning": "10:00", "evening": "23:00"}
    if os.path.exists(SCHEDULE_FILE):
        try:
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for key in ("morning","evening"):
                    if key in data:
                        default[key] = data[key]
        except Exception:
            pass
    return default

def save_schedule(schedule: dict):
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)

def parse_hhmm(s: str):
    h, m = s.split(":")
    return int(h), int(m)

def build_report_text() -> str:
    now = datetime.now(TZ).strftime("%d.%m.%Y %H:%M")
    lines = [
        f"🗓 <b>Отчёт</b> — {now} (Минск)",
        "",
        "📌 <b>Статус проектов</b>",
        "• Бот-уведомитель: работает ✅",
        "",
        "💼 <b>Задачи</b>",
        "• Автоотчёты в 10:00 / 23:00",
        "• Канва: шаблоны роликов",
        "",
        "⚙️ <i>Автосообщение сгенерировано ботом.</i>"
    ]
    return "\n".join(lines)

async def send_report_text():
    await bot.send_message(ADMIN_ID, build_report_text())

def build_pdf(path: str):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont(PDF_FONT, 16)
    c.drawString(50, y, "Ежедневный отчёт")
    y -= 20
    c.setFont(PDF_FONT, 10)
    c.drawString(50, y, f"Дата/время: {datetime.now(TZ).strftime('%d.%m.%Y %H:%M')} (Europe/Minsk)")
    y -= 30
    sections = [
        ("Статус проектов", [
            "Бот-уведомитель: работает",
            "Автоотчёты включены"
        ]),
        ("Задачи", [
            "Проверка таймеров",
            "Подготовка шаблонов для роликов"
        ]),
        ("Примечания", [
            "PDF сформирован автоматически ботом."
        ])
    ]
    for title, items in sections:
        c.setFont(PDF_FONT, 12)
        c.drawString(50, y, title)
        y -= 18
        c.setFont(PDF_FONT, 10)
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

def reschedule_jobs():
    for job in list(scheduler.get_jobs()):
        job.remove()
    schedule = load_schedule()
    h1, m1 = parse_hhmm(schedule["morning"])
    h2, m2 = parse_hhmm(schedule["evening"])
    scheduler.add_job(send_report_text, CronTrigger(hour=h1, minute=m1))
    scheduler.add_job(send_report_text, CronTrigger(hour=h2, minute=m2))
    scheduler.start()

@router.message(F.text == "/start")
async def h_start(message: Message):
    await message.answer("✅ Бот активен. Команды: /ping, /report, /pdfreport, /testnow, /settime HH:MM HH:MM, /backup, /health, /pushurl <URL>")

@router.message(F.text == "/ping")
async def h_ping(message: Message):
    await message.answer("🏓 Бот работает.")

@router.message(F.text == "/report")
async def h_report(message: Message):
    await send_report_text()

@router.message(F.text == "/pdfreport")
async def h_pdf(message: Message):
    await send_report_pdf()
    await message.answer("📄 PDF-отчёт отправлен.")

@router.message(F.text == "/testnow")
async def h_testnow(message: Message):
    await send_report_text()

@router.message(F.text.startswith("/settime"))
async def h_settime(message: Message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            await message.answer("Формат: /settime 09:30 22:15")
            return
        morning, evening = parts[1], parts[2]
        parse_hhmm(morning); parse_hhmm(evening)
        save_schedule({"morning": morning, "evening": evening})
        reschedule_jobs()
        await message.answer(f"⏰ Расписание обновлено: утро {morning}, вечер {evening}")
    except Exception as e:
        await message.answer(f"Ошибка формата. Пример: /settime 09:30 22:15\nДетали: {e}")

@router.message(F.text == "/backup")
async def h_backup(message: Message):
    import zipfile
    paths = []
    for p in ("schedule.json", "README.txt", "requirements.txt", "Procfile", "fonts/CustomFont.ttf"):
        if os.path.exists(p):
            paths.append(p)
    zname = "backup.zip"
    with zipfile.ZipFile(zname, "w") as z:
        for p in paths:
            z.write(p, arcname=p)
    await bot.send_document(ADMIN_ID, FSInputFile(zname))
    await message.answer("📦 Резервная копия отправлена (без .env).")

@router.message(F.text.startswith("/pushurl"))
async def h_pushurl(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        await message.answer("Формат: /pushurl https://example.com/file.zip")
        return
    url = parts[1].strip()
    filename = url.split("/")[-1] or "file.bin"
    path = f"download_{filename}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                with open(path, "wb") as f:
                    f.write(await resp.read())
        await bot.send_document(ADMIN_ID, FSInputFile(path), caption=f"📦 Новый архив: {filename}")
        await message.answer("✅ Архив доставлен.")
    except Exception as e:
        await message.answer(f"❌ Не удалось скачать/доставить: {e}")

@router.message(F.text == "/health")
async def h_health(message: Message):
    jobs = scheduler.get_jobs()
    nexts = ", ".join([str(j.next_run_time.astimezone(TZ)) for j in jobs]) if jobs else "—"
    await message.answer(
        "🩺 <b>Статус</b>\n"
        f"• TOKEN: {'OK' if TOKEN else 'EMPTY'}\n"
        f"• ADMIN_ID: {ADMIN_ID}\n"
        f"• TZ: Europe/Minsk\n"
        f"• Расписание: {load_schedule()}\n"
        f"• Ближайшие задания: {nexts}"
    )

async def handle_root(request):
    return web.Response(text="AlexNotify alive")

async def handle_health(request):
    return web.json_response({"ok": True, "time": datetime.now(TZ).isoformat()})

async def handle_api_push(request):
    token = request.query.get("token", "")
    if token != SECRET_TOKEN:
        return web.json_response({"ok": False, "error": "unauthorized"}, status=401)
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "error": "bad json"}, status=400)
    url = data.get("url")
    caption = data.get("caption", "📦 Новый архив")
    if not url:
        return web.json_response({"ok": False, "error": "url required"}, status=400)
    filename = url.split("/")[-1] or "file.bin"
    path = f"download_{filename}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                with open(path, "wb") as f:
                    f.write(await resp.read())
        await bot.send_document(ADMIN_ID, FSInputFile(path), caption=caption)
        return web.json_response({"ok": True})
    except Exception as e:
        return web.json_response({"ok": False, "error": str(e)})

def create_app():
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/health", handle_health)
    app.router.add_post("/api/push", handle_api_push)
    return app

async def run_http_server():
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    while True:
        await asyncio.sleep(3600)

async def run_bot():
    if not os.path.exists(SCHEDULE_FILE):
        save_schedule(load_schedule())
    reschedule_jobs()
    await dp.start_polling(bot)

async def main():
    await asyncio.gather(run_http_server(), run_bot())

if __name__ == "__main__":
    asyncio.run(main())
