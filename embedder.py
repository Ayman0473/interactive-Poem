from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

MOOD_DESCRIPTIONS = {
    "melancholic": "death, grief, sorrow, loss, mourning, darkness, despair, decay, fading, gone forever, tears, absence, emptiness, withering",
    "joyful": "happiness, celebration, laughter, delight, sunshine, warmth, love, dancing, blooming, radiant, bright, singing, joy",
    "defiant": "resistance, rising, refusing, fighting, strength, unbowed, unconquerable, defiance, power, stand, refuse, rebel, overcome",
    "tranquil": "stillness, peace, quiet, calm, gentle, silence, rest, serene, soft, slow, breathing, accepting, nature, undisturbed",
    "nostalgic": "remember, childhood, past, long ago, used to, once, home, memory, return, lost, years ago, miss, before, gone",
}

def get_mood(poem_text):
    poem_emb = model.encode(poem_text)
    mood_embs = model.encode(list(MOOD_DESCRIPTIONS.values()))
    scores = util.cos_sim(poem_emb, mood_embs)[0].tolist()
    ranked = sorted(zip(MOOD_DESCRIPTIONS.keys(), scores), key=lambda x: x[1], reverse=True)
    return ranked[0][0], round(ranked[0][1], 4)

if __name__ == "__main__":
    tests = [
        "Still I rise, leaving behind nights of terror and fear. Into a daybreak wondrously clear, I rise.",
        "I go and lie down where the wood drake rests in his beauty on the water. I come into the peace of wild things.",
        "I remember, I remember the house where I was born, the little window where the sun came peeping in at morn.",
        "O my Luve is like a red red rose that's newly sprung in June. O my Luve is like the melody that's sweetly played in tune.",
    ]
    expected = ["defiant", "tranquil", "nostalgic", "joyful"]

    for poem, expected_mood in zip(tests, expected):
        mood, score = get_mood(poem)
        result = "✓" if mood == expected_mood else "✗"
        print(f"{result} Expected: {expected_mood:12s} Got: {mood:12s} Score: {score}  ")
        print(f"  '{poem[:60]}...'")
        print()