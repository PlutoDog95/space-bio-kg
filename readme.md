🚀 Space Biology Knowledge Graph



A web application that leverages AI summarization and a knowledge graph to explore insights from NASA’s bioscience publications.

The system lets you upload publications, generate concise AI-driven summaries, and visualize relationships between experiments, results, and impacts.



📂 Project Structure::



space-bio-kg/

├─ backend/           # FastAPI backend (API + AI summarization)

│  └─ app/main.py

├─ frontend/          # React + Vite frontend (UI)

│  └─ src/App.jsx

├─ ingest/            # Scripts to download/parse NASA PDFs

├─ nlp/               # NLP / summarization pipeline

├─ kg/                # Neo4j knowledge graph integration

├─ data/              # Folder to store NASA PDFs

├─ docker-compose.yml # Container orchestration

├─ .gitignore

└─ README.md



⚙️ Setup Instructions::



1\. Clone the Repository

git clone https://github.com/PlutoDog95/space-bio-kg.git

cd space-bio-kg



2\. Backend Setup (FastAPI)

cd backend

pip install -r requirements.txt





!!Run the backend:



python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000



3\. Frontend Setup (React + Vite)

cd frontend

npm install

npm run dev





Frontend runs at: http://localhost:5173



Backend runs at: http://127.0.0.1:8000





🔑 Environment Variables



Create a .env file in the project root with:



OPENAI\_API\_KEY=your\_api\_key\_here





🚀 Features



Upload NASA bioscience PDFs



Extract and preprocess text



Summarize using AI (OpenAI API or alternatives)



Store metadata and relations in a Neo4j knowledge graph



Explore experiments, results, and impacts visually

