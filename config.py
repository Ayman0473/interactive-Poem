import os
from dotenv import load_dotenv

load_dotenv(override=False)

# Debug — print all env vars starting with G
for k, v in os.environ.items():
    if k.startswith('G'):
        print(f"ENV: {k}={v[:4]}...")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(f"GROQ_API_KEY not found. Available vars: {list(os.environ.keys())}")