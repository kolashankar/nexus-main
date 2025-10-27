# 🎨 Assets Guide - Karma Nexus

## Asset Status

✅ **All asset files exist** (93 files total)  
⚠️ **Most are placeholder/minimal files** - Real assets need to be added for production

---

## Asset Testing

### Quick Test
Visit the asset test page to verify all assets:

```
http://localhost:3000/asset-test
```

This page will:
- ✅ Check which assets are accessible
- ✅ Display loading status for each category
- ✅ Show visual previews of images and icons
- ✅ Report any missing or failed assets

---

## Asset Categories

### 1. **3D Models** (38 files)
Location: `/frontend/public/models/`

**Characters** (6 files):
- `male_base.glb`, `male_athletic.glb`, `male_heavy.glb`
- `female_base.glb`, `female_athletic.glb`, `female_heavy.glb`

**Animations** (11 files):
- Basic: `idle.glb`, `walk.glb`, `run.glb`, `jump.glb`
- Combat: `attack.glb`, `defend.glb`, `victory.glb`, `defeat.glb`
- Emotes: `wave.glb`, `dance.glb`, `laugh.glb`

**Robots** (9 files):
- `combat.glb`, `scout.glb`, `guardian.glb`, `assault.glb`
- `tactical.glb`, `hacker.glb`, `medic.glb`, `harvester.glb`, `trader.glb`

**Environment** (7 files):
- Buildings: `headquarters.glb`, `shop.glb`, `tower.glb`, `warehouse.glb`
- Props: `container.glb`, `vehicle.glb`
- Terrain: `platform.glb`

**UI & Placeholders** (5 files):
- `character_placeholder.glb`, `robot_placeholder.glb`, `building_placeholder.glb`
- `hologram.glb`, `interface.glb`

### 2. **Textures** (31 files)
Location: `/frontend/public/textures/`

**Character Textures**:
- Skin: `dark.png`, `light.png`, `medium.png`, `default.png`
- Hair: `black.png`, `blonde.png`, `brown.png`, `red.png`
- Clothing: `casual.png`, `formal.png`, `tactical.png`

**Robot Textures**:
- Metal: `chrome.png`, `gold.png`, `steel.png`
- Lights: `blue.png`, `green.png`, `red.png`

**Environment Textures**:
- Walls: `brick.png`, `concrete.png`, `metal.png`
- Floor: `metal.png`, `tiles.png`, `wood.png`
- Props: `barrel.png`, `crate.png`

**Effects**:
- Glow: `blue.png`, `green.png`, `red.png`
- Particles: `fire.png`, `smoke.png`, `spark.png`

### 3. **Images** (5 files)
Location: `/frontend/public/images/`

- `logo.png` (9.7 KB) - Main logo
- `logo.svg` (2.0 KB) - Vector logo
- `placeholder_avatar.png` (2.9 MB) - Default avatar
- `cyberpunk_city.jpg` (616 KB) - Background image
- `hero_background.jpg` (865 KB) - Hero section background

### 4. **Icons** (7 files)
Location: `/frontend/public/icons/`

- `health.svg` - Health indicator
- `energy.svg` - Energy indicator  
- `karma.svg` - Karma indicator
- `coins.svg` - Currency icon
- `experience.svg` - XP icon
- `energy.jpg` - Energy icon (JPG version)
- `lightning.jpg` - Lightning effect

### 5. **Sounds** (8 files)
Location: `/frontend/public/sounds/`

- `menu_click.wav` (4.3 KB) - UI click sound
- `notification.wav` (19 KB) - Notification sound
- `level_up.wav` (48 KB) - Level up sound
- `combat_hit.wav` (17 KB) - Combat hit sound
- `combat_miss.wav` (21 KB) - Combat miss sound
- `action_success.wav` (30 KB) - Success sound
- `action_fail.wav` (30 KB) - Failure sound
- `background_music.wav` (689 KB) - Background music

### 6. **Fonts** (2 files)
Location: `/frontend/public/fonts/`

- `game_font_regular.woff2` (48 bytes) ⚠️ Placeholder
- `game_font_bold.woff2` (48 bytes) ⚠️ Placeholder

---

## How Assets Are Used

### In Code

Assets are referenced in the code using absolute paths from `/public`:

```javascript
// Images
<img src="/images/logo.png" alt="Logo" />

// Icons
<img src="/icons/health.svg" alt="Health" />

// 3D Models (with Three.js/React Three Fiber)
const loader = new GLTFLoader();
loader.load('/models/characters/male_base.glb', (gltf) => {
  scene.add(gltf.scene);
});

// Sounds
const audio = new Audio('/sounds/menu_click.wav');
audio.play();

// Fonts (in CSS)
@font-face {
  font-family: 'GameFont';
  src: url('/fonts/game_font_regular.woff2') format('woff2');
}
```

### Asset Loader Utility

Use the built-in asset loader for better control:

```javascript
import { assetLoader, verifyAssets } from './utils/assetLoader';

// Verify critical assets
const results = await verifyAssets();
console.log(`${results.available}/${results.total} assets available`);

// Preload specific assets
await assetLoader.preloadAsset('/images/logo.png', 'image');

// Preload multiple assets with progress
const assets = [
  { path: '/images/logo.png', type: 'image' },
  { path: '/models/characters/male_base.glb', type: 'model' },
  { path: '/sounds/menu_click.wav', type: 'audio' }
];

await assetLoader.preloadAssets(assets, (progress, loaded, total) => {
  console.log(`Loading: ${progress.toFixed(0)}% (${loaded}/${total})`);
});
```

