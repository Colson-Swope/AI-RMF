from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch
from datetime import datetime


def create_pdf(input_file, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=LETTER,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)

    styles = getSampleStyleSheet()
    elements = []

    section_style = styles['Heading2']
    body_style = styles['BodyText']
    bullet_style = styles['Bullet']
    timestamp_style = ParagraphStyle(
        'Timestamp',
        parent=styles['Normal'],
        fontSize=9,
        italic=True,
        spaceAfter=12
    )

    # Create header
    elements.append(Paragraph("Operating System Patch Management RMF Compliance", styles['Title']))
    
    timestamp = datetime.now().strftime("Created %B %d, %Y at %H:%M:%S")
    elements.append(Paragraph(timestamp, timestamp_style))

    # Parse input text
    with open(input_file, 'r') as f:
        lines = f.readlines()

    current_section = None
    buffer = []

    def add_section(title, content):
        if title:
            elements.append(Paragraph(title, section_style))
        bullet_items = []
        for line in content:
            line = line.strip()
            if line.startswith('- '):
                bullet_items.append(ListItem(Paragraph(line[2:], body_style)))
            else:
                if bullet_items:
                    elements.append(ListFlowable(bullet_items, bulletType='bullet'))
                    bullet_items = []
                elements.append(Paragraph(line, body_style))
        if bullet_items:
            elements.append(ListFlowable(bullet_items, bulletType='bullet'))
        elements.append(Spacer(1, 0.2 * inch))

    for line in lines:
        line = line.strip()
        if line.startswith('***') and line.endswith('***'):
            if current_section and buffer:
                add_section(current_section, buffer)
                buffer = []
            current_section = line.strip('* ').strip()
        else:
            buffer.append(line)

    if current_section and buffer:
        add_section(current_section, buffer)

    doc.build(elements)

