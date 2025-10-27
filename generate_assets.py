#!/usr/bin/env python3
"""
Generate placeholder asset files and assets_links.txt for Karma Nexus 2.0
"""

import os
import json

# Base directory
PUBLIC_DIR = "/app/frontend/public"

# Define all assets needed based on code analysis
ASSETS = {
    # 3D Models (GLB format)
    "models": {
        "characters": [
            "male_base.glb",
            "male_athletic.glb",
            "male_heavy.glb",
            "female_base.glb",
            "female_athletic.glb",
            "female_heavy.glb"
        ],
        "animations": [
            "idle.glb",
            "walk.glb",
            "run.glb",
            "jump.glb",
            "attack.glb",
            "defend.glb",
            "victory.glb",
            "defeat.glb"
        ],
        "animations/emotes": [
            "wave.glb",
            "dance.glb",
            "laugh.glb"
        ],
        "robots": [
            "combat.glb",
            "scout.glb",
            "guardian.glb",
            "assault.glb",
            "tactical.glb",
            "hacker.glb",
            "medic.glb",
            "harvester.glb",
            "trader.glb"
        ],
        "environment/buildings": [
            "warehouse.glb",
            "shop.glb",
            "headquarters.glb",
            "tower.glb"
        ],
        "environment/props": [
            "container.glb",
            "vehicle.glb"
        ],
        "environment/terrain": [
            "platform.glb"
        ],
        "ui": [
            "hologram.glb",
            "interface.glb"
        ],
        "placeholders": [
            "character_placeholder.glb",
            "robot_placeholder.glb",
            "building_placeholder.glb"
        ]
    },
    # Textures (PNG format)
    "textures": {
        "characters/skin": [
            "default.png",
            "light.png",
            "medium.png",
            "dark.png"
        ],
        "characters/hair": [
            "black.png",
            "brown.png",
            "blonde.png",
            "red.png"
        ],
        "characters/clothing": [
            "casual.png",
            "formal.png",
            "tactical.png"
        ],
        "robots/metal": [
            "chrome.png",
            "steel.png",
            "gold.png"
        ],
        "robots/lights": [
            "blue.png",
            "red.png",
            "green.png"
        ],
        "environment/walls": [
            "concrete.png",
            "metal.png",
            "brick.png"
        ],
        "environment/floor": [
            "tiles.png",
            "metal.png",
            "wood.png"
        ],
        "environment/props": [
            "crate.png",
            "barrel.png"
        ],
        "effects/particles": [
            "spark.png",
            "smoke.png",
            "fire.png"
        ],
        "effects/glow": [
            "blue.png",
            "red.png",
            "green.png"
        ]
    },
    # Sounds (MP3 format)
    "sounds": [
        "background_music.mp3",
        "menu_click.mp3",
        "action_success.mp3",
        "action_fail.mp3",
        "level_up.mp3",
        "combat_hit.mp3",
        "combat_miss.mp3",
        "notification.mp3"
    ],
    # Images (PNG/SVG format)
    "images": [
        "logo.png",
        "hero_background.jpg",
        "placeholder_avatar.png"
    ],
    # Icons (SVG format)
    "icons": [
        "karma.svg",
        "health.svg",
        "energy.svg",
        "coins.svg"
    ],
    # Fonts (WOFF2 format)
    "fonts": [
        "game_font_regular.woff2",
        "game_font_bold.woff2"
    ]
}

