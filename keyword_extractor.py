from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def extract_keywords(poem_text, mood):
    prompt = f"""You are a visual artist and poet. I will give you a poem and its emotional mood.
Your job is to extract 5 specific, painterly, visually rich keywords or short phrases that capture the poem's imagery.

Rules:
- Be specific and concrete, not abstract. "silver morning mist" not "sadness"
- Think like a painter — what would you actually put on canvas?
- Each keyword should be visually distinct from the others
- Reflect both the mood AND the specific imagery in this poem
- Return ONLY a Python list of 5 strings, nothing else. No explanation, no preamble, no markdown.

Poem:
{poem_text}

Mood: {mood}

Example output format:
["silver mist over harbour", "cat on silent haunches", "grey morning light", "still water", "fog rolling in"]

Your output:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )

    raw = response.choices[0].message.content.strip()

    # Remove any markdown code fences if present
    raw = raw.replace("```python", "").replace("```", "").strip()

    import ast
    try:
        keywords = ast.literal_eval(raw)
        if not isinstance(keywords, list):
            raise ValueError("Not a list")
    except:
        # fallback: split by comma if parsing fails
        keywords = [k.strip().strip('"').strip("'") for k in raw.strip("[]").split(",")]

    return keywords

if __name__ == "__main__":
    poem = "I go and lie down where the wood drake rests in his beauty on the water. I come into the peace of wild things who do not tax their lives with forethought of grief."
    mood = "tranquil"
    keywords = extract_keywords(poem, mood)
    print(f"Mood:     {mood}")
    print(f"Keywords: {keywords}")