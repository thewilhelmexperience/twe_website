#!/usr/bin/env python3
"""Generate Wilhelm parrot concept art using OpenRouter API"""
import requests
import os
import base64
from pathlib import Path

# Setup
api_key = os.getenv("OPENAI_API_KEY")  # OpenRouter uses same key format
output_dir = Path("/home/captain_tommy/.openclaw/workspace/twe_website/experiments/concept-art")
output_dir.mkdir(parents=True, exist_ok=True)

# Wilhelm character description for consistency
base_description = """A charismatic parrot character named Wilhelm with:
- White and cream colored feathers as the base
- Coral orange-red (#e94560) feather accents on wings, tail, and crest
- Large expressive eyes with personality (slightly raised eyebrow, knowing look)
- Smart, slightly sarcastic expression
- Clean white background for easy extraction
- High quality digital art suitable for avatar use
"""

# 4 style variations
variations = [
    {
        "name": "professional-assistant",
        "prompt": f"""{base_description}
Style: Professional Assistant
- Wearing a small navy captain's hat or communication headset
- Perched on a computer keyboard or standing near a monitor/screen
- Helpful posture but with a knowing smirk
- Professional yet approachable vibe
- Digital art style, clean lines, corporate mascot quality"""
    },
    {
        "name": "tech-savvy", 
        "prompt": f"""{base_description}
Style: Tech-Savvy Cyberpunk-Lite
- Modern, sleek appearance with subtle digital elements
- Slightly glowing coral eyes or subtle holographic interface nearby
- Futuristic but not overwhelming - cyberpunk-lite aesthetic
- Clean geometric background accents suggesting technology
- Digital art style, modern and polished"""
    },
    {
        "name": "classic-wise",
        "prompt": f"""{base_description}
Style: Classic Wise Parrot
- Distinguished appearance with small reading glasses perched on beak
- Perched on a stack of old books or sitting near a coffee cup
- Intellectual, scholarly vibe - like a wise librarian
- Warm, cozy lighting
- Digital art style with classic illustration qualities"""
    },
    {
        "name": "friendly-mascot",
        "prompt": f"""{base_description}
Style: Friendly Mascot
- Cute but not overly childish - approachable and warm
- Waving with one wing or making a welcoming gesture
- Warm color palette with emphasis on coral #e94560 accents
- Cheerful, welcoming expression
- Perfect for a digital assistant avatar
- Digital art style, mascot character design"""
    }
]

def generate_image_openrouter(variation):
    """Generate image using OpenRouter API with image generation model"""
    print(f"Generating: {variation['name']}...")
    
    try:
        # Try using a free image generation model on OpenRouter
        # Using gemini-2.0-flash-exp which supports image generation
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://openclaw.local",
                "X-Title": "Wilhelm Concept Art Generator"
            },
            json={
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Generate an image: {variation['prompt']}"
                    }
                ],
                "modalities": ["image", "text"],
                "stream": False
            },
            timeout=120
        )
        
        data = response.json()
        print(f"Response: {data.keys() if isinstance(data, dict) else data}")
        
        if response.status_code != 200:
            print(f"API Error: {data}")
            return False
            
        # Check for generated images in the response
        if "choices" in data and len(data["choices"]) > 0:
            message = data["choices"][0].get("message", {})
            
            # Try to get image from various possible locations
            if "images" in message:
                images = message["images"]
                if images and len(images) > 0:
                    image_data = images[0].get("imageUrl", {}).get("url", "")
                    if image_data.startswith("data:image"):
                        # Extract base64 data
                        base64_data = image_data.split(",")[1]
                        image_bytes = base64.b64decode(base64_data)
                    else:
                        # Download from URL
                        img_response = requests.get(image_data, timeout=60)
                        image_bytes = img_response.content
                    
                    output_path = output_dir / f"wilhelm-{variation['name']}.png"
                    with open(output_path, "wb") as f:
                        f.write(image_bytes)
                    print(f"✓ Saved: {output_path}")
                    return True
            
            # Check for content that might contain image data
            content = message.get("content", "")
            if "data:image" in content:
                # Extract base64 image from content
                import re
                match = re.search(r'data:image/[^;]+;base64,([^"\']+)', content)
                if match:
                    base64_data = match.group(1)
                    image_bytes = base64.b64decode(base64_data)
                    output_path = output_dir / f"wilhelm-{variation['name']}.png"
                    with open(output_path, "wb") as f:
                        f.write(image_bytes)
                    print(f"✓ Saved: {output_path}")
                    return True
        
        print(f"No image found in response: {data}")
        return False
        
    except Exception as e:
        print(f"✗ Error generating {variation['name']}: {e}")
        import traceback
        traceback.print_exc()
        return False

# Generate all variations
print("="*60)
print("Generating Wilhelm Concept Art - 4 Variations via OpenRouter")
print("="*60)

results = []
for var in variations:
    success = generate_image_openrouter(var)
    results.append((var["name"], success))

# Summary
print("\n" + "="*60)
print("GENERATION COMPLETE")
print("="*60)
for name, success in results:
    status = "✓" if success else "✗"
    print(f"{status} {name}")

print(f"\nAll images saved to: {output_dir}")
