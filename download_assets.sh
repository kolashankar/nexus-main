#!/bin/bash

###############################################################################
# Karma Nexus Asset Download Helper
# This script helps you download free, high-quality assets
###############################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUBLIC_DIR="$SCRIPT_DIR/frontend/public"
TEMP_DIR="/tmp/nexus-assets-download"

echo "=========================================="
echo "Karma Nexus Asset Download Helper"
echo "=========================================="
echo ""

# Create temp directory
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

echo "📁 Temp directory: $TEMP_DIR"
echo "📁 Public directory: $PUBLIC_DIR"
echo ""

###############################################################################
# FONTS - Google Fonts (Orbitron)
###############################################################################

echo "=========================================="
echo "1. Downloading Fonts (Orbitron)"
echo "=========================================="

if command -v wget &> /dev/null; then
    echo "Downloading Orbitron font..."
    wget -q --show-progress -O orbitron.zip \
        "https://fonts.google.com/download?family=Orbitron" || \
        echo "⚠️  Font download failed. Download manually from: https://fonts.google.com/specimen/Orbitron"
    
    if [ -f orbitron.zip ]; then
        unzip -q orbitron.zip -d orbitron
        
        # Find and copy WOFF2 files
        find orbitron -name "*.ttf" -o -name "*.woff2" | while read font; do
            echo "  Found: $(basename "$font")"
        done
        
        echo "✅ Font downloaded. You'll need to convert TTF to WOFF2 if needed."
        echo "   Use: https://cloudconvert.com/ttf-to-woff2"
    fi
else
    echo "⚠️  wget not found. Please install: sudo apt install wget"
fi

echo ""

###############################################################################
# IMAGES - Free stock photos
###############################################################################

echo "=========================================="
echo "2. Images (Manual Download Required)"
echo "=========================================="
echo ""
echo "Please download these images manually:"
echo ""
echo "🖼️  Cyberpunk City Background:"
echo "   https://unsplash.com/s/photos/cyberpunk-city"
echo "   Search: 'cyberpunk city night neon'"
echo "   Save as: cyberpunk_city.jpg"
echo ""
echo "🖼️  Hero Background:"
echo "   https://unsplash.com/s/photos/futuristic-city"
echo "   Search: 'futuristic city'"
echo "   Save as: hero_background.jpg"
echo ""
echo "🖼️  Logo:"
echo "   Create at: https://www.canva.com/"
echo "   Or use: https://www.freelogodesign.org/"
echo "   Save as: logo.png (400x150px)"
echo ""

###############################################################################
# ICONS - Heroicons (Free SVG)
###############################################################################

echo "=========================================="
echo "3. Icons (Heroicons - Free)"
echo "=========================================="
echo ""
echo "Download from: https://heroicons.com/"
echo ""
echo "Required icons:"
echo "  - health.svg → heart icon"
echo "  - energy.svg → bolt/lightning icon"
echo "  - karma.svg → sparkles icon"
echo "  - coins.svg → currency-dollar icon"
echo "  - experience.svg → star icon"
echo ""
echo "Or use Font Awesome: https://fontawesome.com/search?o=r&m=free"
echo ""

###############################################################################
# 3D MODELS - Mixamo & Poly Pizza
###############################################################################

echo "=========================================="
echo "4. 3D Models (Requires Manual Download)"
echo "=========================================="
echo ""
echo "📦 CHARACTERS & ANIMATIONS:"
echo "   Website: https://www.mixamo.com/"
echo "   Account: Free (Adobe ID required)"
echo ""
echo "   Characters to download (6):"
echo "     1. Male Base → X Bot"
echo "     2. Male Athletic → Remy"
echo "     3. Male Heavy → Big Vegas"
echo "     4. Female Base → Amy"
echo "     5. Female Athletic → Kaya"
echo "     6. Female Heavy → Jasper"
echo ""
echo "   Animations to download (11):"
echo "     1. idle → Breathing Idle"
echo "     2. walk → Walking"
echo "     3. run → Running"
echo "     4. jump → Jumping"
echo "     5. attack → Punching"
echo "     6. defend → Blocking"
echo "     7. victory → Victory"
echo "     8. defeat → Dying"
echo "     9. wave → Waving"
echo "     10. dance → Hip Hop Dancing"
echo "     11. laugh → Laughing"
echo ""
echo "   Export Settings:"
echo "     Format: FBX for Unity (.fbx)"
echo "     Skin: With Skin (for characters)"
echo "     Skin: Without Skin (for animations)"
echo "     FPS: 30"
echo ""
echo "📦 ROBOTS & ENVIRONMENT:"
echo "   Website: https://poly.pizza/"
echo "   License: CC0 (Free)"
echo ""
echo "   Search terms:"
echo "     - 'robot' (download 9 different robots)"
echo "     - 'building' (download 4 buildings)"
echo "     - 'container' (download 1)"
echo "     - 'vehicle' (download 1)"
echo ""
echo "   Download as: GLB format"
echo ""

###############################################################################
# TEXTURES - Poly Haven
###############################################################################

