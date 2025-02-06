import fitz  # PyMuPDF
import tiktoken

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def chunk_text(text, chunk_size=300, overlap=50):

    encoding = tiktoken.get_encoding("cl100k_base")  # OpenAI tokenizer
    tokens = encoding.encode(text)

    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk_tokens = tokens[i : i + chunk_size]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks

if __name__ == "__main__":
    pdf_path = "Econ 301 Practice Problems/Chapter 1 Practice Problems.pdf"  
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks[:]): 
        print(f"Chunk {i+1}:\n{chunk}\n{'-'*50}")
