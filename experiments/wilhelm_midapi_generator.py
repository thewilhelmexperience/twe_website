#!/usr/bin/env python3
"""
Wilhelm Concept Art Generator - MidAPI.ai Edition
Generates 4 style variations of Wilhelm the parrot assistant
"""

import os
import json
import time
from pathlib import Path
from typing import Optional
import requests

# Default settings
DEFAULT_VERSION = "7"
DEFAULT_ASPECT_RATIO = "1:1"
DEFAULT_SPEED = "fast"  # relaxed, fast, turbo


class WilhelmGenerator:
    def __init__(self, api_key: Optional[str] = None, output_dir: str = None):
        """Initialize MidAPI.ai generator for Wilhelm concept art."""
        self.api_key = api_key or os.getenv("MIDAPI_KEY")
        self.base_url = "https://api.midapi.ai/api/v1/mj"
        
        if output_dir is None:
            self.output_dir = Path("/home/captain_tommy/.openclaw/workspace/twe_website/experiments/concept-art")
        else:
            self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.api_key:
            raise ValueError("MidAPI key required. Set MIDAPI_KEY env var or pass api_key parameter.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Wilhelm character base description for consistency
        self.base_description = """A charismatic parrot character named Wilhelm with white and cream colored feathers as the base, coral orange-red (#e94560) feather accents on wings tail and crest, large expressive eyes with personality slightly raised eyebrow knowing look, smart slightly sarcastic expression, clean white background, high quality digital art suitable for avatar use"""
    
    def get_variations(self):
        """Return the 4 style variations."""
        return [
            {
                "name": "professional-assistant",
                "prompt": f"{self.base_description}, professional assistant style, wearing a small navy captain hat or communication headset, perched on a computer keyboard or standing near a monitor screen, helpful posture but with a knowing smirk, professional yet approachable vibe, digital art style clean lines corporate mascot quality --ar 1:1 --v 6 --style raw"
            },
            {
                "name": "tech-savvy", 
                "prompt": f"{self.base_description}, tech-savvy cyberpunk-lite style, modern sleek appearance with subtle digital elements, slightly glowing coral eyes or subtle holographic interface nearby, futuristic but not overwhelming cyberpunk-lite aesthetic, clean geometric background accents suggesting technology, digital art style modern and polished --ar 1:1 --v 6 --style raw"
            },
            {
                "name": "classic-wise",
                "prompt": f"{self.base_description}, classic wise parrot style, distinguished appearance with small reading glasses perched on beak, perched on a stack of old books or sitting near a coffee cup, intellectual scholarly vibe like a wise librarian, warm cozy lighting, digital art style with classic illustration qualities --ar 1:1 --v 6 --style raw"
            },
            {
                "name": "friendly-mascot",
                "prompt": f"{self.base_description}, friendly mascot style, cute but not overly childish approachable and warm, waving with one wing or making a welcoming gesture, warm color palette with emphasis on coral #e94560 accents, cheerful welcoming expression, perfect for a digital assistant avatar, digital art style mascot character design --ar 1:1 --v 6 --style raw"
            }
        ]
    
    def generate_image(self, variation: dict, 
                       version: str = DEFAULT_VERSION,
                       speed: str = DEFAULT_SPEED,
                       max_retries: int = 3) -> Optional[str]:
        """Generate a single image using MidAPI.ai."""
        
        print(f"\n🎨 Generating: {variation['name']}")
        print(f"   Prompt: {variation['prompt'][:100]}...")
        
        payload = {
            "taskType": "mj_txt2img",
            "prompt": variation['prompt'],
            "speed": speed,
            "aspectRatio": DEFAULT_ASPECT_RATIO,
            "version": version
        }
        
        for attempt in range(max_retries):
            try:
                print(f"   Submitting task... (attempt {attempt + 1}/{max_retries})")
                
                # Submit generation task
                response = requests.post(
                    f"{self.base_url}/generate",
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )
                
                result = response.json()
                
                if result.get("code") != 200:
                    print(f"   API Error: {result.get('msg', 'Unknown error')}")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                        continue
                    return None
                
                task_id = result["data"]["taskId"]
                print(f"   Task started: {task_id}")
                
                # Wait for completion
                image_url = self._wait_for_completion(task_id)
                return image_url
                    
            except Exception as e:
                print(f"   Error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    return None
        
        return None
    
    def _wait_for_completion(self, task_id: str, max_wait: int = 300) -> Optional[str]:
        """Poll for task completion."""
        start_time = time.time()
        poll_interval = 10
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(
                    f"{self.base_url}/record-info?taskId={task_id}",
                    headers=self.headers,
                    timeout=30
                )
                
                result = response.json()
                
                if result.get("code") != 200:
                    print(f"   Status check error: {result.get('msg')}")
                    time.sleep(poll_interval)
                    continue
                
                data = result["data"]
                success_flag = data.get("successFlag", 0)
                
                if success_flag == 0:
                    print(f"   Generating... ({int(time.time() - start_time)}s)")
                elif success_flag == 1:
                    result_info = data.get("resultInfoJson", {})
                    urls = result_info.get("resultUrls", [])
                    if urls:
                        return urls[0].get("resultUrl")
                    return None
                elif success_flag in [2, 3]:
                    error_msg = data.get("errorMessage", "Generation failed")
                    print(f"   Generation failed: {error_msg}")
                    return None
                
                time.sleep(poll_interval)
                
            except Exception as e:
                print(f"   Poll error: {e}")
                time.sleep(poll_interval)
        
        print("   Timeout waiting for generation")
        return None
    
    def download_image(self, url: str, filepath: Path) -> bool:
        """Download image from URL to local file."""
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"   Download error: {e}")
            return False
    
    def generate_all(self, version: str = DEFAULT_VERSION,
                    speed: str = DEFAULT_SPEED,
                    skip_existing: bool = True) -> dict:
        """Generate all 4 Wilhelm concept art variations."""
        
        print("="*60)
        print("🦜 WILHELM CONCEPT ART GENERATOR")
        print("="*60)
        print(f"\nUsing MidAPI.ai with Midjourney v{version}")
        print(f"Output directory: {self.output_dir}")
        
        variations = self.get_variations()
        results = {
            "generated": [],
            "failed": [],
            "skipped": []
        }
        
        for var in variations:
            output_file = self.output_dir / f"wilhelm-{var['name']}.png"
            
            # Check if already exists
            if skip_existing and output_file.exists():
                print(f"\n⏭️  {var['name']}: Already exists, skipping")
                results["skipped"].append({
                    "name": var['name'],
                    "file": str(output_file)
                })
                continue
            
            # Generate image
            image_url = self.generate_image(var, version, speed)
            
            if image_url:
                # Download and save
                if self.download_image(image_url, output_file):
                    print(f"   ✅ Saved: {output_file.name}")
                    results["generated"].append({
                        "name": var['name'],
                        "file": str(output_file),
                        "url": image_url
                    })
                else:
                    print(f"   ⚠️  Generated but failed to download")
                    results["failed"].append({
                        "name": var['name'],
                        "error": "Download failed"
                    })
            else:
                print(f"   ❌ Failed to generate")
                results["failed"].append({
                    "name": var['name'],
                    "error": "Generation failed"
                })
        
        # Print summary
        print("\n" + "="*60)
        print("📊 GENERATION SUMMARY")
        print("="*60)
        print(f"   ✅ Generated: {len(results['generated'])}")
        print(f"   ⏭️  Skipped: {len(results['skipped'])}")
        print(f"   ❌ Failed: {len(results['failed'])}")
        
        if results['generated']:
            print(f"\n📁 Output files:")
            for item in results['generated']:
                print(f"      • {Path(item['file']).name}")
        
        return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Wilhelm concept art with MidAPI.ai")
    parser.add_argument("--output", default=None, help="Output directory")
    parser.add_argument("--version", default="7", help="Midjourney model version (6, 6.1, 7)")
    parser.add_argument("--speed", default="fast", choices=["relaxed", "fast", "turbo"],
                       help="Generation speed")
    parser.add_argument("--regenerate", action="store_true", help="Force regenerate existing images")
    parser.add_argument("--api-key", default=None, help="MidAPI key (or set MIDAPI_KEY env var)")
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = args.api_key or os.getenv("MIDAPI_KEY")
    if not api_key:
        print("❌ Error: MIDAPI_KEY required")
        print("   Get your key at: https://midapi.ai")
        print("   Then either:")
        print("      export MIDAPI_KEY='your-key-here'")
        print("   Or pass it as an argument:")
        print("      python wilhelm_midapi_generator.py --api-key 'your-key'")
        return
    
    # Initialize generator
    try:
        generator = WilhelmGenerator(
            api_key=api_key,
            output_dir=args.output
        )
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    # Generate all variations
    results = generator.generate_all(
        version=args.version,
        speed=args.speed,
        skip_existing=not args.regenerate
    )
    
    print("\n✨ Done!")


if __name__ == "__main__":
    main()
