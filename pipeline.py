from embedder import get_mood
from keyword_extractor import extract_keywords
from image_generator import generate_image
import os

def poem_to_visual(poem_text, output_path="output.png"):
    print("\n── Poem to Visual Pipeline ──")
    print(f"Poem: {poem_text[:80]}...")

    # Step 1: detect mood
    mood, score = get_mood(poem_text)
    print(f"\n[1] Mood detected:  {mood}  (confidence: {score})")

    # Step 2: extract visual keywords
    keywords = extract_keywords(poem_text, mood)
    print(f"[2] Keywords:       {keywords}")

    # Step 3: generate image
    print(f"[3] Generating image...")
    result = generate_image(keywords, mood, output_path)

    if result:
        print(f"\n✓ Done. Image saved to {output_path}")
    else:
        print("\n✗ Image generation failed.")

    return {"mood": mood, "confidence": score, "keywords": keywords, "image": result}

if __name__ == "__main__":
    poems = [
        ("berry_tranquil.png", "I go and lie down where the wood drake rests in his beauty on the water. I come into the peace of wild things who do not tax their lives with forethought of grief."),
        ("angelou_defiant.png", "You may write me down in history with your bitter, twisted lies. You may trod me in the very dirt, but still, like dust, I rise. Does my sassiness upset you?"),
        ("hood_nostalgic.png",  "I remember, I remember the house where I was born, the little window where the sun came peeping in at morn. He never came a wink too soon, nor brought too long a day."),
    ]

    for filename, poem in poems:
        poem_to_visual(poem, output_path=filename)
        print()