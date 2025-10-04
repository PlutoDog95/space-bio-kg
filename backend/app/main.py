import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.responses import JSONResponse

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Initialize FastAPI
app = FastAPI()

# CORS settings for frontend (Vite default port 5173)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# PDF summarization endpoint
@app.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    try:
        # Extract text from PDF
        with pdfplumber.open(file.file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if not text.strip():
            return JSONResponse(status_code=400, content={"error": "PDF contains no readable text."})

        # Limit text to avoid token issues
        text = text[:4000]

        # OpenAI summarization using v1 API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in summarizing scientific papers."},
                {"role": "user", "content": f"Summarize the following NASA bioscience paper in 3-4 sentences:\n\n{text}"}
            ],
            temperature=0.3,
            max_tokens=300
        )

        summary = response.choices[0].message.content.strip()
        return {"summary": summary}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
