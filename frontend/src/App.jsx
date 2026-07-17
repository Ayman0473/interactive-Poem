import { useState } from "react"

const MOODS = {
  tranquil:   { color: "#5BA865", bg: "#e6f4ec", emoji: "🌿" },
  melancholic:{ color: "#5B8DB8", bg: "#e8f0f9", emoji: "🌧️" },
  joyful:     { color: "#E8A838", bg: "#fdf8e6", emoji: "☀️" },
  defiant:    { color: "#C85250", bg: "#fdf0e8", emoji: "⚡" },
  nostalgic:  { color: "#9B6B9B", bg: "#f5eef8", emoji: "🕰️" },
}

export default function App() {
  const [poem, setPoem]       = useState("")
  const [step, setStep]       = useState("idle")  // idle → loading → mood → keywords → image → done
  const [mood, setMood]       = useState(null)
  const [confidence, setConf] = useState(null)
  const [keywords, setKw]     = useState([])
  const [imageUrl, setImg]    = useState(null)
  const [error, setError]     = useState(null)
  const [visibleKw, setVisKw] = useState(0)

  async function generate() {
    if (!poem.trim()) return
    setStep("loading")
    setMood(null); setConf(null); setKw([]); setImg(null)
    setError(null); setVisKw(0)

    try {
      const res = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ poem })
      })
      if (!res.ok) throw new Error("Server error")
      const data = await res.json()

      // Step 1: show mood
      setMood(data.mood)
      setConf(data.confidence)
      setStep("mood")

      // Step 2: reveal keywords one by one
      await delay(600)
      setKw(data.keywords)
      setStep("keywords")
      for (let i = 1; i <= data.keywords.length; i++) {
        await delay(300)
        setVisKw(i)
      }

      // Step 3: show image
      await delay(400)
      setImg("http://127.0.0.1:8000/image?t=" + Date.now())
      setStep("done")

    } catch(e) {
      setError("Something went wrong. Is the backend running?")
      setStep("idle")
    }
  }

  const delay = ms => new Promise(r => setTimeout(r, ms))
  const m = mood ? MOODS[mood] || { color: "#888", bg: "#f5f5f5", emoji: "✨" } : null

  return (
    <div style={{
      minHeight: "100vh",
      background: "#faf8f4",
      fontFamily: "'DM Sans', system-ui, sans-serif",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      padding: "48px 24px",
    }}>

      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: 40 }}>
        <h1 style={{ fontSize: 32, fontWeight: 300, letterSpacing: -0.5, color: "#1a1814", margin: 0 }}>
          Poem → Visual
        </h1>
        <p style={{ color: "#8a8680", fontSize: 14, marginTop: 8, fontWeight: 300 }}>
          Paste a poem. Watch it become an image.
        </p>
      </div>

      {/* Input */}
      <div style={{ width: "100%", maxWidth: 600 }}>
        <textarea
          value={poem}
          onChange={e => setPoem(e.target.value)}
          placeholder="Paste any poem here..."
          rows={6}
          style={{
            width: "100%", padding: "16px", borderRadius: 12,
            border: "1px solid #e0dbd4", background: "#fff",
            fontSize: 15, lineHeight: 1.6, color: "#1a1814",
            resize: "vertical", outline: "none",
            fontFamily: "inherit", boxSizing: "border-box"
          }}
        />
        <button
          onClick={generate}
          disabled={step === "loading" || !poem.trim()}
          style={{
            marginTop: 12, width: "100%", padding: "14px",
            background: step === "loading" ? "#aaa" : "#2d5a8e",
            color: "#fff", border: "none", borderRadius: 10,
            fontSize: 15, fontWeight: 500, cursor: step === "loading" ? "not-allowed" : "pointer",
            transition: "background 0.2s"
          }}
        >
          {step === "loading" ? "Generating..." : "Generate visual"}
        </button>

        {error && (
          <p style={{ color: "#c0392b", fontSize: 13, marginTop: 8 }}>{error}</p>
        )}
      </div>

      {/* Results */}
      {step !== "idle" && step !== "loading" && (
        <div style={{ width: "100%", maxWidth: 600, marginTop: 32, display: "flex", flexDirection: "column", gap: 16 }}>

          {/* Mood */}
          {mood && (
            <div style={{
              background: m.bg, border: `1px solid ${m.color}40`,
              borderRadius: 12, padding: "16px 20px",
              display: "flex", alignItems: "center", gap: 12,
              animation: "fadeIn 0.4s ease"
            }}>
              <span style={{ fontSize: 28 }}>{m.emoji}</span>
              <div>
                <div style={{ fontSize: 11, color: m.color, fontWeight: 600, textTransform: "uppercase", letterSpacing: 0.5 }}>
                  Mood detected
                </div>
                <div style={{ fontSize: 20, fontWeight: 500, color: "#1a1814", marginTop: 2 }}>
                  {mood.charAt(0).toUpperCase() + mood.slice(1)}
                </div>
                <div style={{ fontSize: 12, color: "#8a8680", marginTop: 2 }}>
                  Confidence: {(confidence * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          )}

          {/* Keywords */}
          {keywords.length > 0 && (
            <div style={{
              background: "#fff", border: "1px solid #e0dbd4",
              borderRadius: 12, padding: "16px 20px",
              animation: "fadeIn 0.4s ease"
            }}>
              <div style={{ fontSize: 11, color: "#8a8680", fontWeight: 600, textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 12 }}>
                Visual keywords
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                {keywords.slice(0, visibleKw).map((kw, i) => (
                  <span key={i} style={{
                    background: "#f5f3ef", color: "#4a4640",
                    padding: "6px 14px", borderRadius: 20,
                    fontSize: 13, fontWeight: 400,
                    animation: "fadeIn 0.3s ease"
                  }}>
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Image */}
          {imageUrl && (
            <div style={{
              borderRadius: 12, overflow: "hidden",
              border: "1px solid #e0dbd4",
              animation: "fadeIn 0.6s ease"
            }}>
              <img
                src={imageUrl}
                alt="Generated visual"
                style={{ width: "100%", display: "block" }}
              />
              <div style={{ padding: "12px 16px", background: "#fff", fontSize: 12, color: "#8a8680" }}>
                Generated from poem embeddings → mood classification → keyword extraction → image synthesis
              </div>
            </div>
          )}

        </div>
      )}

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap');
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
        * { box-sizing: border-box; }
        body { margin: 0; }
        textarea:focus { border-color: #2d5a8e !important; }
      `}</style>
    </div>
  )
}