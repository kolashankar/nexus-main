#!/usr/bin/env python3
"""
Create high-quality cyberpunk textures for Karma Nexus 2.0 - Batch 2
"""
from PIL import Image, ImageDraw, ImageFilter
import os
import random

PUBLIC_DIR = "/app/frontend/public"

def create_neon_glow_texture(filepath, color_rgb, size=(512, 512)):
    """Create a neon glow effect texture"""
    img = Image.new('RGB', size, color=(10, 10, 20))
    draw = ImageDraw.Draw(img)
    
    # Create multiple glowing circles
    for _ in range(20):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        r = random.randint(20, 80)
        
        # Draw glow effect with alpha blending
        for i in range(r, 0, -5):
            alpha = int(255 * (i / r) * 0.3)
            color = (*color_rgb, alpha)
            draw.ellipse([x-i, y-i, x+i, y+i], fill=color_rgb)
    
    img = img.filter(ImageFilter.GaussianBlur(radius=15))
    img.save(filepath, 'PNG')

def create_metal_texture(filepath, base_color, size=(512, 512)):
    """Create a metallic texture"""
    img = Image.new('RGB', size, color=base_color)
    draw = ImageDraw.Draw(img)
    
    # Add scratches and details
    for _ in range(100):
        x1 = random.randint(0, size[0])
        y1 = random.randint(0, size[1])
        x2 = x1 + random.randint(-50, 50)
        y2 = y1 + random.randint(-50, 50)
        brightness = random.randint(0, 50)
        color = tuple(min(255, c + brightness) for c in base_color)
        draw.line([x1, y1, x2, y2], fill=color, width=1)
    
    img = img.filter(ImageFilter.SMOOTH)
    img.save(filepath, 'PNG')

def create_skin_texture(filepath, base_tone, size=(512, 512)):
    """Create a skin texture"""
    img = Image.new('RGB', size, color=base_tone)
    draw = ImageDraw.Draw(img)
    
    # Add subtle variation
    for _ in range(500):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        variation = random.randint(-10, 10)
        color = tuple(max(0, min(255, c + variation)) for c in base_tone)
        draw.point((x, y), fill=color)
    
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    img.save(filepath, 'PNG')

def create_particle_texture(filepath, particle_color, size=(128, 128)):
    """Create a particle effect texture"""
    img = Image.new('RGBA', size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create a glowing particle
    center = (size[0]//2, size[1]//2)
    max_radius = size[0]//2
    
    for r in range(max_radius, 0, -2):
        alpha = int(255 * (1 - r/max_radius))
        color = (*particle_color, alpha)
        draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], fill=color)
    
    img = img.filter(ImageFilter.GaussianBlur(radius=3))
    img.save(filepath, 'PNG')

def create_hair_texture(filepath, hair_color, size=(512, 512)):
    """Create a hair texture"""
    img = Image.new('RGB', size, color=hair_color)
    draw = ImageDraw.Draw(img)
    
    # Draw hair strands
    for _ in range(200):
        x = random.randint(0, size[0])
        y1 = random.randint(0, size[1])
        y2 = y1 + random.randint(30, 100)
        
        # Slight color variation
        variation = random.randint(-20, 20)
        color = tuple(max(0, min(255, c + variation)) for c in hair_color)
        draw.line([x, y1, x + random.randint(-5, 5), y2], fill=color, width=2)
    
    img = img.filter(ImageFilter.SMOOTH)
    img.save(filepath, 'PNG')

def create_clothing_texture(filepath, pattern_type, size=(512, 512)):
    """Create a clothing texture"""
    if pattern_type == 'casual':
        base_color = (100, 100, 150)
    elif pattern_type == 'formal':
        base_color = (40, 40, 60)
    else:  # tactical
        base_color = (60, 80, 70)
    
    img = Image.new('RGB', size, color=base_color)
    draw = ImageDraw.Draw(img)
    
    # Add fabric texture pattern
    for y in range(0, size[1], 4):
        for x in range(0, size[0], 4):
            if (x + y) % 8 == 0:
                variation = random.randint(-5, 5)
                color = tuple(max(0, min(255, c + variation)) for c in base_color)
                draw.point((x, y), fill=color)
    
    img = img.filter(ImageFilter.SMOOTH)
    img.save(filepath, 'PNG')

# Create Batch 2 textures
print("Creating Batch 2 textures...")

# Neon glow effects (red and green)
os.makedirs(f"{PUBLIC_DIR}/textures/effects/glow", exist_ok=True)
create_neon_glow_texture(f"{PUBLIC_DIR}/textures/effects/glow/red.png", (255, 50, 50))
create_neon_glow_texture(f"{PUBLIC_DIR}/textures/effects/glow/green.png", (50, 255, 50))
print("✓ Created glow textures (red, green)")

# Skin textures
os.makedirs(f"{PUBLIC_DIR}/textures/characters/skin", exist_ok=True)
create_skin_texture(f"{PUBLIC_DIR}/textures/characters/skin/default.png", (230, 195, 170))
create_skin_texture(f"{PUBLIC_DIR}/textures/characters/skin/light.png", (255, 220, 200))
create_skin_texture(f"{PUBLIC_DIR}/textures/characters/skin/medium.png", (200, 160, 130))
create_skin_texture(f"{PUBLIC_DIR}/textures/characters/skin/dark.png", (140, 100, 70))
print("✓ Created skin textures (default, light, medium, dark)")

# Hair textures
os.makedirs(f"{PUBLIC_DIR}/textures/characters/hair", exist_ok=True)
create_hair_texture(f"{PUBLIC_DIR}/textures/characters/hair/black.png", (20, 20, 20))
create_hair_texture(f"{PUBLIC_DIR}/textures/characters/hair/brown.png", (100, 60, 40))
create_hair_texture(f"{PUBLIC_DIR}/textures/characters/hair/blonde.png", (230, 200, 130))
create_hair_texture(f"{PUBLIC_DIR}/textures/characters/hair/red.png", (180, 60, 40))
print("✓ Created hair textures (black, brown, blonde, red)")

# Clothing textures
os.makedirs(f"{PUBLIC_DIR}/textures/characters/clothing", exist_ok=True)
create_clothing_texture(f"{PUBLIC_DIR}/textures/characters/clothing/casual.png", 'casual')
print("✓ Created clothing texture (casual)")

print(f"\n✅ Batch 2 Complete: Created 11 high-quality textures")
