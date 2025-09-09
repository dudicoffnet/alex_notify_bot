from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import os

def generate_pdf():
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "STSong-Light"
    doc = SimpleDocTemplate("daily_report.pdf")
    story = [Paragraph(f"Привет, Юрий! Сегодня: {datetime.now().strftime('%d.%m.%Y %H:%M')}", style)]
    doc.build(story)
    return "daily_report.pdf"