echo "=========================================="
echo "5. Textures (Poly Haven - Free)"
echo "=========================================="
echo ""
echo "Website: https://polyhaven.com/textures"
echo "License: CC0 (Free, no attribution)"
echo ""
echo "Required textures (31 total):"
echo ""
echo "Character Textures:"
echo "  - Skin: 4 variations (dark, light, medium, default)"
echo "  - Hair: 4 colors (black, blonde, brown, red)"
echo "  - Clothing: 3 types (casual, formal, tactical)"
echo ""
echo "Robot Textures:"
echo "  - Metal: chrome, gold, steel"
echo "  - Lights: blue, green, red (create solid color PNGs)"
echo ""
echo "Environment:"
echo "  - Walls: brick, concrete, metal"
echo "  - Floor: metal, tiles, wood"
echo "  - Props: barrel, crate"
echo ""
echo "Effects:"
echo "  - Glow: blue, green, red (gradient PNGs)"
echo "  - Particles: fire, smoke, spark"
echo ""
echo "Download settings:"
echo "  - Resolution: 2K (2048x2048)"
echo "  - Format: PNG"
echo ""

###############################################################################
# SOUNDS - Freesound
###############################################################################

echo "=========================================="
echo "6. Sounds (Freesound - Free)"
echo "=========================================="
echo ""
echo "Website: https://freesound.org/"
echo "Account: Free registration required"
echo ""
echo "Required sounds (8):"
echo "  1. menu_click.wav → Search: 'UI click button'"
echo "  2. notification.wav → Search: 'notification beep'"
echo "  3. level_up.wav → Search: 'level up success'"
echo "  4. combat_hit.wav → Search: 'punch hit impact'"
echo "  5. combat_miss.wav → Search: 'whoosh miss swing'"
echo "  6. action_success.wav → Search: 'success chime'"
echo "  7. action_fail.wav → Search: 'error buzz fail'"
echo "  8. background_music.wav → Search: 'cyberpunk ambient loop'"
echo ""
echo "Download settings:"
echo "  - Format: WAV"
echo "  - License: CC0 or CC-BY"
echo ""

###############################################################################
# SUMMARY
###############################################################################

echo ""
echo "=========================================="
echo "📋 DOWNLOAD SUMMARY"
echo "=========================================="
echo ""
echo "✅ Fonts: Partially automated (conversion needed)"
echo "⚠️  Images: Manual download required (5 files)"
echo "⚠️  Icons: Manual download required (7 files)"
echo "⚠️  3D Models: Manual download required (38 files)"
echo "⚠️  Textures: Manual download required (31 files)"
echo "⚠️  Sounds: Manual download required (8 files)"
echo ""
echo "Total: 93 assets to download"
echo ""
echo "=========================================="
echo "📚 HELPFUL RESOURCES"
echo "=========================================="
echo ""
echo "All-in-One Asset Packs:"
echo "  • Kenney.nl: https://kenney.nl/assets (Free, CC0)"
echo "  • OpenGameArt: https://opengameart.org/ (Free, various licenses)"
echo "  • itch.io: https://itch.io/game-assets/free (Free & Paid)"
echo ""
echo "Conversion Tools:"
echo "  • FBX to GLB: https://products.aspose.app/3d/conversion/fbx-to-glb"
echo "  • TTF to WOFF2: https://cloudconvert.com/ttf-to-woff2"
echo "  • Image Optimizer: https://tinypng.com/"
echo ""
echo "=========================================="
echo "🎯 NEXT STEPS"
echo "=========================================="
echo ""
echo "1. Download assets from the sources above"
echo "2. Place them in the correct directories:"
echo "   $PUBLIC_DIR/models/"
echo "   $PUBLIC_DIR/textures/"
echo "   $PUBLIC_DIR/sounds/"
echo "   $PUBLIC_DIR/images/"
echo "   $PUBLIC_DIR/icons/"
echo "   $PUBLIC_DIR/fonts/"
echo ""
echo "3. Test assets at: http://localhost:3000/asset-test"
echo ""
echo "4. See ASSET_ACQUISITION_GUIDE.md for detailed instructions"
echo ""
echo "=========================================="
echo ""

# Open browser to key websites
echo "Would you like to open the download websites in your browser? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Opening websites..."
    
    if command -v xdg-open &> /dev/null; then
        xdg-open "https://www.mixamo.com/" 2>/dev/null &
        sleep 1
        xdg-open "https://poly.pizza/" 2>/dev/null &
        sleep 1
        xdg-open "https://polyhaven.com/textures" 2>/dev/null &
        sleep 1
        xdg-open "https://freesound.org/" 2>/dev/null &
        sleep 1
        xdg-open "https://fonts.google.com/specimen/Orbitron" 2>/dev/null &
        echo "✅ Websites opened in browser"
    else
        echo "⚠️  Could not open browser automatically"
        echo "   Please visit the URLs listed above manually"
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 For detailed instructions, see:"
echo "   - ASSET_ACQUISITION_GUIDE.md"
echo "   - ASSETS_GUIDE.md"
echo ""
