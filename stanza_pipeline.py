from embedder import get_mood
from keyword_extractor import extract_keywords
from image_generator import generate_image
import re

def split_into_stanzas(poem_text):
    """
    Split a poem into stanzas by blank lines.
    Filters out empty stanzas and strips whitespace.
    """
    raw = re.split(r'\n\s*\n', poem_text.strip())
    stanzas = [s.strip() for s in raw if s.strip()]
    return stanzas

def process_stanza(stanza_text, index):
    """
    Run the full pipeline on a single stanza.
    Returns a dict with stanza text, mood, keywords, and image path.
    """
    print(f"\n── Stanza {index + 1} ──")
    print(f"Text: {stanza_text[:60]}...")

    mood, confidence = get_mood(stanza_text)
    print(f"Mood: {mood} ({confidence})")

    keywords = extract_keywords(stanza_text, mood)
    print(f"Keywords: {keywords}")

    output_path = f"stanza_{index}.png"
    generate_image(keywords, mood, output_path)

    return {
        "index": index,
        "text": stanza_text,
        "mood": mood,
        "confidence": round(confidence, 3),
        "keywords": keywords,
        "image_path": output_path,
    }

def poem_to_stanzas(poem_text):
    """
    Full pipeline: poem text → list of stanza results.
    """
    stanzas = split_into_stanzas(poem_text)
    print(f"Found {len(stanzas)} stanzas")
    results = []
    for i, stanza in enumerate(stanzas):
        result = process_stanza(stanza, i)
        results.append(result)
    return results

if __name__ == "__main__":
    poem = """I go and lie down where the wood drake rests
in his beauty on the water, and the great heron feeds.
I come into the peace of wild things
who do not tax their lives with forethought of grief.

For a time I rest in the grace of the world,
and am free.

I come into the presence of still water.
And I feel above me the day-blind stars
waiting with their light."""

    results = poem_to_stanzas(poem)
    print("\n── Results ──")
    for r in results:
        print(f"\nStanza {r['index'] + 1}")
        print(f"  Mood:     {r['mood']}")
        print(f"  Keywords: {r['keywords']}")
        print(f"  Image:    {r['image_path']}")