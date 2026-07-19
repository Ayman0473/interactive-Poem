import { useState, useRef } from "react"

const MOOD_STYLES = {
  tranquil:    { accent: "#2d8a6e", emoji: "🌿" },
  melancholic: { accent: "#3a5a8a", emoji: "🌧️" },
  joyful:      { accent: "#c8860a", emoji: "☀️" },
  defiant:     { accent: "#8a2a2a", emoji: "⚡" },
  nostalgic:   { accent: "#6a3a8a", emoji: "🕰️" },
}

const DEFAULT_STYLE = { accent: "#555", emoji: "✨" }

function StanzaImage({ url }) {
  const [loaded, setLoaded] = useState(false)
  const [retries, setRetries] = useState(0)

  function handleError() {
    if (retries < 3) {
      setTimeout(() => {
        setRetries(r => r + 1)
      }, 15000)
    }
  }

  // Route through backend proxy to avoid CORB
  const apiUrl = import.meta.env.VITE_API_URL || ""

  const proxied = `${apiUrl}/proxy-image?url=${encodeURIComponent(url)}`
  const src = retries === 0 ? proxied : `${proxied}&_retry=${retries}`

  return (
    <>
      {/* Dark fallback while loading */}
      {!loaded && (
        <div style={{
          position: "absolute", inset: 0,
          background: "#0d0d0d",
          display: "flex", alignItems: "center", justifyContent: "center"
        }}>
          <div style={{ fontSize: 11, color: "#333", letterSpacing: 3, fontFamily: "system-ui" }}>
            RENDERING IMAGE{retries > 0 ? ` (attempt ${retries + 1})` : "..."}
          </div>
        </div>
      )}
      <img
        key={retries}
        src={src}
        alt=""
        onLoad={() => setLoaded(true)}
        onError={handleError}
        style={{
          position: "absolute", inset: 0,
          width: "100%", height: "100%",
          objectFit: "cover",
          filter: "brightness(0.35)",
          opacity: loaded ? 1 : 0,
          transition: "opacity 1s ease",
        }}
      />
    </>
  )
}

