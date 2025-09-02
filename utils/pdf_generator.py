
import os
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(path: str = "data/report.pdf"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c = canvas.Canvas(path)
    c.setFont("Helvetica", 12)
    now = datetime.now()
    hour = now.hour

    c.drawString(72, 800, "Полноценный PDF-доклад")
    if hour < 15:
        c.drawString(72, 780, "⚡ Утренний доклад:")
        c.drawString(72, 760, "• Билеты и поездки")
        c.drawString(72, 740, "• Проекты и задачи")
        c.drawString(72, 720, "• Крипто-обновления")
        c.drawString(72, 700, "• Ситуация с домом")
    else:
        c.drawString(72, 780, "🌙 Вечерний доклад:")
        c.drawString(72, 760, "• Сводка дня")
        c.drawString(72, 740, "• Выполненные задачи")
        c.drawString(72, 720, "• Напоминания на завтра")

    c.showPage()
    c.save()
    return path
