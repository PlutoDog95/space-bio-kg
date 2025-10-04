import React, { useState } from 'react'

export default function App() {
  const [file, setFile] = useState(null)
  const [summary, setSummary] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleUpload = async () => {
    if (!file) return
    setLoading(true)
    setError("")
    setSummary("")

    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch("http://127.0.0.1:8000/summarize-pdf", {
        method: "POST",
        body: formData
      })

      const data = await res.json()

      if (res.ok) {
        setSummary(data.summary)
      } else {
        setError(data.error || "Failed to summarize PDF")
      }

    } catch (err) {
      setError("Error connecting to backend")
    }

    setLoading(false)
  }

  return (
    <div style={{ fontFamily: 'sans-serif', padding: 20 }}>
      <h1>🚀 Space Biology Knowledge Graph</h1>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload} style={{ marginLeft: 10 }}>
        Upload & Summarize
      </button>

      {loading && <p>Processing PDF…</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {summary && (
        <div style={{ marginTop: 20 }}>
          <h2>Summary:</h2>
          <p>{summary}</p>
        </div>
      )}
    </div>
  )
}
