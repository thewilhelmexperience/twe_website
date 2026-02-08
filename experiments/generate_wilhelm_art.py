#!/usr/bin/env python3
"""Generate Wilhelm parrot concept art using OpenAI DALL-E 3"""
import openai
import os
import requests
from pathlib import Path

# Setup
openai.api_key = os.getenv("OPENAI_API_KEY")
output_dir = Path("/home/captain_tommy/.openclaw/workspace/twe_website/experiments/concept-art")
output_dir.mkdir(parents=True, exist_ok=True)

# Wilhelm character description for consistency
base_description = """A charismatic parrot character named Wilhelm with:
- White and cream colored feathers as the base
- Coral orange-red (#e94560) feather accents on wings, tail, and crest
- Large expressive eyes with personality (slightly raised eyebrow, knowing look)
- Smart, slightly sarcastic expression
- Clean white or transparent background for easy extraction
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

def generate_image(variation):
    """Generate image using DALL-E 3"""
    print(f"Generating: {variation['name']}...")
    
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=variation["prompt"],
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Get the image URL
        image_url = response.data[0].url
        
        # Download the image
        img_response = requests.get(image_url, timeout=60)
        img_response.raise_for_status()
        
        # Save the image
        output_path = output_dir / f"wilhelm-{variation['name']}.png"
        with open(output_path, "wb") as f:
            f.write(img_response.content)
        
        print(f"✓ Saved: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error generating {variation['name']}: {e}")
        return False

# Generate all variations
print("="*60)
print("Generating Wilhelm Concept Art - 4 Variations")
print("="*60)

results = []
for var in variations:
    success = generate_image(var)
    results.append((var["name"], success))

# Summary
print("\n" + "="*60)
print("GENERATION COMPLETE")
print("="*60)
for name, success in results:
    status = "✓" if success else "✗"
    print(f"{status} {name}")

print(f"\nAll images saved to: {output_dir}")
