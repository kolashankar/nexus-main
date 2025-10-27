#!/usr/bin/env python3
"""
Create more cyberpunk textures - Batch 3
"""
from PIL import Image, ImageDraw, ImageFilter
import os
import random

PUBLIC_DIR = "/app/frontend/public"

def create_metal_texture(filepath, base_color, metallic_type, size=(512, 512)):
    """Create a metallic texture with different finishes"""
    img = Image.new('RGB', size, color=base_color)
    draw = ImageDraw.Draw(img)
    
    if metallic_type == 'chrome':
        # Highly reflective with streaks
        for _ in range(50):
            y = random.randint(0, size[1])
            brightness = random.randint(150, 255)
            for x in range(size[0]):
                if random.random() > 0.7:
                    color = (brightness, brightness, brightness)
                    draw.point((x, y), fill=color)
    elif metallic_type == 'steel':
        # Brushed steel effect
        for x in range(0, size[0], 2):
            for y in range(size[1]):
                variation = random.randint(-30, 30)
                color = tuple(max(0, min(255, c + variation)) for c in base_color)
                draw.point((x, y), fill=color)
    else:  # gold
        # Gold with shine
        for _ in range(100):
            x = random.randint(0, size[0])
            y = random.randint(0, size[1])
            r = random.randint(5, 20)
            brightness = random.randint(30, 80)
            color = tuple(min(255, c + brightness) for c in base_color)
            draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
    
    img = img.filter(ImageFilter.SMOOTH)
    img.save(filepath, 'PNG')

def create_robot_light_texture(filepath, light_color, size=(256, 256)):
    """Create glowing robot light texture"""
    img = Image.new('RGBA', size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = (size[0]//2, size[1]//2)
    
    # Create glowing LED effect
    for r in range(size[0]//2, 0, -3):
        alpha = int(255 * (1 - r/(size[0]//2)) * 0.8)
        color = (*light_color, alpha)
        draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], fill=color)
    
    # Add bright center
    center_r = size[0]//8
    draw.ellipse([center[0]-center_r, center[1]-center_r, center[0]+center_r, center[1]+center_r], 
                 fill=(*light_color, 255))
    
    img = img.filter(ImageFilter.GaussianBlur(radius=5))
    img.save(filepath, 'PNG')

def create_particle_effect(filepath, particle_color, size=(128, 128)):
    """Create particle effect texture"""
    img = Image.new('RGBA', size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = (size[0]//2, size[1]//2)
    
    # Outer glow
    for r in range(size[0]//2, 0, -2):
        alpha = int(120 * (1 - r/(size[0]//2)))
        color = (*particle_color, alpha)
        draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], fill=color)
    
    img = img.filter(ImageFilter.GaussianBlur(radius=4))
    img.save(filepath, 'PNG')

def create_prop_texture(filepath, prop_type, size=(512, 512)):
    """Create environment prop textures"""
    if prop_type == 'crate':
        base_color = (120, 90, 60)
    else:  # barrel
        base_color = (100, 100, 110)
    
    img = Image.new('RGB', size, color=base_color)
    draw = ImageDraw.Draw(img)
    
    # Add wood grain or metal panels
    for y in range(0, size[1], 20):
        variation = random.randint(-20, 20)
        color = tuple(max(0, min(255, c + variation)) for c in base_color)
        draw.rectangle([0, y, size[0], y+10], fill=color)
    
    # Add wear and tear
    for _ in range(50):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        size_spot = random.randint(5, 15)
        dark = tuple(max(0, c - 40) for c in base_color)
        draw.ellipse([x, y, x+size_spot, y+size_spot], fill=dark)
    
    img = img.filter(ImageFilter.SMOOTH)
    img.save(filepath, 'PNG')

def create_clothing_texture(filepath, clothing_type, size=(512, 512)):
    """Create clothing textures"""
    if clothing_type == 'formal':
        base_color = (30, 30, 50)
    else:  # tactical
        base_color = (50, 60, 50)
    
    img = Image.new('RGB', size, color=base_color)
    draw = ImageDraw.Draw(img)
    
    # Add fabric pattern
    for y in range(0, size[1], 3):
        for x in range(0, size[0], 3):
            if (x + y) % 6 == 0:
                variation = random.randint(-8, 8)
                color = tuple(max(0, min(255, c + variation)) for c in base_color)
                draw.point((x, y), fill=color)
    
    if clothing_type == 'tactical':
        # Add camouflage pattern
        for _ in range(30):
            x = random.randint(0, size[0])
            y = random.randint(0, size[1])
            w = random.randint(20, 60)
            h = random.randint(20, 60)
            dark = tuple(max(0, c - 20) for c in base_color)
            draw.ellipse([x, y, x+w, y+h], fill=dark)
    
    img = img.filter(ImageFilter.SMOOTH)
    img.save(filepath, 'PNG')

print("Creating Batch 3 textures...")

# Robot metal textures
os.makedirs(f"{PUBLIC_DIR}/textures/robots/metal", exist_ok=True)
create_metal_texture(f"{PUBLIC_DIR}/textures/robots/metal/chrome.png", (200, 200, 220), 'chrome')
create_metal_texture(f"{PUBLIC_DIR}/textures/robots/metal/steel.png", (140, 140, 160), 'steel')
create_metal_texture(f"{PUBLIC_DIR}/textures/robots/metal/gold.png", (218, 165, 32), 'gold')
print("✓ Created robot metal textures (chrome, steel, gold)")

# Robot light textures
os.makedirs(f"{PUBLIC_DIR}/textures/robots/lights", exist_ok=True)
create_robot_light_texture(f"{PUBLIC_DIR}/textures/robots/lights/blue.png", (50, 150, 255))
create_robot_light_texture(f"{PUBLIC_DIR}/textures/robots/lights/red.png", (255, 50, 50))
create_robot_light_texture(f"{PUBLIC_DIR}/textures/robots/lights/green.png", (50, 255, 100))
print("✓ Created robot light textures (blue, red, green)")

# Particle effects
os.makedirs(f"{PUBLIC_DIR}/textures/effects/particles", exist_ok=True)
create_particle_effect(f"{PUBLIC_DIR}/textures/effects/particles/spark.png", (255, 230, 100))
create_particle_effect(f"{PUBLIC_DIR}/textures/effects/particles/smoke.png", (150, 150, 150))
create_particle_effect(f"{PUBLIC_DIR}/textures/effects/particles/fire.png", (255, 100, 30))
print("✓ Created particle effect textures (spark, smoke, fire)")

# Environment props
os.makedirs(f"{PUBLIC_DIR}/textures/environment/props", exist_ok=True)
create_prop_texture(f"{PUBLIC_DIR}/textures/environment/props/crate.png", 'crate')
create_prop_texture(f"{PUBLIC_DIR}/textures/environment/props/barrel.png", 'barrel')
print("✓ Created environment prop textures (crate, barrel)")

# Clothing textures
os.makedirs(f"{PUBLIC_DIR}/textures/characters/clothing", exist_ok=True)
create_clothing_texture(f"{PUBLIC_DIR}/textures/characters/clothing/formal.png", 'formal')
create_clothing_texture(f"{PUBLIC_DIR}/textures/characters/clothing/tactical.png", 'tactical')
print("✓ Created clothing textures (formal, tactical)")

print(f"\n✅ Batch 3 Complete: Created 13 high-quality textures")
print(f"Total textures so far: 34/30 ✓ All textures complete!")
