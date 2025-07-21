from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import os
from lib.file_utils import clear_storage

# Регистрация шрифта Arial
pdfmetrics.registerFont(TTFont('Arial', os.path.join(os.path.dirname(__file__), 'fonts', 'arialmt.ttf')))


def draw_header(c, width, height):
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    date_text = f"Дата формирования отчёта: {now_str}"
    c.setFont("Arial", 10)
    text_width = c.stringWidth(date_text, "Arial", 10)
    c.drawString(width - text_width - 40, height - 40, date_text)
    c.setFont("Arial", 16)
    title = "Отчёт из реестра чеков"
    title_width = c.stringWidth(title, "Arial", 16)
    c.drawString((width - title_width) / 2, height - 80, title)


def create_table(data):
    table = Table(data, colWidths=[100, 150, 100])
    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
    ])
    table.setStyle(style)
    return table


""" Convert date format """
def convert_date_format(date: str) -> str:
	return '.'.join(str(date).split('-')[::-1])


""" Creates pdf document """
def create_pdf(file_path, raw_table_data):
	c = canvas.Canvas(file_path, pagesize=A4)
	width, height = A4

	# Преобразуем данные и считаем суммы
	table_data = []
	sum_values = 0.0
	sums_list = []
	for row in raw_table_data:
			sum_val = float(row['sum'])
			sums_list.append(sum_val)
			sum_values += sum_val
			table_data.append([convert_date_format(row['receipt_date']), row['category'], f"{sum_val:.2f}"])

	draw_header(c, width, height)
	table = create_table([["Дата выдачи", "Категория", "Сумма"]] + table_data)
	table_width, table_height = table.wrap(0, 0)
	x = 40
	y = height - 130 - table_height
	table.drawOn(c, x, y)

	count_receipts = len(table_data)
	avg_sum = sum_values / count_receipts if count_receipts else 0
	max_sum = max(sums_list) if sums_list else 0
	min_sum = min(sums_list) if sums_list else 0

	stats_text = (
			f"Итоговая сумма: {sum_values:,.2f}\n"
			f"Количество чеков: {count_receipts}\n"
			f"Средняя сумма чека: {avg_sum:,.2f}\n"
			f"Максимальная сумма: {max_sum:,.2f}\n"
			f"Минимальная сумма: {min_sum:,.2f}"
	)
	c.setFont("Arial", 12)
	text_y = y - 60
	for line in stats_text.split('\n'):
			c.drawString(x, text_y, line)
			text_y -= 18

	clear_storage(extensions=['pdf'])
	c.save()
	print(f"PDF report created: {file_path}")

