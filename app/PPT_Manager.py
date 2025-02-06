import os
import io
from pdf2image import convert_from_path
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.schema import SystemMessage, HumanMessage
from langchain.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
import base64
from Loader import Loader

load_dotenv()

class OCRResult(BaseModel):
    slide_1_text: str = Field(description="Text from slide 1.")
    slide_2_text: str = Field(description="Text from slide 2.")

class PPTManager:
    def __init__(self):
        self.pdf_directory = "../Econ 301 PPT"
        self.ocr_model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest", 
            temperature=0,
            safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,}
        )
        self.pdf_files = [os.path.join(self.pdf_directory, f) for f in os.listdir(self.pdf_directory) if f.endswith(".pdf")]
        self.loader = Loader()
    
    def perform_ocr(self, images):
        ocr_results = []
        
        # Set up the Pydantic parser with OCRResult as the model
        parser = PydanticOutputParser(pydantic_object=OCRResult)

        for i, image in enumerate(images):
            # Convert the image to bytes and save it as a .jpg
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="JPEG")  # Save as JPEG format
            img_data = img_bytes.getvalue()

            # Base64 encode the image data
            img_base64 = base64.b64encode(img_data).decode("utf-8")

            # Send the image as part of the prompt
            messages = [
                SystemMessage(content=f"Extract text from this image to two PowerPoint slides. There are two slides per page. Avoid graph text and ensure only content from the PowerPoint is included. {parser.get_format_instructions()}"),
                HumanMessage(content=img_base64)  # Image passed as base64-encoded string
            ]

            # Prepare and invoke the prompt with the OCR model
            response = self.ocr_model.invoke(messages)

            print(response.content)

            # Parse the model's response using PydanticOutputParser
            ocr_result = parser.parse(response.content)

            # Add the parsed OCR result to the list
            ocr_results.append(ocr_result)

        return ocr_results

    def process_pdfs(self):
        all_results = []
        for pdf_file in self.pdf_files:
            images = self.loader.extract_images(pdf_file)
            results = self.perform_ocr(images)
            all_results.extend(results)
        return all_results
