import sys
try:
    import PyPDF2
except ImportError:
    import os
    os.system('pip3 install PyPDF2')
    import PyPDF2

def read_pdf_pages(filename, num_pages):
    try:
        with open(filename, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for i in range(min(num_pages, len(reader.pages))):
                text += f"--- Page {i+1} ---\n"
                text += reader.pages[i].extract_text() + "\n"
            print(f"Content of {filename}:")
            print(text)
    except Exception as e:
        print(f"Error reading {filename}: {e}")

read_pdf_pages('wmn-lab-report.pdf', 1)
read_pdf_pages('129_wmn_labExp.pdf', 3)
