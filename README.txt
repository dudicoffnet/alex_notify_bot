
Авто-бот с отчётами + PDF (кириллица) + web-«будильник» + авто-доставка ZIP.

Команды:
/start — справка
/ping — проверка
/report — текстовый отчёт
/pdfreport — PDF-отчёт
/testnow — отправить отчёт сейчас
/settime HH:MM HH:MM — изменить время автоотчётов
/backup — zip с файлами проекта (без .env)
/pushurl https://... — скачать файл по URL и прислать в Telegram
/health — статус и ближайшие задания

HTTP:
GET  /health — JSON ok
POST /api/push?token=SECRET — { "url": "https://.../file.zip", "caption": "..." } → бот скачает и пришлёт

ENV (Railway):
BOT_TOKEN=...
ADMIN_ID=...
SECRET_TOKEN=что-нибудь_секретное
PORT — даётся Railway автоматически

Procfile: web: python main.py
