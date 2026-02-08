#!/usr/bin/env python3
"""
Wilhelm Customizer - Transform the parrot into Wilhelm
Applies brand colors and prepares for customization
"""

import json
import struct
import os
from pathlib import Path

# Wilhelm brand colors
CORAL = [0.914, 0.271, 0.376, 1.0]  # #e94560
CREAM = [0.98, 0.96, 0.92, 1.0]     # Off-white
DARK_NAVY = [0.102, 0.102, 0.18, 1.0]  # #1a1a2e

def customize_wilhelm(input_path, output_path):
    """Customize the parrot GLB with Wilhelm's brand colors."""
    
    with open(input_path, 'rb') as f:
        data = f.read()
    
    # Parse GLB
    header = data[:12]
    magic, version, total_length = struct.unpack('<4sII', header)
    
    # Find JSON chunk
    offset = 12
    json_chunk_data = None
    json_chunk_start = None
    json_chunk_length = None
    bin_chunk_data = None
    
    while offset < total_length:
        chunk_header = data[offset:offset+8]
        chunk_length, chunk_type = struct.unpack('<I4s', chunk_header)
        chunk_data = data[offset+8:offset+8+chunk_length]
        
        if chunk_type == b'JSON':
            json_chunk_data = chunk_data
            json_chunk_start = offset
            json_chunk_length = chunk_length
        elif chunk_type == b'BIN\x00':
            bin_chunk_data = chunk_data
        
        offset += 8 + chunk_length
    
    # Parse and modify JSON
    gltf = json.loads(json_chunk_data.decode('utf-8'))
    
    # Modify materials to Wilhelm colors
    for mat in gltf.get('materials', []):
        mat['name'] = 'Wilhelm'
        if 'pbrMetallicRoughness' in mat:
            # Create a gradient effect - main body coral, accents cream
            mat['pbrMetallicRoughness']['baseColorFactor'] = CORAL
            mat['pbrMetallicRoughness']['metallicFactor'] = 0.1
            mat['pbrMetallicRoughness']['roughnessFactor'] = 0.6
        
        # Add emissive for subtle glow
        mat['emissiveFactor'] = [0.05, 0.02, 0.02]
    
    # Add custom extras for Wilhelm branding
    gltf['extras'] = {
        'wilhelm': {
            'version': '1.0',
            'brandColor': '#e94560',
            'customized': True
        }
    }
    
    # Serialize modified JSON
    new_json = json.dumps(gltf, separators=(',', ':')).encode('utf-8')
    new_json_length = len(new_json)
    
    # Pad to 4-byte alignment
    padding_needed = (4 - (new_json_length % 4)) % 4
    new_json_padded = new_json + b' ' * padding_needed
    new_json_length_padded = len(new_json_padded)
    
    # Rebuild GLB
    new_total_length = 12 + 8 + new_json_length_padded + 8 + len(bin_chunk_data)
    
    new_glb = bytearray()
    new_glb.extend(header[:8])  # magic + version
    new_glb.extend(struct.pack('<I', new_total_length))  # new total length
    
    # JSON chunk
    new_glb.extend(struct.pack('<I', new_json_length_padded))
    new_glb.extend(b'JSON')
    new_glb.extend(new_json_padded)
    
    # BIN chunk
    new_glb.extend(struct.pack('<I', len(bin_chunk_data)))
    new_glb.extend(b'BIN\x00')
    new_glb.extend(bin_chunk_data)
    
    # Write output
    with open(output_path, 'wb') as f:
        f.write(new_glb)
    
    print(f"✅ Wilhelm customized!")
    print(f"   Input: {input_path} ({len(data):,} bytes)")
    print(f"   Output: {output_path} ({len(new_glb):,} bytes)")
    print(f"   Brand color: #e94560 (coral)")

if __name__ == '__main__':
    input_file = '/home/captain_tommy/.openclaw/workspace/twe_website/experiments/models/wilhelm/Parrot.glb'
    output_file = '/home/captain_tommy/.openclaw/workspace/twe_website/experiments/models/wilhelm/Wilhelm-v1.glb'
    
    customize_wilhelm(input_file, output_file)