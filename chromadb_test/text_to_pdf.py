from fpdf import FPDF
from datetime import datetime

def create_pdf(input_file, output_file):
    margin_size = 1
    text_width = 10
    pdf = FPDF()
    # pdf.set_auto_page_break(True, margin=margin_size)
    pdf.add_page()

    title = "AI RMF Report"
    date = str(datetime.now())
    
    vuln_text = "Vulnerabilities:"

    # replace with dynamic values
    time = "Time: 08:55:00"
    computer_name = "Computer Name: RMF-Client01"
    os_version = "OS Version: Debian 6.1.128-1"
    ip_address = "IP Address: 10.0.0.20"

    pdf.set_font('Courier', 'B', 20)
    pdf.cell(200, 10, txt=title, ln=1)
    pdf.set_font('Courier', 'B', 10)
    pdf.cell(200, 10, txt=date, ln=1)
    pdf.set_font('Courier', 'B', 10)
    pdf.cell(200, 10, txt=time, ln=1)
    pdf.set_font('Courier', 'B', 10)
    pdf.cell(200, 10, txt=computer_name, ln=1)
    pdf.set_font('Courier', 'B', 10)
    pdf.cell(200, 10, txt=os_version, ln=1)
    pdf.set_font('Courier', 'B', 10)
    pdf.cell(200, 10, txt=ip_address, ln=1)

    pdf.cell(200, 10, txt=vuln_text, ln=1)

    pdf.set_font('Courier', 'B', 8)
    

    with open(input_file) as f:
        for line in f:
            # pdf.cell(200, 10, txt=line, ln=1)
            pdf.multi_cell(0, 10, txt=line)


    pdf.output(output_file)



