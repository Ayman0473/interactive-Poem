from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

MOODS = ["melancholic", "joyful", "defiant", "tranquil", "nostalgic"]

def get_mood(poem_text):
    prompt = f"""Classify the emotional mood of this poem into exactly one of these categories: {', '.join(MOODS)}.

Poem:
{poem_text}

Reply with ONLY the mood word, nothing else."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
        temperature=0,
    )

    mood = response.choices[0].message.content.strip().lower()
    if mood not in MOODS:
        mood = "melancholic"
    return mood, 0.85