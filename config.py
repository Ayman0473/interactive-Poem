from dotenv import load_dotenv
import os

load_dotenv()


STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
MODELSLAB_API_KEY = os.getenv("MODELSLAB_API_KEY")


if not STABILITY_API_KEY:
    raise ValueError("STABILITY_API_KEY not found in .env")
if not MODELSLAB_API_KEY:
    raise ValueError("MODELSLAB_API_KEY not found in .env")

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY not found in .env")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")