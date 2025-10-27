#!/usr/bin/env python3
"""
Create SVG icons and logo for Karma Nexus 2.0 - Batch 4
"""
import os

PUBLIC_DIR = "/app/frontend/public"

# Create directories
os.makedirs(f"{PUBLIC_DIR}/icons", exist_ok=True)
os.makedirs(f"{PUBLIC_DIR}/images", exist_ok=True)

# Karma Icon - Yin Yang style with cyberpunk glow
karma_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <radialGradient id="karmaGlow" cx="50%" cy="50%">
      <stop offset="0%" style="stop-color:#00ffff;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#0088ff;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#0044aa;stop-opacity:0.3" />
    </radialGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <circle cx="50" cy="50" r="48" fill="url(#karmaGlow)" filter="url(#glow)"/>
  <path d="M 50 10 A 20 20 0 0 1 50 50 A 20 20 0 0 0 50 90 A 40 40 0 0 0 50 10" fill="#001133" opacity="0.7"/>
  <circle cx="50" cy="30" r="7" fill="#00ffff" filter="url(#glow)"/>
  <circle cx="50" cy="70" r="7" fill="#001133"/>
  <text x="50" y="56" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#00ffff" text-anchor="middle">K</text>
</svg>'''

# Health Icon - Heart with pulse
health_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="healthGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#ff4466;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#cc0022;stop-opacity:1" />
    </linearGradient>
    <filter id="healthGlow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <path d="M 50 85 L 20 55 Q 10 45 10 35 Q 10 20 25 20 Q 35 20 50 35 Q 65 20 75 20 Q 90 20 90 35 Q 90 45 80 55 Z" 
        fill="url(#healthGrad)" stroke="#ff0044" stroke-width="2" filter="url(#healthGlow)"/>
  <polyline points="25,50 35,50 40,40 45,60 50,50 65,50" stroke="#ffffff" stroke-width="3" fill="none" opacity="0.8"/>
</svg>'''

# Energy Icon - Lightning bolt
energy_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="energyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ffff00;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#ffaa00;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ff6600;stop-opacity:1" />
    </linearGradient>
    <filter id="energyGlow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <polygon points="55,10 30,45 45,45 25,90 70,50 55,50 80,10" 
           fill="url(#energyGrad)" stroke="#ffff44" stroke-width="2" filter="url(#energyGlow)"/>
  <polygon points="55,10 30,45 45,45 25,90 70,50 55,50 80,10" 
           fill="none" stroke="#ffffff" stroke-width="1" opacity="0.5"/>
</svg>'''

# Coins Icon - Stack of coins with $ symbol
coins_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <radialGradient id="coinGrad" cx="40%" cy="40%">
      <stop offset="0%" style="stop-color:#ffdd44;stop-opacity:1" />
      <stop offset="70%" style="stop-color:#ffaa00;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#cc8800;stop-opacity:1" />
    </radialGradient>
    <filter id="coinGlow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <ellipse cx="45" cy="70" rx="25" ry="8" fill="#aa7700" opacity="0.6"/>
  <ellipse cx="50" cy="65" rx="28" ry="9" fill="url(#coinGrad)" stroke="#ffaa00" stroke-width="2" filter="url(#coinGlow)"/>
  <ellipse cx="55" cy="50" rx="30" ry="10" fill="url(#coinGrad)" stroke="#ffaa00" stroke-width="2" filter="url(#coinGlow)"/>
  <ellipse cx="60" cy="35" rx="32" ry="11" fill="url(#coinGrad)" stroke="#ffaa00" stroke-width="2" filter="url(#coinGlow)"/>
  <text x="60" y="42" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#ffffff" text-anchor="middle" opacity="0.9">$</text>
</svg>'''

# Logo - Karma Nexus 2.0
logo_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 150" width="400" height="150">
  <defs>
    <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00ffff;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#0088ff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ff00ff;stop-opacity:1" />
    </linearGradient>
    <filter id="logoGlow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background hexagon -->
  <polygon points="75,25 125,25 150,75 125,125 75,125 50,75" 
           fill="none" stroke="url(#logoGrad)" stroke-width="3" filter="url(#logoGlow)"/>
  
  <!-- K letter with circuit pattern -->
  <path d="M 65 50 L 65 100 M 65 75 L 100 50 M 65 75 L 100 100" 
        stroke="url(#logoGrad)" stroke-width="6" stroke-linecap="round" filter="url(#logoGlow)"/>
  
  <!-- Neural network nodes -->
  <circle cx="75" cy="60" r="4" fill="#00ffff" filter="url(#logoGlow)"/>
  <circle cx="90" cy="75" r="4" fill="#0088ff" filter="url(#logoGlow)"/>
  <circle cx="75" cy="90" r="4" fill="#ff00ff" filter="url(#logoGlow)"/>
  
  <!-- Text: KARMA NEXUS -->
  <text x="165" y="70" font-family="'Orbitron', 'Arial Black', sans-serif" font-size="36" font-weight="bold" 
        fill="url(#logoGrad)" filter="url(#logoGlow)">KARMA</text>
  <text x="165" y="105" font-family="'Orbitron', 'Arial', sans-serif" font-size="36" font-weight="bold" 
        fill="url(#logoGrad)" filter="url(#logoGlow)">NEXUS</text>
  
  <!-- Version 2.0 -->
  <text x="165" y="130" font-family="Arial, sans-serif" font-size="16" font-weight="normal" 
        fill="#00ffff" opacity="0.8">v2.0</text>
  
  <!-- Decorative circuit lines -->
  <line x1="155" y1="75" x2="165" y2="75" stroke="#00ffff" stroke-width="2" opacity="0.5"/>
  <line x1="340" y1="75" x2="350" y2="75" stroke="#ff00ff" stroke-width="2" opacity="0.5"/>
</svg>'''

# Write all SVG files
with open(f"{PUBLIC_DIR}/icons/karma.svg", 'w') as f:
    f.write(karma_svg)
print("✓ Created karma.svg icon")

with open(f"{PUBLIC_DIR}/icons/health.svg", 'w') as f:
    f.write(health_svg)
print("✓ Created health.svg icon")

with open(f"{PUBLIC_DIR}/icons/energy.svg", 'w') as f:
    f.write(energy_svg)
print("✓ Created energy.svg icon")

with open(f"{PUBLIC_DIR}/icons/coins.svg", 'w') as f:
    f.write(coins_svg)
print("✓ Created coins.svg icon")

with open(f"{PUBLIC_DIR}/images/logo.svg", 'w') as f:
    f.write(logo_svg)
print("✓ Created logo.svg")

# Convert logo SVG to PNG using a placeholder approach
print("\n✅ Batch 4 Complete: Created 5 SVG assets (4 icons + 1 logo)")
print("Total progress: Textures (30/30) ✓ | Icons (4/4) ✓ | Images (2/3)")
