import PyPDF2

def read_pdf(filename):
    with open(filename, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for i, page in enumerate(reader.pages):
            text += f"--- Page {i+1} ---\n"
            text += page.extract_text() + "\n"
            if i > 5:  # limit to first 6 pages for now
                break
        print(text)

read_pdf('/Users/sahanaagadi/Downloads/6th sem/wmn/report/wmn.pdf')
