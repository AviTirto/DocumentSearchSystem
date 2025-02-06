from pydantic import BaseModel, Field
from typing import List

class OCRResult(BaseModel):
    slide_1_text: str = Field(description="Text from slide 1.")
    slide_2_text: str = Field(description="Text from slide 2. If there are two slides. If not then None.")

class Slide(BaseModel):
    id: str
    page_num: int
    rag_text: str
    full_text: str

class PPT(BaseModel):
    title: str
    slides:  List[Slide]