from fpdf import FPDF
from datetime import datetime


def create_pdf(input_file, output_file):
    pdf = FPDF()
    # pdf.set_auto_page_break(True, margin=margin_size)
    pdf.add_page()

    title = "AI RMF Report"
    date = str(datetime.now())

    pdf.set_font('Courier', 'B', 24)
    pdf.cell(200, 10, txt=title, ln=1)
    pdf.set_font('Courier', 'B', 14)
    pdf.cell(200, 10, txt=date, ln=1)
    pdf.set_font('Courier', 'B', 12)

    with open(input_file) as f:
        for line in f:
            pdf.multi_cell(0, 10, txt=line)

    pdf.output(output_file)


