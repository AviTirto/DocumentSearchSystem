import streamlit as st
import os
from Loader import Loader  # Ensure Loader is properly implemented

# Set directory where PDFs are stored
PDF_DIR = "../Econ 301 PPT"

# Get list of available PDFs
pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]

# Streamlit UI
st.title("PowerPoint OCR Viewer")

# Select a PDF from the dropdown
selected_pdf = st.selectbox("Choose a PDF", pdf_files)

# Load the selected PDF
loader = Loader(pdf_path=os.path.join(PDF_DIR, selected_pdf))

# Extract images and text
images = loader.extract_images()
texts = loader.extract_text()

# Ensure there are slides in the PDF
if images and texts:
    # Slider to navigate slides
    slide_number = st.slider("Select Slide", 1, len(images), 1)

    # Display slide image
    st.image(images[slide_number - 1], caption=f"Slide {slide_number}", use_container_width=True)

    # Display original OCR text
    with st.expander("Raw OCR Text"):
        st.text(texts[slide_number - 1])

    # Process text using Loader's cleaning function
    cleaned_text = Loader.clean_text_for_rag(texts[slide_number - 1])
    with st.expander("Cleaned OCR Text"):
        st.text(cleaned_text)
else:
    st.warning("No slides found in this PDF.")
