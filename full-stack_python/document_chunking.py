# document_chunking.py
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def chunk_document(pdf_path, chunk_size=1000):
    doc = fitz.open(pdf_path)
    text = ""
    
    for page in doc:
        text += page.get_text()

    sentences = sent_tokenize(text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size:
            chunks.append(current_chunk)
            current_chunk = sentence
        else:
            current_chunk += " " + sentence
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks
