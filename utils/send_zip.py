from aiogram.types import Message

async def send_zip_file(message: Message):
    with open("alex_notify_bot_v22_payload.zip", "rb") as zip_file:
        await message.answer_document(zip_file, caption="Готовый ZIP файл")