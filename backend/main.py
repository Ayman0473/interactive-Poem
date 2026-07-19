from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import sys, os, json, asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embedder import get_mood
from keyword_extractor import extract_keywords
from image_generator import get_image_url

from fastapi.responses import Response
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # will lock down after deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

class PoemRequest(BaseModel):
    poem: str

def split_into_stanzas(poem_text):
    import re
    raw = re.split(r'\n\s*\n', poem_text.strip())
    return [s.strip() for s in raw if s.strip()]

@app.get("/")
def root():
    return {"status": "ok", "service": "poem-to-visual"}

@app.post("/generate-stanzas")
async def generate_stanzas(req: PoemRequest):
    stanzas = split_into_stanzas(req.poem)

    async def stream():
        yield f"data: {json.dumps({'type': 'count', 'total': len(stanzas)})}\n\n"

        # First pass: stream text + keywords immediately for all stanzas
        stanza_data = []
        for i, stanza_text in enumerate(stanzas):
            loop = asyncio.get_event_loop()
            mood, confidence = await loop.run_in_executor(None, get_mood, stanza_text)
            keywords = await loop.run_in_executor(None, extract_keywords, stanza_text, mood)
            
            data = {
                "index": i,
                "text": stanza_text,
                "mood": mood,
                "confidence": round(confidence, 3),
                "keywords": keywords,
            }
            stanza_data.append(data)

            # Stream text immediately — no image yet
            yield f"data: {json.dumps({'type': 'stanza_text', **data})}\n\n"

        # Second pass: generate images in parallel, stream each as it's ready
        async def generate_image_for_stanza(data):
            loop = asyncio.get_event_loop()
            image_url = await loop.run_in_executor(
                None, get_image_url, data['keywords'], data['mood']
            )
            return {"type": "stanza_image", "index": data['index'], "image_url": image_url}

        tasks = [asyncio.ensure_future(generate_image_for_stanza(d)) for d in stanza_data]
        pending = set(tasks)
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                yield f"data: {json.dumps(task.result())}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )
@app.get("/proxy-image")
async def proxy_image(url: str):
    async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
        r = await client.get(url)
        content_type = r.headers.get("content-type", "image/jpeg")
        return Response(
            content=r.content,
            media_type=content_type,
            headers={
                "Cache-Control": "public, max-age=3600",
                "Access-Control-Allow-Origin": "*",
            }
        )