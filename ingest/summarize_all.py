import os
import json
import pdfplumber
from transformers import pipeline
from tqdm import tqdm

DATA_DIR = "data"
SUMMARIES_DIR = "summaries"
os.makedirs(SUMMARIES_DIR, exist_ok=True)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def summarize_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    chunk_size = 1000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
        summaries.append(summary[0]['summary_text'])

    return " ".join(summaries), len(chunks)

pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".pdf")]

for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
    pdf_path = os.path.join(DATA_DIR, pdf_file)
    summary_text, num_chunks = summarize_pdf(pdf_path)

    summary_path = os.path.join(SUMMARIES_DIR, pdf_file + ".json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "pdf_file": pdf_file,
            "summary": summary_text,
            "chunks": num_chunks
        }, f, ensure_ascii=False, indent=4)

print(f"✅ Completed summarizing {len(pdf_files)} PDFs. Summaries saved in '{SUMMARIES_DIR}' folder.")
