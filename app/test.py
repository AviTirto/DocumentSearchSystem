import base64
import io
from pdf2image import convert_from_path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# 📌 Define the expected OCR output structure
class OCRResult(BaseModel):
    slide_1_text: str = Field(description="Text from slide 1.")
    slide_2_text: str = Field(description="Text from slide 2.")

# 📌 Convert PDF to images (one image per page)
def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)  # Convert all PDF pages to images
    if not images:
        return None
    return images

# 📌 Convert an image to a base64-encoded string
def image_to_base64(image):
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")  # Save the image as JPEG
    img_bytes = img_bytes.getvalue()

    # Convert image to base64
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    return img_base64

file_path = "../Econ 301 PPT/Chapter 5 PPT.pdf"

# Convert PDF to images
images = pdf_to_images(file_path)

if images is None:
    print("No images were generated from the PDF.")
else:
    # Convert each image to base64
    base64_images = [image_to_base64(img) for img in images]

    # 🔹 Initialize Gemini Flash model
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0
    )

    # 🔹 Setup LangChain's Pydantic Parser
    parser = PydanticOutputParser(pydantic_object=OCRResult)
    
    # 🔹 Send the first base64 image to Gemini with both text and image
    response = model.invoke([
        SystemMessage(
            content=f"Extract text from this image into two PowerPoint slides. There are two slides per page. Avoid graph text and ensure only content from the PowerPoint is included.\n\n{parser.get_format_instructions()}"
        ),
        HumanMessage(
            content=[
                {"type": "text", "text": "Extract text."},  # Adding the text parameter
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_images[0]}"}
            ]
        )
    ])


    # 🔹 Parse the model's response using PydanticOutputParser
    ocr_result = parser.parse(response.content)

    print(response.usage_metadata['input_tokens'])
    print(response.usage_metadata['output_tokens'])

    # Print the parsed OCR results (slide text)
    print("Slide 1 Text:", ocr_result.slide_1_text)
    print("Slide 2 Text:", ocr_result.slide_2_text)
