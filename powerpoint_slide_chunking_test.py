import re
import streamlit as st
import fitz  # PyMuPDF
from pdf2image import convert_from_path
from bs4 import BeautifulSoup
import os

PDF_PATH = "Econ 301 PPT/Chapter 12 PPT.pdf"

PDF_DIRECTORY = "Econ 301 PPT"


def extract_text_by_slide(pdf_path):
    """Extracts text from each slide in a PowerPoint PDF."""
    doc = fitz.open(pdf_path)
    slides = [{"slide_number": i+1, "text": page.get_text("text"), "html": page.get_text("html")} for i, page in enumerate(doc)]
    return slides

def convert_pdf_to_images(pdf_path):
    """Converts PDF slides to images for display."""
    return convert_from_path(pdf_path)

def clean_text_for_rag(raw_text):
    """Cleans raw text for RAG system: keeps only letters, numbers, and selected symbols, while removing standalone number lines."""
    
    # Define allowed characters
    allowed_chars = r'a-zA-Z0-9+\-*/=<>∑√∞∫≈≠≤≥$%,.\*\(\)\[\]\{\}'

    # Define Unicode ranges for mathematical alphanumeric symbols and numbers
    allowed_unicode = r'\U0001D400-\U0001D7FF\U0001D7CE-\U0001D7FF'

    # Remove all characters **not** in the allowed set
    cleaned_text = re.sub(fr'[^{allowed_chars}{allowed_unicode}\s]', '', raw_text)

    # Remove lines that contain only numbers (including spaces around them)
    # cleaned_text = re.sub(r'^\s*\d+\s*$', '', cleaned_text, flags=re.MULTILINE)

    return cleaned_text

    
    
def clean_text_for_llm(raw_text):
    pass

st.title("PowerPoint PDF Viewer & Slide Extractor")

# Load the PDF
slides = extract_text_by_slide(PDF_PATH)
images = convert_pdf_to_images(PDF_PATH)

# Allow the user to navigate slides
slide_index = st.slider("Slide", 1, len(images), 1) - 1

# Display the slide image and extracted text
st.image(images[slide_index], caption=f"Slide {slides[slide_index]['slide_number']}", use_container_width=True)

# Display the raw extracted text and cleaned HTML text
st.subheader(f"Extracted Text (Slide {slides[slide_index]['slide_number']})")
st.text(slides[slide_index]["text"])

# Clean and display the HTML text
st.subheader(f"Cleaned HTML Text (Slide {slides[slide_index]['slide_number']})")
cleaned_text = clean_html_to_text(slides[slide_index]["html"])
st.text(cleaned_text)
# st.text(slides[slide_index]["html"])

# Apply the custom cleaning function to the raw text for RAG and display it
st.subheader(f"Cleaned Text for RAG (Slide {slides[slide_index]['slide_number']})")
cleaned_for_rag = clean_text_for_rag(slides[slide_index]["text"])
st.text(cleaned_for_rag)

total_pages = 0
pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.endswith(".pdf")]

for pdf_file in pdf_files:
    pdf_path = os.path.join(PDF_DIRECTORY, pdf_file)
    slides = extract_text_by_slide(pdf_path)
    num_pages = len(slides)
    total_pages += num_pages
    print(f"{pdf_file}: {num_pages} pages")

print(f"Total pages across all PDFs: {total_pages}")

