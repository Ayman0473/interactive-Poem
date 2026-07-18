from sentence_transformers import SentenceTransformer, util

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

MOOD_DESCRIPTIONS = {
    "melancholic": "death, grief, sorrow, loss, mourning, darkness, despair, decay, fading, gone forever, tears, absence, emptiness, withering",
    "joyful": "happiness, celebration, laughter, delight, sunshine, warmth, love, dancing, blooming, radiant, bright, singing, joy",
    "defiant": "resistance, rising, refusing, fighting, strength, unbowed, unconquerable, defiance, power, stand, refuse, rebel, overcome",
    "tranquil": "stillness, peace, quiet, calm, gentle, silence, rest, serene, soft, slow, breathing, accepting, nature, undisturbed",
    "nostalgic": "remember, childhood, past, long ago, used to, once, home, memory, return, lost, years ago, miss, before, gone",
}

def get_mood(poem_text):
    model = get_model()
    poem_emb = model.encode(poem_text)
    mood_embs = model.encode(list(MOOD_DESCRIPTIONS.values()))
    scores = util.cos_sim(poem_emb, mood_embs)[0].tolist()
    ranked = sorted(zip(MOOD_DESCRIPTIONS.keys(), scores), key=lambda x: x[1], reverse=True)
    return ranked[0][0], round(ranked[0][1], 4)