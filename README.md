# Poem → Visual

A web app that transforms any poem into an AI-generated image by detecting its emotional mood, extracting painterly visual keywords, and synthesising an image from those keywords.

---

## How it works

The pipeline has three stages, each built on top of the last:

**1. Mood detection**
The poem is encoded into a 384-dimensional embedding vector using `sentence-transformers` (`all-MiniLM-L6-v2`). Five mood descriptions (melancholic, joyful, defiant, tranquil, nostalgic) are embedded the same way. Cosine similarity between the poem vector and each mood vector determines the dominant mood — no labelled training data, no classifier trained from scratch. This is zero-shot classification: the geometry of the embedding space does the work.

**2. Keyword extraction**
The poem text and detected mood are sent to Groq's `llama-3.1-8b-instant` model with a prompt that asks for five specific, painterly, visually concrete phrases — the kind a painter would actually put on canvas. "Silver mist over harbour" rather than "sadness".

**3. Image generation**
The keywords are assembled into a prompt and sent to Pollinations.ai, which returns a 512×512 image. The full prompt is visible in the UI so the reasoning is transparent end to end.

---

## What I found interesting

The mood classifier has low confidence on literary text (typically 0.25–0.35) because poets encode emotion through imagery rather than emotional vocabulary. Wendell Berry's tranquil poem about lying down near water got classified as melancholic — but the keywords the LLM extracted were accurate regardless, and the generated image came out hauntingly beautiful: a heron over still dark water, moonlight through grey clouds. The two stages compensate for each other's errors in a way I didn't design intentionally.

The UMAP visualisation from Phase 1 revealed something similar: Carl Sandburg's fog poem, labelled melancholic, clustered with the tranquil poems. The model was right — the poem uses calm, still language (cat feet, silent haunches) even if the human emotional register is melancholic. Embeddings capture semantic content, not the affective interpretation a reader applies.

---

## Stack

| Layer | Technology |
|---|---|
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Keyword extraction | Groq API (llama-3.1-8b-instant) |
| Image generation | Pollinations.ai |
| Backend | FastAPI + Uvicorn |
| Frontend | React + Vite |

---

## Project structure

```
poem_to_visual/
├── backend/
│   └── main.py              # FastAPI server — /generate and /image endpoints
├── frontend/
│   └── src/
│       └── App.jsx          # React UI with step-by-step mood → keywords → image reveal
├── embedder.py              # Sentence embedding + zero-shot mood classification
├── keyword_extractor.py     # Groq API call — poem + mood → visual keywords
├── image_generator.py       # Pollinations.ai call — keywords → image
├── pipeline.py              # End-to-end pipeline (CLI version)
└── config.py                # Loads API keys from .env
```

---

## Running locally

**Prerequisites:** Python 3.10+, Node.js 18+

**1. Clone and set up Python environment**

```bash
git clone https://github.com/yourusername/poem-to-visual.git
cd poem-to-visual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install fastapi uvicorn sentence-transformers groq requests python-dotenv
```

**2. Add API keys**

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_key_here
```

Get a free Groq key at [console.groq.com](https://console.groq.com). No other API keys needed — Pollinations.ai requires no authentication.

**3. Start the backend**

```bash
cd backend
uvicorn main:app --reload
```

Backend runs at `http://127.0.0.1:8000`

**4. Start the frontend**

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

**5. Use it**

Open `http://localhost:5173`, paste any poem, and click Generate Visual.

---

## Example outputs

| Poem | Mood detected | Image |
|---|---|---|
| Wendell Berry — *The Peace of Wild Things* | Melancholic (0.31) | Heron over still water, moonlit reeds |
| Maya Angelou — *Still I Rise* | Melancholic (0.25) | Worn boots on cracked earth, dusty light |
| Thomas Hood — *I Remember* | Nostalgic (0.30) | Ivy-covered door, warm morning light |

---

## Limitations

- The mood classifier performs best on poems with direct emotional vocabulary and struggles with irony, metaphor, and understatement — common in literary poetry. Confidence scores below 0.35 are expected and normal.
- Pollinations.ai is a free public API with no SLA. Generation times vary between 5–30 seconds.
- The sentence-transformer model has a 256-token limit. Poems longer than roughly 180 words are silently truncated — use a representative excerpt for best results.

---

## Background

This project grew out of a scroll-driven poetry website I built earlier in my gap year — a GSAP/ScrollTrigger experience for Frost's *The Road Not Taken*. I wanted to understand what it would take to make that kind of visual interpretation *generative* rather than hand-crafted, which led me to learn sentence embeddings, zero-shot classification, and how language models represent semantic meaning. The gap between what these models understand and what a human reader understands turned out to be the most interesting part.
