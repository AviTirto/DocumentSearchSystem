import fitz  # PyMuPDF

# Path to your local PDF file
PDF_PATH = "Econ 301 PPT/Chapter 9 PPT.pdf"

def extract_raw_pdf(pdf_path):
    """Extracts raw content from each page in a PowerPoint PDF."""
    doc = fitz.open(pdf_path)
    raw_data = []
    
    for page in doc:
        raw_text = page.get_text("rawdict")  # Get raw PDF structure
        raw_data.append(raw_text)
    
    return raw_data

# Get raw data from the PDF
raw_pdf_data = extract_raw_pdf(PDF_PATH)

# Print the raw data of the first page (for example)
for item in raw_pdf_data[0]['blocks']:
    print(item)