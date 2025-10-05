from fastapi import FastAPI, UploadFile, File
import pdfplumber
from transformers import pipeline

app = FastAPI(title="Space Mission PDF Summarizer")

# Initialize summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    # Read PDF
    with pdfplumber.open(file.file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "

    # Clean text
    text = " ".join(text.split())  # remove extra spaces/line breaks

    # Split text into chunks if too long (BART has ~1024 token limit)
    max_chunk_size = 1000  # roughly 1000 words per chunk
    words = text.split()
    chunks = [" ".join(words[i:i+max_chunk_size]) for i in range(0, len(words), max_chunk_size)]

    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    final_summary = " ".join(summaries)
    return {"summary": final_summary, "chunks": len(chunks)}
