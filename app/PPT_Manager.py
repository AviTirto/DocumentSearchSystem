import os
import base64
from dotenv import load_dotenv
from Loader import Loader
from OCR import OCRModel
from records import CDB
from types import PPT, Slide

load_dotenv()

class PPTManager:
    def __init__(self):
        self.pdf_directory = "../Econ_301_PPT"
        self.pdf_files = [os.path.join(self.pdf_directory, f) for f in os.listdir(self.pdf_directory) if f.endswith(".pdf")]
        self.loader = Loader()
        self.ocr_model = OCRModel()
        self.cdb = CDB()

    def generate_unique_chunk_id(title, page_num):
        combined = f"{title}_{page_num}"
        return base64.urlsafe_b64encode(combined.encode()).decode()

    def parse_ppt(self, file_path: str) -> PPT:
        ppt = PPT(title=file_path, slides=[])
        images = self.loader.pdf_to_images(file_path)
        total_input_cost = 0
        total_output_cost = 0

        for i in range(len(images)):
            response = self.ocr_model.extract_text(images[i])
            ocr_result = response['result']
            total_input_cost += response['input_cost']
            total_output_cost += response['output_cost']

            slide1 = Slide(
                id=self.generate_unique_chunk_id(file_path, 2*i + 1),
                page_num=i+1,
                rag_text=self.loader.clean_text_for_rag(ocr_result.slide_1_text),
                full_text=ocr_result.slide_1_text,
            )

            ppt.slides += [slide1]

            if ocr_result.slide_2_text:
                slide2 = Slide(
                    id=self.generate_unique_chunk_id(file_path, 2*i + 2),
                    page_num=i+1,
                    rag_text=self.loader.clean_text_for_rag(ocr_result.slide_2_text),
                    full_text=ocr_result.slide_2_text,
                )

                ppt.slides += [slide2]

            return ppt
        
    def add_ppt(self, ppt: PPT):
        for slide in ppt.slides:
            try:
                self.cdb.add_slide(id = slide.id, title = ppt.title, page_num = slide.page_num, rag_text = slide.rag_text, full_text = slide.full_text)
            except:
                print(f'Error in PPT: {ppt.title} on slide: {slide.page_num}')

        return True

    def populate_ppts(self):
        for file in self.pdf_files:
            ppt = self.parse_ppt(file)
            self.add_ppt(ppt)

    def query(self):
        pass


    

    
    