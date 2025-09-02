
from reportlab.pdfgen import canvas
import os

def generate_pdf():
    os.makedirs("data", exist_ok=True)
    c = canvas.Canvas("data/report.pdf")
    c.drawString(100, 750, "Это автоматический PDF-отчёт.")
    c.save()
