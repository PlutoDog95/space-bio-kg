import React, { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
      e.dataTransfer.clearData();
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/summarize-pdf", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setSummary(data.summary);
    } catch (err) {
      console.error("Error:", err);
      setSummary("Error summarizing the file.");
    }
    setLoading(false);
  };

  return (
    <div
      className="app"
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
    >
      <header>
        <h1>Space Biology Summarizer</h1>
      </header>

      <section className="upload-section">
        <div className="drop-area">
          {file ? (
            <p>Selected file: {file.name}</p>
          ) : (
            <p>Drag & drop a PDF here or click below to select</p>
          )}
        </div>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload & Summarize</button>
      </section>

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Summarizing… please wait.</p>
        </div>
      )}

      {summary && (
        <section className="summaries-section">
          <h2>Summary:</h2>
          <p>{summary}</p>
        </section>
      )}

      <footer>
        &copy; {new Date().getFullYear()} Space Biology Project. All rights reserved.
      </footer>
    </div>
  );
}

export default App;
