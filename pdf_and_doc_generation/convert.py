import text_to_docx
import text_to_pdf

input_file = "output.txt"
output_file = "doc_output.docx"

text_to_pdf.create_pdf(input_file, output_file)
text_to_docx.create_docx(input_file, output_file)
