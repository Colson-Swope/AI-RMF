from fpdf import FPDF
from datetime import datetime

def create_pdf(input_file, output_file):
    margin_size = 1
    text_width = 10
    pdf = FPDF()
    # pdf.set_auto_page_break(True, margin=margin_size)
    pdf.add_page()

    title = "RMF Report for Operating System Patch Management"

    pdf.set_font('Courier', 'B', 20)
    pdf.cell(200, 10, txt=title, ln=1)
    pdf.set_font('Courier', 'B', 10)
  
    with open(input_file) as f:
        for line in f:
            # pdf.cell(200, 10, txt=line, ln=1)
            pdf.multi_cell(0, 5, txt=line)


    pdf.output(output_file)
