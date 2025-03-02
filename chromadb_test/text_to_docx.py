from docx import Document
from datetime import datetime


def create_docx(input_file, output_file):
    doc = Document()
    # pdf.set_auto_page_break(True, margin=margin_size)

    title = "AI RMF Report"
    date = str(datetime.now())

    time = "08:55:00"
    computer_name = "Computer Name: RMF-Client01"
    os_version = "OS Version: Debian 6.1.128-1"
    ip_address = "IP Address: 10.0.0.20"
	
    doc.add_heading(title, 0)
    doc.add_heading(date, 1)
    doc.add_heading(time, 1)
    doc.add_heading(computer_name, 1)
    doc.add_heading(os_version, 1)
    doc.add_heading(ip_address, 1)


    with open(input_file) as f:
        for line in f:
            doc.add_paragraph(line)

    doc.save(output_file)


