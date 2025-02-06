import os
from dotenv import load_dotenv
from Loader import Loader
from OCR import OCRModel

load_dotenv()

class PPTManager:
    def __init__(self):
        self.pdf_directory = "../Econ_301_PPT"
        self.pdf_files = [os.path.join(self.pdf_directory, f) for f in os.listdir(self.pdf_directory) if f.endswith(".pdf")]
        self.loader = Loader()
        self.ocr_model = OCRModel()


    

    
    