
from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile
from aiogram import Router
import asyncio
import os
from datetime import datetime, time
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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
scheduler = AsyncIOScheduler(timezone=TZ)

SCHEDULE_FILE = "schedule.json"
LOG_FILE = "logs.txt"

def log(msg: str):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {msg}\n")
    except Exception:
        pass

def load_schedule():
    # default times
    schedule = {"morning": "10:00", "evening": "23:00"}
    if os.path.exists(SCHEDULE_FILE):
        try:
            import json
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                schedule.update({k:v for k,v in data.items() if k in ("morning","evening")})
        except Exception:
            pass
    return schedule

def save_schedule(schedule: dict):
    import json
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
        "• Фукуок: мониторинг билетов — подключим источники в следующем релизе",
        "• Бот «Сейчас»: перенос доработок на текущий прод",
        "",
        "💼 <b>Задачи</b>",
        "• Проверка авто-таймеров",
        "• Готовим шаблоны для Canva",
        "",
        "⚙️ <i>Автосообщение сгенерировано ботом-уведомителем.</i>"
    ]
    return "\n".join(lines)

async def send_report_text():
    await bot.send_message(ADMIN_ID, build_report_text())

def build_pdf(path: str):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Ежедневный отчёт")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Дата/время: {datetime.now(TZ).strftime('%d.%m.%Y %H:%M')} (Europe/Minsk)")
    y -= 30
    sections = [
        ("Статус проектов", [
            "Бот-уведомитель: работает",
            "Фукуок: мониторинг билетов — в планах подключения",
            "Бот «Сейчас»: прод-версия, доработки запланированы"
        ]),
        ("Задачи на день", [
            "Проверка авто-таймеров (10:00 / 23:00)",
            "Подготовка шаблонов для роликов"
        ]),
        ("Примечания", [
            "Отчёт сформирован автоматически ботом."
        ])
    ]
    for title, items in sections:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, title)
        y -= 18
        c.setFont("Helvetica", 10)
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
    # Remove existing jobs
    for job in list(scheduler.get_jobs()):
        job.remove()
    schedule = load_schedule()
    h1, m1 = parse_hhmm(schedule["morning"])
    h2, m2 = parse_hhmm(schedule["evening"])
    scheduler.add_job(send_report_text, CronTrigger(hour=h1, minute=m1))
    scheduler.add_job(send_report_text, CronTrigger(hour=h2, minute=m2))
    scheduler.start()
    log(f"Rescheduled: morning {schedule['morning']}, evening {schedule['evening']}")

# === HANDLERS ===
@router.message(F.text == "/start")
async def h_start(message: Message):
    await message.answer("✅ Бот-уведомитель активен. Команды: /ping, /report, /pdfreport, /testnow, /settime HH:MM HH:MM, /backup, /health")

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
        # basic validation
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
    for p in ("schedule.json", "README.txt", "requirements.txt", "Procfile"):
        if os.path.exists(p):
            paths.append(p)
    # не включаем .env, чтобы не утекли секреты
    zname = "backup.zip"
    with zipfile.ZipFile(zname, "w") as z:
        for p in paths:
            z.write(p, arcname=p)
    await bot.send_document(ADMIN_ID, FSInputFile(zname))
    await message.answer("📦 Резервная копия отправлена (без .env).")

@router.message(F.text == "/health")
async def h_health(message: Message):
    schedule = load_schedule()
    jobs = scheduler.get_jobs()
    nexts = []
    for j in jobs:
        try:
            nexts.append(str(j.next_run_time.astimezone(TZ)))
        except Exception:
            nexts.append("—")
    text = (
        "🩺 <b>Статус</b>\n"
        f"• TOKEN: {'OK' if TOKEN else 'EMPTY'}\n"
        f"• ADMIN_ID: {ADMIN_ID}\n"
        f"• TZ: Europe/Minsk\n"
        f"• Расписание: утро {schedule.get('morning')}, вечер {schedule.get('evening')}\n"
        f"• Ближайшие задания: {', '.join(nexts) if nexts else 'нет'}\n"
        "• Логи: пишутся в logs.txt"
    )
    await message.answer(text)

async def main():
    # ensure defaults exist
    if not os.path.exists(SCHEDULE_FILE):
        save_schedule(load_schedule())
    reschedule_jobs()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
