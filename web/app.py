
from aiohttp import web
from aiogram import Bot
from aiogram.types import FSInputFile
import os

def create_app(bot: Bot, chat_id: int, upload_secret: str) -> web.Application:
    app = web.Application()

    async def health(request: web.Request):
        return web.Response(text="ok")

    async def uploadzip(request: web.Request):
        secret = request.headers.get("X-Upload-Secret")
        if secret != upload_secret:
            return web.Response(status=403, text="forbidden")

        content = await request.read()
        if not content:
            return web.Response(status=400, text="empty payload")

        zip_path = "alex_notify.zip"
        with open(zip_path, "wb") as f:
            f.write(content)

        await bot.send_document(chat_id, FSInputFile(zip_path), caption="📦 Новый архив от Алекса (webhook)")
        return web.json_response({"status": "ok"})

    app.router.add_get("/health", health)
    app.router.add_post("/uploadzip", uploadzip)
    return app