---

## Asset Replacement Guide

### To Replace Placeholder Assets:

1. **Prepare your assets**:
   - 3D Models: GLB format, optimized for web
   - Textures: PNG format, power-of-2 dimensions (512x512, 1024x1024, etc.)
   - Images: PNG/JPG, compressed for web
   - Sounds: WAV or MP3, compressed
   - Fonts: WOFF2 format

2. **Replace files**:
   ```bash
   # Navigate to public directory
   cd frontend/public
   
   # Replace a specific asset
   cp /path/to/your/new_logo.png images/logo.png
   
   # Replace multiple assets
   cp /path/to/models/*.glb models/characters/
   ```

3. **Verify replacement**:
   - Visit http://localhost:3000/asset-test
   - Check that assets load correctly
   - Verify file sizes are reasonable

4. **Optimize assets**:
   ```bash
   # Optimize images
   npm install -g imagemin-cli
   imagemin public/images/*.png --out-dir=public/images/
   
   # Optimize 3D models
   npm install -g gltf-pipeline
   gltf-pipeline -i model.glb -o model-optimized.glb
   ```

---

## Current Asset Status

### ✅ Working Assets
- All directory structures exist
- All placeholder files are in place
- Asset paths are correctly configured in code
- Asset loader utility is functional

### ⚠️ Needs Attention
- **Fonts**: Current files are 48 bytes (placeholders)
  - Need real WOFF2 font files
  - Recommended: Use Google Fonts or custom game fonts

- **3D Models**: Current files are ~0.8 KB (minimal GLB files)
  - Need proper 3D models with geometry
  - Recommended: Use Blender to create or download from Sketchfab

- **Some textures**: May need higher resolution versions
  - Current textures range from 3 KB to 7 MB
  - Optimize large textures (>2 MB) for web

---

## Testing Assets

### 1. Visual Test
```
http://localhost:3000/asset-test
```

### 2. Console Test
Open browser console (F12) and run:
```javascript
// Check if asset exists
fetch('/images/logo.png')
  .then(r => console.log('Logo exists:', r.ok))
  .catch(e => console.error('Logo missing:', e));

// Verify all icons
['health', 'energy', 'karma', 'coins'].forEach(icon => {
  fetch(`/icons/${icon}.svg`)
    .then(r => console.log(`${icon}:`, r.ok ? '✅' : '❌'));
});
```

### 3. Network Tab
1. Open DevTools (F12)
2. Go to Network tab
3. Refresh page
4. Filter by type (Img, Font, Media, etc.)
5. Check for 404 errors (red)

---

## Asset Loading Best Practices

### 1. **Lazy Loading**
Load assets only when needed:
```javascript
// Load on demand
const loadCharacterModel = async (gender) => {
  const path = `/models/characters/${gender}_base.glb`;
  return await assetLoader.preloadAsset(path, 'model');
};
```

### 2. **Preloading Critical Assets**
Load important assets early:
```javascript
// In App.jsx or main component
useEffect(() => {
  const criticalAssets = [
    { path: '/images/logo.png', type: 'image' },
    { path: '/icons/health.svg', type: 'image' },
    { path: '/sounds/menu_click.wav', type: 'audio' }
  ];
  
  assetLoader.preloadAssets(criticalAssets);
}, []);
```

### 3. **Error Handling**
Always handle loading failures:
```javascript
<img 
  src="/images/logo.png"
  onError={(e) => {
    e.target.src = '/images/placeholder.png'; // Fallback
  }}
/>
```

### 4. **Loading States**
Show loading indicators:
```javascript
const [assetsLoaded, setAssetsLoaded] = useState(false);

useEffect(() => {
  verifyAssets().then(() => setAssetsLoaded(true));
}, []);

if (!assetsLoaded) {
  return <LoadingScreen />;
}
```

---

## Troubleshooting

### Assets Not Loading?

**1. Check file exists:**
```bash
ls -lh frontend/public/images/logo.png
```

**2. Check file permissions:**
```bash
chmod 644 frontend/public/images/*
```

**3. Check Vite is serving public folder:**
- Public folder should be at `frontend/public/`
- Assets should be accessible at `http://localhost:3000/images/logo.png`

**4. Clear browser cache:**
- Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
- Or clear cache in DevTools

**5. Check console for errors:**
- Open DevTools (F12)
- Look for 404 or CORS errors

### 3D Models Not Rendering?

**1. Verify GLB format:**
```bash
file frontend/public/models/characters/male_base.glb
# Should show: glTF binary model
```

**2. Check model size:**
```bash
du -h frontend/public/models/characters/male_base.glb
# Should be > 1 KB for real models
```

**3. Test model in viewer:**
- Use https://gltf-viewer.donmccurdy.com/
- Drag and drop your GLB file

---

## Summary

✅ **Asset structure is complete**  
✅ **Asset loader utility is ready**  
✅ **Asset test page is available**  
⚠️ **Replace placeholder assets with production assets**  
⚠️ **Optimize large assets for web performance**  

**Next Steps:**
1. Visit http://localhost:3000/asset-test to verify current status
2. Replace placeholder fonts with real fonts
3. Add proper 3D models if needed
4. Optimize large texture files
5. Test all assets load correctly in production build

---

**Asset Test Page:** http://localhost:3000/asset-test  
**Total Assets:** 93 files  
**Status:** Ready for production asset replacement
