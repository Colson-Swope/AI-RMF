from reportlab.lib.pagesizes import LETTER
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

    list_items = []
    # Add lines to doc
    for line in lines:
        line = line.strip()
        if line.startswith('- ') or line.startswith('+ ') or line.startswith('* '):
            list_items.append(ListItem(Paragraph(line[2:], body_style)))
        else:
            if len(list_items) != 0:
                elements.append(ListFlowable(list_items, bulletType='bullet'))
                list_items = []
            if line.startswith('***') and line.endswith('***'):
                elements.append(Paragraph(line[3:-3], section_style))
                elements.append(Spacer(1, 0.2 * inch))
            elif line.startswith('**') and line.endswith('**'):
                elements.append(Paragraph(line[2:-2], section_style))
                elements.append(Spacer(1, 0.2 * inch))
            else:
                elements.append(Paragraph(line, body_style))


    doc.build(elements)


