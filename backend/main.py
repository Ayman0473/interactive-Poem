from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embedder import get_mood
from keyword_extractor import extract_keywords
from image_generator import generate_image

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
    mood, confidence = get_mood(req.poem)
    keywords = extract_keywords(req.poem, mood)
    output_path = "output.png"
    generate_image(keywords, mood, output_path)
    return {
        "mood": mood,
        "confidence": round(confidence, 3),
        "keywords": keywords,
        "image_url": "/image"
    }

@app.get("/image")
def get_image():
    return FileResponse("output.png", media_type="image/png")