
import os
from reportlab.pdfgen import canvas

def generate_pdf(path: str = "data/report.pdf"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c = canvas.Canvas(path)
    c.setFont("Helvetica", 12)
    c.drawString(72, 780, "Полноценный PDF-доклад")
    c.drawString(72, 760, "⚡ Утро: обновления по проектам, билетам, крипте, дому")
    c.drawString(72, 740, "🌙 Вечер: сводка дня и напоминания")
    c.showPage()
    c.save()
    return path
