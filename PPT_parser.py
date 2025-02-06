import fitz
import re

class Loader:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)

    def extract_text(self):
        extracted_text = []
        for page in self.doc:
            extracted_text.append(page.get_text("text"))
        return extracted_text

    def extract_images(self):
        images = []
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                images.append(base_image["image"])
        return images

    @staticmethod
    def clean_text_for_rag(raw_text):
        """Cleans raw text for RAG system: keeps only letters, numbers, and selected symbols, while removing standalone number lines."""
        
        # Define allowed characters
        allowed_chars = r'a-zA-Z0-9+\-*/=<>∑√∞∫≈≠≤≥$%,.\*\(\)\[\]\{\}'

        # Define Unicode ranges for mathematical alphanumeric symbols and numbers
        allowed_unicode = r'\U0001D400-\U0001D7FF\U0001D7CE-\U0001D7FF'

        # Remove all characters **not** in the allowed set
        cleaned_text = re.sub(fr'[^{{allowed_chars}}{{allowed_unicode}}\s]', '', raw_text)

        return cleaned_text