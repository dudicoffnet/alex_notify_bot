from aiogram.types import FSInputFile

async def send_zip_file(message):
    try:
        zip_path = "/mnt/data/alex_notify_bot_v23.zip"
        zip_file = FSInputFile(zip_path, filename="alex_notify_bot_v23.zip")
        await message.answer_document(zip_file)
    except Exception as e:
        await message.answer(f"Ошибка при отправке ZIP: {e}")