export default function App() {
  const [poem, setPoem]       = useState("")
  const [phase, setPhase]     = useState("input")
  const [stanzas, setStanzas] = useState([])
  const [total, setTotal]     = useState(0)
  const [error, setError]     = useState(null)
  const experienceRef         = useRef(null)

  
  async function generate() {
    console.log("API URL:", import.meta.env.VITE_API_URL)
    console.log("Full URL:", `${import.meta.env.VITE_API_URL}/generate-stanzas`)
    if (!poem.trim()) return
    if (!poem.trim()) return
    setPhase("generating")
    setStanzas([])
    setError(null)
    setTotal(0)

    try {
      const apiUrl = import.meta.env.VITE_API_URL || ""
      const res = await fetch(`${apiUrl}/generate-stanzas`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ poem })
      })

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ""

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split("\n")
        buffer = lines.pop()

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue
          const data = JSON.parse(line.slice(6))

          if (data.type === "count") {
            setTotal(data.total)
          } else if (data.type === "stanza") {
            setStanzas(prev => [...prev, data])
          } else if (data.type === "done") {
            setPhase("experience")
            setTimeout(() => {
              experienceRef.current?.scrollIntoView({ behavior: "smooth" })
            }, 300)
          }
        }
      }
    } catch(e) {
      setError("Something went wrong. Is the backend running?")
      setPhase("input")
    }
  }

  function reset() {
    setPhase("input")
    setStanzas([])
    setPoem("")
    setTotal(0)
  }

  return (
    <div style={{ fontFamily: "'Georgia', serif", background: "#0a0a0a", minHeight: "100vh", color: "#fff" }}>

      {/* ── Hero / Input ── */}
      <div style={{
        minHeight: "100vh", display: "flex", flexDirection: "column",
        alignItems: "center", justifyContent: "center",
        padding: "48px 24px", textAlign: "center",
        background: "linear-gradient(180deg, #0a0a0a 0%, #111318 100%)"
      }}>
        <p style={{ fontSize: 12, letterSpacing: 4, textTransform: "uppercase", color: "#666", marginBottom: 16 }}>
          Poem → Visual Experience
        </p>
        <h1 style={{ fontSize: "clamp(32px, 6vw, 64px)", fontWeight: 400, letterSpacing: -1, margin: "0 0 16px", lineHeight: 1.1 }}>
          Every poem has a world<br />
          <span style={{ color: "#888", fontStyle: "italic" }}>waiting inside it.</span>
        </h1>
        <p style={{ fontSize: 16, color: "#666", marginBottom: 40, maxWidth: 480, lineHeight: 1.6, fontFamily: "system-ui" }}>
          Paste any poem. AI detects the mood of each stanza, extracts visual imagery, and generates a scroll-driven experience.
        </p>

        <div style={{ width: "100%", maxWidth: 560 }}>
          <textarea
            value={poem}
            onChange={e => setPoem(e.target.value)}
            placeholder={"Paste your poem here...\n\nSeparate stanzas with a blank line."}
            rows={8}
            style={{
              width: "100%", padding: "20px", borderRadius: 12,
              border: "1px solid #2a2a2a", background: "#111",
              color: "#e0e0e0", fontSize: 15, lineHeight: 1.8,
              resize: "vertical", outline: "none", fontFamily: "Georgia, serif",
              boxSizing: "border-box"
            }}
          />

          {phase === "generating" && (
            <div style={{ margin: "16px 0", textAlign: "left" }}>
              <div style={{ fontSize: 12, color: "#666", fontFamily: "system-ui", marginBottom: 8, letterSpacing: 1 }}>
                BUILDING YOUR EXPERIENCE
              </div>
              <div style={{ background: "#1a1a1a", borderRadius: 8, overflow: "hidden", height: 4 }}>
                <div style={{
                  height: "100%", background: "#4a90d9",
                  width: total > 0 ? `${(stanzas.length / total) * 100}%` : "10%",
                  transition: "width 0.6s ease",
                  borderRadius: 8
                }}/>
              </div>
              <div style={{ fontSize: 12, color: "#555", fontFamily: "system-ui", marginTop: 8 }}>
                {stanzas.length === 0
                  ? "Analysing poem structure..."
                  : `Generated ${stanzas.length} of ${total} stanzas`}
              </div>
            </div>
          )}

          {error && (
            <p style={{ color: "#c0392b", fontSize: 13, marginTop: 8, fontFamily: "system-ui" }}>{error}</p>
          )}

          <button
            onClick={generate}
            disabled={phase === "generating" || !poem.trim()}
            style={{
              marginTop: 12, width: "100%", padding: "16px",
              background: phase === "generating" ? "#222" : "#fff",
              color: phase === "generating" ? "#555" : "#000",
              border: "none", borderRadius: 10, fontSize: 15,
              fontWeight: 600, cursor: phase === "generating" ? "not-allowed" : "pointer",
              fontFamily: "system-ui", letterSpacing: 0.3,
              transition: "all 0.2s"
            }}
          >
            {phase === "generating" ? "Generating..." : "Generate Experience"}
          </button>
        </div>
      </div>

      {/* ── Scroll Experience ── */}
      {stanzas.length > 0 && (
        <div ref={experienceRef}>
          {stanzas.map((stanza, i) => {
            const style = MOOD_STYLES[stanza.mood] || DEFAULT_STYLE
            return (
              <div key={i} style={{
                minHeight: "100vh", position: "relative",
                display: "flex", alignItems: "center", justifyContent: "center",
              }}>

                {/* Background image with retry logic */}
                <StanzaImage url={stanza.image_url} />

                {/* Gradient overlay */}
                <div style={{
                  position: "absolute", inset: 0,
                  background: "linear-gradient(to bottom, transparent 40%, rgba(0,0,0,0.7) 100%)",
                  zIndex: 1
                }}/>

                {/* Content */}
                <div style={{
                  position: "relative", zIndex: 2,
                  maxWidth: 640, padding: "80px 40px",
                  textAlign: "center",
                }}>
                  <div style={{
                    fontSize: 11, letterSpacing: 4, textTransform: "uppercase",
                    color: style.accent, marginBottom: 32, fontFamily: "system-ui"
                  }}>
                    {style.emoji} &nbsp; Stanza {i + 1} &nbsp;·&nbsp; {stanza.mood}
                  </div>

                  <div style={{
                    fontSize: "clamp(18px, 2.5vw, 26px)", lineHeight: 1.9,
                    color: "#f0f0f0", whiteSpace: "pre-line",
                    textShadow: "0 2px 20px rgba(0,0,0,0.8)",
                    marginBottom: 40
                  }}>
                    {stanza.text}
                  </div>

                  <div style={{ display: "flex", flexWrap: "wrap", gap: 8, justifyContent: "center" }}>
                    {stanza.keywords.map((kw, j) => (
                      <span key={j} style={{
                        fontSize: 11, padding: "4px 12px", borderRadius: 20,
                        background: "rgba(255,255,255,0.08)",
                        border: "1px solid rgba(255,255,255,0.12)",
                        color: "#aaa", fontFamily: "system-ui",
                        letterSpacing: 0.3
                      }}>
                        {kw}
                      </span>
                    ))}
                  </div>
                </div>

                {i === 0 && (
                  <div style={{
                    position: "absolute", bottom: 32, left: "50%",
                    transform: "translateX(-50%)", zIndex: 2,
                    fontSize: 11, color: "#555", letterSpacing: 3,
                    textTransform: "uppercase", fontFamily: "system-ui",
                    animation: "pulse 2s infinite"
                  }}>
                    scroll ↓
                  </div>
                )}
              </div>
            )
          })}

          {/* End screen */}
          <div style={{
            minHeight: "60vh", display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "center",
            background: "#0a0a0a", padding: 40, textAlign: "center"
          }}>
            <p style={{ fontSize: 13, color: "#555", letterSpacing: 3, textTransform: "uppercase", fontFamily: "system-ui", marginBottom: 16 }}>
              End of poem
            </p>
            <p style={{ fontSize: 20, color: "#888", fontStyle: "italic", marginBottom: 40 }}>
              {stanzas.length} stanzas · {stanzas.length} worlds
            </p>
            <button onClick={reset} style={{
              padding: "12px 32px", background: "transparent",
              border: "1px solid #333", borderRadius: 8, color: "#888",
              fontSize: 13, cursor: "pointer", fontFamily: "system-ui",
              letterSpacing: 1
            }}>
              Try another poem
            </button>
          </div>
        </div>
      )}

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.4; }
          50% { opacity: 1; }
        }
        * { box-sizing: border-box; }
        body { margin: 0; }
        textarea:focus { border-color: #444 !important; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #0a0a0a; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }
      `}</style>
    </div>
  )
}
