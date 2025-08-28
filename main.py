
import asyncio
import httpx
import os
from datetime import datetime
import zipfile

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("ADMIN_ID")

REPORT_NAME = "report.txt"

def build_report(title="Отчёт"):
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    lines = [
        f"{title} — {now}",
        "",
        "🏠 Снос дома (ул. Мирная, 32, Минск):",
        "• Обновления: (пока нет данных — добавлю по мере поступления)",
        "",
        "✈️ Фукуок (перелёты, жильё, байк, еда, визы):",
        "• Обновления: (пока нет данных — добавлю по мере поступления)",
        "",
        "💰 Возможные заработки и новые схемы:",
        "• Обновления: (пока нет данных — добавлю по мере поступления)",
        "",
        "— Отчёт сгенерирован автоматически ботом-уведомителем."
    ]
    with open(REPORT_NAME, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return REPORT_NAME

def make_backup():
    name = "backup.zip"
    with zipfile.ZipFile(name, "w") as z:
        for fn in os.listdir("."):
            if fn.endswith(".py") or fn.endswith(".txt"):
                z.write(fn)
    return name

async def tg_send_file(path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(path, "rb") as f:
        files = {"document": (path, f)}
        data = {"chat_id": CHAT_ID, "caption": caption}
        async with httpx.AsyncClient(timeout=30) as client:
            await client.post(url, data=data, files=files)

async def handle_force():
    txt = build_report("Отчёт по запросу (/force)")
    await tg_send_file(txt, "📄 Отчёт по команде /force")
    zip_path = make_backup()
    await tg_send_file(zip_path, "📦 Целевой архив (force)")

async def listen_updates():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    offset = 0
    while True:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.get(url, params={"offset": offset + 1, "timeout": 25})
                for u in r.json().get("result", []):
                    offset = u["update_id"]
                    msg = u.get("message") or {}
                    text = (msg.get("text") or "").strip()
                    chat_id = str((msg.get("chat") or {}).get("id", ""))
                    if text == "/force" and chat_id == CHAT_ID:
                        await handle_force()
        except Exception:
            pass
        await asyncio.sleep(2)

async def scheduler():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "10:00":
            txt = build_report("Утренний отчёт")
            await tg_send_file(txt, "📄 Утренний отчёт (TXT)")
        elif now == "23:00":
            txt = build_report("Вечерний отчёт")
            await tg_send_file(txt, "📄 Вечерний отчёт (TXT)")
        await asyncio.sleep(60)

async def main():
    await asyncio.gather(scheduler(), listen_updates())

if __name__ == "__main__":
    asyncio.run(main())
