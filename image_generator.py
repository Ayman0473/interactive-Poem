import requests
import urllib.parse

def get_image_url(keywords, mood):
    """
    Returns a Pollinations URL directly — no file saving needed.
    This works for deployment since we don't rely on local filesystem.
    """
    prompt = f"{', '.join(keywords)}, {mood} mood, digital painting, atmospheric, detailed, cinematic lighting"
    negative = "text, watermark, blurry, low quality, cartoon, anime"
    encoded = urllib.parse.quote(prompt)
    encoded_neg = urllib.parse.quote(negative)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&nologo=true&negative={encoded_neg}"
    return url

def generate_image(keywords, mood, output_path="output.png"):
    """
    Keeps backward compatibility — downloads and saves for local use.
    """
    url = get_image_url(keywords, mood)
    print(f"Generating image...")
    print(f"Prompt URL: {url[:80]}...")
    response = requests.get(url, timeout=60)
    if response.status_code != 200:
        print(f"Error {response.status_code}")
        return None
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Image saved to {output_path}")
    return output_path

if __name__ == "__main__":
    keywords = ['wood drake on water', 'soft lily pad', 'peaceful forest floor', 'wildflowers swaying', 'dew-kissed morning leaf']
    mood = "tranquil"
    print(get_image_url(keywords, mood))