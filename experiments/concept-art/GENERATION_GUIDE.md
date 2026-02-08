# Wilhelm Concept Art - Generation Package

## Overview
This package contains everything needed to generate Wilhelm the parrot assistant concept art.

## Character Reference

### Wilhelm - The Sarcastic Parrot Assistant
- **Base colors**: White and cream feathers
- **Accent color**: Coral/orange-red (#e94560) on wings, tail, and crest
- **Expression**: Smart, slightly sarcastic, knowing smirk
- **Eyes**: Large, expressive, slightly raised eyebrow
- **Style**: High-quality digital art, clean backgrounds for easy extraction

## Generation Prompts

### 1. Professional Assistant
```
A charismatic parrot character named Wilhelm with white and cream colored feathers as the base, coral orange-red (#e94560) feather accents on wings tail and crest, large expressive eyes with personality slightly raised eyebrow knowing look, smart slightly sarcastic expression, wearing a small navy captain's hat or communication headset, perched on a computer keyboard or standing near a monitor screen, helpful posture but with a knowing smirk, professional yet approachable vibe, clean white background for easy extraction, high quality digital art style clean lines corporate mascot quality, suitable for avatar use --ar 1:1 --v 6
```

### 2. Tech-Savvy Parrot
```
A charismatic parrot character named Wilhelm with white and cream colored feathers as the base, coral orange-red (#e94560) feather accents on wings tail and crest, large expressive eyes with personality slightly raised eyebrow knowing look, smart slightly sarcastic expression, tech-savvy cyberpunk-lite style, modern sleek appearance with subtle digital elements, slightly glowing coral eyes or subtle holographic interface nearby, futuristic but not overwhelming cyberpunk-lite aesthetic, clean geometric background accents suggesting technology, clean white background for easy extraction, high quality digital art style modern and polished, suitable for avatar use --ar 1:1 --v 6
```

### 3. Classic Wise Parrot
```
A charismatic parrot character named Wilhelm with white and cream colored feathers as the base, coral orange-red (#e94560) feather accents on wings tail and crest, large expressive eyes with personality slightly raised eyebrow knowing look, smart slightly sarcastic expression, classic wise parrot style, distinguished appearance with small reading glasses perched on beak, perched on a stack of old books or sitting near a coffee cup, intellectual scholarly vibe like a wise librarian, warm cozy lighting, clean white background for easy extraction, high quality digital art style with classic illustration qualities, suitable for avatar use --ar 1:1 --v 6
```

### 4. Friendly Mascot
```
A charismatic parrot character named Wilhelm with white and cream colored feathers as the base, coral orange-red (#e94560) feather accents on wings tail and crest, large expressive eyes with personality slightly raised eyebrow knowing look, smart slightly sarcastic expression, friendly mascot style, cute but not overly childish approachable and warm, waving with one wing or making a welcoming gesture, warm color palette with emphasis on coral #e94560 accents, cheerful welcoming expression, perfect for a digital assistant avatar, clean white background for easy extraction, high quality digital art style mascot character design, suitable for avatar use --ar 1:1 --v 6
```

## Generation Instructions

### Using MidAPI (Midjourney API)
1. Sign up at https://midapi.ai
2. Get your API key
3. Use the prompts above with the MidAPI endpoint
4. Character reference for consistency: Use the same seed or reference image across all 4 variations

### Using Midjourney Directly
1. Copy each prompt
2. Paste into Discord with /imagine command
3. Use character reference (--cref) with the first generated image for consistency

### Using DALL-E 3 (OpenAI)
1. Use the prompts above (remove --ar and --v parameters)
2. Add style: "digital art, high quality, avatar suitable"

### Using Stable Diffusion/FLUX
1. Use the prompts as-is
2. Recommended settings: 1024x1024, CFG 7-8, 30-50 steps

## Output Files

Expected output files in `/home/captain_tommy/.openclaw/workspace/twe_website/experiments/concept-art/`:
- `wilhelm-professional-assistant.png`
- `wilhelm-tech-savvy.png`
- `wilhelm-classic-wise.png`
- `wilhelm-friendly-mascot.png`

## Notes
- All images should have clean backgrounds for easy extraction
- Maintain consistent character appearance across all 4 variations
- The coral accent color (#e94560) is critical for brand consistency
- Expressive eyes are key to the character's personality
