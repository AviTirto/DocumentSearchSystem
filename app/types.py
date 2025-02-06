from pydantic import BaseModel, Field

class OCRResult(BaseModel):
    slide_1_text: str = Field(description="Text from slide 1.")
    slide_2_text: str = Field(description="Text from slide 2.")