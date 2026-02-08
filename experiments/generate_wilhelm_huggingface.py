#!/usr/bin/env python3
"""Generate Wilhelm parrot concept art using HuggingFace Inference API (free tier)"""
import urllib.request
import urllib.parse
import json
import os
from pathlib import Path

# Setup
output_dir = Path("/home/captain_tommy/.openclaw/workspace/twe_website/experiments/concept-art")
output_dir.mkdir(parents=True, exist_ok=True)

# Wilhelm character description for consistency
base_description = """A charismatic parrot character named Wilhelm with white and cream colored feathers as the base, coral orange-red feather accents on wings tail and crest, large expressive eyes with personality slightly raised eyebrow knowing look, smart slightly sarcastic expression, clean white background, high quality digital art suitable for avatar use"""

# 4 style variations
variations = [
    {
        "name": "professional-assistant",
        "prompt": f"{base_description}, professional assistant style, wearing a small navy captain hat or communication headset, perched on a computer keyboard or standing near a monitor screen, helpful posture but with a knowing smirk, professional yet approachable vibe, digital art style clean lines corporate mascot quality"
    },
    {
        "name": "tech-savvy", 
        "prompt": f"{base_description}, tech-savvy cyberpunk-lite style, modern sleek appearance with subtle digital elements, slightly glowing coral eyes or subtle holographic interface nearby, futuristic but not overwhelming cyberpunk-lite aesthetic, clean geometric background accents suggesting technology, digital art style modern and polished"
    },
    {
        "name": "classic-wise",
        "prompt": f"{base_description}, classic wise parrot style, distinguished appearance with small reading glasses perched on beak, perched on a stack of old books or sitting near a coffee cup, intellectual scholarly vibe like a wise librarian, warm cozy lighting, digital art style with classic illustration qualities"
    },
    {
        "name": "friendly-mascot",
        "prompt": f"{base_description}, friendly mascot style, cute but not overly childish approachable and warm, waving with one wing or making a welcoming gesture, warm color palette with emphasis on coral accents, cheerful welcoming expression, perfect for a digital assistant avatar, digital art style mascot character design"
    }
]

# Try multiple models in case some are unavailable
models = [
    "black-forest-labs/FLUX.1-schnell",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "runwayml/stable-diffusion-v1-5"
]

def generate_image_huggingface(variation, model):
    """Generate image using HuggingFace Inference API"""
    print(f"Generating: {variation['name']} using {model}...")
    
    try:
        # HuggingFace Inference API endpoint
        api_url = f"https://api-inference.huggingface.co/models/{model}"
        
        # Prepare the payload
        payload = json.dumps({"inputs": variation['prompt']}).encode('utf-8')
        
        # Create request
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(api_url, data=payload, headers=headers, method='POST')
        
        # Make request with longer timeout for model loading
        with urllib.request.urlopen(req, timeout=180) as response:
            # HuggingFace returns the image bytes directly
            image_data = response.read()
            
            # Save the image
            output_path = output_dir / f"wilhelm-{variation['name']}.png"
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            # Check if file was saved and has content
            if output_path.exists() and output_path.stat().st_size > 1000:
                print(f"✓ Saved: {output_path} ({output_path.stat().st_size} bytes)")
                return True
            else:
                print(f"✗ File too small or not saved properly")
                return False
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"✗ HTTP Error {e.code}: {error_body[:200]}")
        return False
    except Exception as e:
        print(f"✗ Error generating {variation['name']}: {e}")
        import traceback
        traceback.print_exc()
        return False

# Generate all variations
print("="*60)
print("Generating Wilhelm Concept Art - 4 Variations via HuggingFace")
print("="*60)

results = []
for var in variations:
    # Try each model until one works
    success = False
    for model in models:
        success = generate_image_huggingface(var, model)
        if success:
            break
        print(f"  Retrying with different model...")
    results.append((var["name"], success))

# Summary
print("\n" + "="*60)
print("GENERATION COMPLETE")
print("="*60)
for name, success in results:
    status = "✓" if success else "✗"
    print(f"{status} {name}")

print(f"\nAll images saved to: {output_dir}")

# List generated files
print("\nGenerated files:")
for f in sorted(output_dir.glob("*.png")):
    print(f"  - {f.name} ({f.stat().st_size} bytes)")
