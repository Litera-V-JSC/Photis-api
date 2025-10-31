from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

pdfmetrics.registerFont(
    TTFont('Arial', os.path.join(os.path.dirname(__file__), 'fonts', 'arialmt.ttf'))
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TableHeader', fontName='Arial', fontSize=12, alignment=1))
styles.add(ParagraphStyle(name='Cyrillic', fontName='Arial', fontSize=12))

def convert_date_format(date: str) -> str:
    return '.'.join(str(date).split('-')[::-1])

def draw_first_page_header(canvas, doc):
    canvas.saveState()
    width, height = A4
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    date_text = f"Дата формирования отчёта: {now_str}"
    canvas.setFont("Arial", 10)
    text_width = canvas.stringWidth(date_text, "Arial", 10)
    canvas.drawString(width - text_width - 40, height - 40, date_text)
    canvas.setFont("Arial", 16)
    title = "Отчёт из реестра"
    title_width = canvas.stringWidth(title, "Arial", 16)
    canvas.drawString((width - title_width) / 2, height - 70, title)
    canvas.restoreState()

def draw_later_page_placeholder(canvas, doc):
    canvas.saveState()
    canvas.restoreState()

def draw_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Arial', 9)
    canvas.drawString(A4[0] - 50, 30, f"Страница {doc.page}")
    canvas.restoreState()

def create_table(data):
    t = Table(data, colWidths=[100, 150, 100])
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
    t.setStyle(style)
    return t

def create_pdf(storage_dir, file_path, raw_table_data):
	doc = SimpleDocTemplate(file_path, pagesize=A4,
							leftMargin=40, rightMargin=40,
							topMargin=100, bottomMargin=60)

	# Prepare data rows
	table_data = []
	sum_values = 0.0
	sums_list = []
	images_paths = list()

	for row in raw_table_data:
		sum_val = float(row['sum'])
		sums_list.append(sum_val)
		sum_values += sum_val
		images_paths.append(os.path.join(storage_dir, row['file_name']))
		table_data.append([convert_date_format(row['creation_date']), row['category'], f"{sum_val:.2f}", row['file_name']])

	# Create table
	data = [["Дата выдачи", "Категория", "Сумма", "Изображение"]] + table_data
	table = create_table(data)

	# Prepare stats text as Paragraphs
	count = len(table_data)
	avg_sum = sum_values / count if count else 0
	max_sum = max(sums_list) if sums_list else 0
	min_sum = min(sums_list) if sums_list else 0

	stats_lines = [
		f"Количество: {count}",
		f"Итоговая сумма: {sum_values:,.2f}",
		f"Средняя сумма: {avg_sum:,.2f}",
		f"Максимальная сумма: {max_sum:,.2f}",
		f"Минимальная сумма: {min_sum:,.2f}",
	]

	story = []
	story.append(table)
	story.append(Spacer(1, 30))
	for line in stats_lines:
		p = Paragraph(line, styles["Cyrillic"])
		story.append(p)

	# --- Add images of items ---
	used_image_paths = list()
	for img_path in images_paths:
		if img_path in used_image_paths:
			continue
			
		used_image_paths.append(img_path)
		try:
			story.append(PageBreak())
			# Fit image into A4 with margins: safe width/height for portrait A4
			max_width, max_height = A4[0] - 80, A4[1] - 120
			img = Image(img_path)
			# Resize proportionally
			img.drawWidth, img.drawHeight = _fit_image(img_path, max_width, max_height)
			story.append(img)
			story.append(Spacer(1, 12))
			story.append(Paragraph(os.path.basename(img_path), styles["Cyrillic"]))
		except Exception as e:
			story.append(Paragraph(f"Ошибка с изображением: {img_path} ({e})", styles["Cyrillic"]))

	# Build PDF with the correct page headers and numbers
	doc.build(
		story,
		onFirstPage=lambda canvas, doc: (draw_first_page_header(canvas, doc), draw_page_number(canvas, doc)),
		onLaterPages=lambda canvas, doc: (draw_later_page_placeholder(canvas, doc), draw_page_number(canvas, doc))
	)
	

# Add proportional image resizing
from PIL import Image as PIL_Image

def _fit_image(img_path, max_width, max_height):
    with PIL_Image.open(img_path) as im:
        width, height = im.size
    aspect = width / height
    if width > max_width:
        width, height = max_width, max_width / aspect
    if height > max_height:
        width, height = max_height * aspect, max_height
    return width, height