def create_placeholder_file(filepath, file_type):
    """Create a minimal placeholder file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if file_type == "glb":
        # Minimal GLB file header
        with open(filepath, 'wb') as f:
            # GLB magic number and version
            f.write(b'glTF')
            f.write(b'\x02\x00\x00\x00')
            # File length (20 bytes - just header)
            f.write(b'\x14\x00\x00\x00')
            # JSON chunk length (0)
            f.write(b'\x00\x00\x00\x00')
    
    elif file_type == "png":
        # Minimal 1x1 transparent PNG
        with open(filepath, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
    
    elif file_type == "jpg":
        # Minimal 1x1 JPEG
        with open(filepath, 'wb') as f:
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xfe\xfa(\xa2\x80\x3f\xff\xd9')
    
    elif file_type == "svg":
        # Minimal SVG
        with open(filepath, 'w') as f:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"><rect width="24" height="24" fill="#ccc"/></svg>')
    
    elif file_type == "mp3":
        # Minimal MP3 header (silent)
        with open(filepath, 'wb') as f:
            f.write(b'ID3\x04\x00\x00\x00\x00\x00\x00')
    
    elif file_type == "woff2":
        # Minimal WOFF2 signature
        with open(filepath, 'wb') as f:
            f.write(b'wOF2')
    
    else:
        # Default: empty file
        with open(filepath, 'w') as f:
            f.write('')

def generate_assets():
    """Generate all placeholder assets and create assets_links.txt"""
    
    assets_list = []
    
    # Process models
    for category, files in ASSETS.get("models", {}).items():
        for filename in files:
            filepath = os.path.join(PUBLIC_DIR, "models", category, filename)
            create_placeholder_file(filepath, "glb")
            assets_list.append({
                "file": f"/models/{category}/{filename}",
                "type": "3D Model (GLB)",
                "link": "placeholder created - needs actual 3D model",
                "description": f"3D model for {category}"
            })
            print(f"Created: {filepath}")
    
    # Process textures
    for category, files in ASSETS.get("textures", {}).items():
        for filename in files:
            filepath = os.path.join(PUBLIC_DIR, "textures", category, filename)
            create_placeholder_file(filepath, "png")
            assets_list.append({
                "file": f"/textures/{category}/{filename}",
                "type": "Texture (PNG)",
                "link": "placeholder created - needs actual texture",
                "description": f"Texture for {category}"
            })
            print(f"Created: {filepath}")
    
    # Process sounds
    for filename in ASSETS.get("sounds", []):
        filepath = os.path.join(PUBLIC_DIR, "sounds", filename)
        create_placeholder_file(filepath, "mp3")
        assets_list.append({
            "file": f"/sounds/{filename}",
            "type": "Sound (MP3)",
            "link": "placeholder created - needs actual sound file",
            "description": "Game sound effect or music"
        })
        print(f"Created: {filepath}")
    
    # Process images
    for filename in ASSETS.get("images", []):
        ext = filename.split('.')[-1]
        filepath = os.path.join(PUBLIC_DIR, "images", filename)
        create_placeholder_file(filepath, ext)
        assets_list.append({
            "file": f"/images/{filename}",
            "type": f"Image ({ext.upper()})",
            "link": "placeholder created - needs actual image",
            "description": "Game image asset"
        })
        print(f"Created: {filepath}")
    
    # Process icons
    for filename in ASSETS.get("icons", []):
        filepath = os.path.join(PUBLIC_DIR, "icons", filename)
        create_placeholder_file(filepath, "svg")
        assets_list.append({
            "file": f"/icons/{filename}",
            "type": "Icon (SVG)",
            "link": "placeholder created - needs actual icon",
            "description": "UI icon"
        })
        print(f"Created: {filepath}")
    
    # Process fonts
    for filename in ASSETS.get("fonts", []):
        filepath = os.path.join(PUBLIC_DIR, "fonts", filename)
        create_placeholder_file(filepath, "woff2")
        assets_list.append({
            "file": f"/fonts/{filename}",
            "type": "Font (WOFF2)",
            "link": "placeholder created - needs actual font file",
            "description": "Game font"
        })
        print(f"Created: {filepath}")
    
    # Create assets_links.txt
    assets_file = "/app/frontend/assets_links.txt"
    with open(assets_file, 'w') as f:
        f.write("# KARMA NEXUS 2.0 - ASSET LIST\n")
        f.write("# Generated: Asset placeholder files created\n")
        f.write("#\n")
        f.write("# Format: FILENAME | TYPE | LINK/STATUS | DESCRIPTION\n")
        f.write("#" + "="*80 + "\n\n")
        
        for asset in assets_list:
            f.write(f"{asset['file']:<50} | {asset['type']:<20} | {asset['link']:<50} | {asset['description']}\n")
        
        f.write(f"\n# Total assets: {len(assets_list)}\n")
        f.write("\n# NOTE: All files are placeholders. Replace with actual assets for production use.\n")
    
    print(f"\n✅ Created {len(assets_list)} placeholder asset files")
    print(f"✅ Generated assets_links.txt at {assets_file}")
    
    return len(assets_list)

if __name__ == "__main__":
    total = generate_assets()
    print(f"\n🎉 Asset generation complete! Total: {total} files")
