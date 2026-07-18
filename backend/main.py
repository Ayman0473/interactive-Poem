from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import sys, os, json, asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embedder import get_mood
from keyword_extractor import extract_keywords
from image_generator import generate_image
from stanza_pipeline import split_into_stanzas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PoemRequest(BaseModel):
    poem: str

@app.post("/generate")
async def generate(req: PoemRequest):
    """Original single-image endpoint — keep for backward compatibility."""
    mood, confidence = get_mood(req.poem)
    keywords = extract_keywords(req.poem, mood)
    generate_image(keywords, mood, "output.png")
    return {
        "mood": mood,
        "confidence": round(confidence, 3),
        "keywords": keywords,
        "image_url": "/image"
    }

@app.get("/image")
def get_image():
    return FileResponse("output.png", media_type="image/png")

@app.post("/generate-stanzas")
async def generate_stanzas(req: PoemRequest):
    """
    Server-sent events endpoint — streams stanza results as they complete.
    Frontend receives each stanza the moment its image is ready.
    """
    stanzas = split_into_stanzas(req.poem)

    async def stream():
        # First event: tell the frontend how many stanzas to expect
        yield f"data: {json.dumps({'type': 'count', 'total': len(stanzas)})}\n\n"

        for i, stanza_text in enumerate(stanzas):
            # Run pipeline for this stanza
            mood, confidence = get_mood(stanza_text)
            keywords = extract_keywords(stanza_text, mood)
            output_path = f"stanza_{i}.png"
            generate_image(keywords, mood, output_path)

            # Stream the result immediately
            event = {
                "type": "stanza",
                "index": i,
                "text": stanza_text,
                "mood": mood,
                "confidence": round(confidence, 3),
                "keywords": keywords,
                "image_url": f"/stanza-image/{i}",
            }
            yield f"data: {json.dumps(event)}\n\n"
            await asyncio.sleep(0.1)

        # Final event: all done
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )

@app.get("/stanza-image/{index}")
def get_stanza_image(index: int):
    path = f"stanza_{index}.png"
    if not os.path.exists(path):
        return {"error": "Image not found"}
    return FileResponse(path, media_type="image/png")