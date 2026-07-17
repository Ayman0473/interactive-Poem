import requests
import urllib.parse

def generate_image(keywords, mood, output_path="output.png"):
    prompt = f"{', '.join(keywords)}, {mood} mood, digital painting, atmospheric, detailed, cinematic lighting"
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"
    
    print(f"Generating image...")
    print(f"Prompt: {prompt}")
    
    response = requests.get(url, timeout=60)
    
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Image saved to {output_path}")
    return output_path

if __name__ == "__main__":
    keywords = ['wood drake on water', 'soft lily pad', 'peaceful forest floor', 'wildflowers swaying', 'dew-kissed morning leaf']
    mood = "tranquil"
    generate_image(keywords, mood, "test_output.png")