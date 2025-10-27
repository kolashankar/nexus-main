/**
 * Asset Loader Utility
 * Handles loading and verification of all game assets
 */

export class AssetLoader {
  constructor() {
    this.loadedAssets = new Map();
    this.failedAssets = new Map();
    this.loadingProgress = 0;
  }

  /**
   * Preload an asset and track its status
   */
  async preloadAsset(path, type = 'auto') {
    if (this.loadedAssets.has(path)) {
      return this.loadedAssets.get(path);
    }

    try {
      const fullPath = path.startsWith('/') ? path : `/${path}`;
      
      switch (type) {
        case 'image':
          return await this.loadImage(fullPath);
        case 'model':
          return await this.loadModel(fullPath);
        case 'audio':
          return await this.loadAudio(fullPath);
        case 'font':
          return await this.loadFont(fullPath);
        default:
          return await this.loadGeneric(fullPath);
      }
    } catch (error) {
      console.warn(`Failed to load asset: ${path}`, error);
      this.failedAssets.set(path, error);
      return null;
    }
  }

  /**
   * Load an image asset
   */
  loadImage(path) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        this.loadedAssets.set(path, img);
        resolve(img);
      };
      img.onerror = () => {
        reject(new Error(`Failed to load image: ${path}`));
      };
      img.src = path;
    });
  }

  /**
   * Load a 3D model (GLB/GLTF)
   */
  async loadModel(path) {
    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const blob = await response.blob();
      this.loadedAssets.set(path, blob);
      return blob;
    } catch (error) {
      throw new Error(`Failed to load model: ${path} - ${error.message}`);
    }
  }

  /**
   * Load an audio file
   */
  async loadAudio(path) {
    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const arrayBuffer = await response.arrayBuffer();
      this.loadedAssets.set(path, arrayBuffer);
      return arrayBuffer;
    } catch (error) {
      throw new Error(`Failed to load audio: ${path} - ${error.message}`);
    }
  }

  /**
   * Load a font
   */
  async loadFont(path) {
    try {
      const fontFace = new FontFace('GameFont', `url(${path})`);
      await fontFace.load();
      document.fonts.add(fontFace);
      this.loadedAssets.set(path, fontFace);
      return fontFace;
    } catch (error) {
      throw new Error(`Failed to load font: ${path} - ${error.message}`);
    }
  }

  /**
   * Generic asset loader
   */
  async loadGeneric(path) {
    try {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.blob();
      this.loadedAssets.set(path, data);
      return data;
    } catch (error) {
      throw new Error(`Failed to load asset: ${path} - ${error.message}`);
    }
  }

  /**
   * Preload multiple assets
   */
  async preloadAssets(assets, onProgress) {
    const total = assets.length;
    let loaded = 0;

    const promises = assets.map(async ({ path, type }) => {
      try {
        await this.preloadAsset(path, type);
        loaded++;
        this.loadingProgress = (loaded / total) * 100;
        if (onProgress) {
          onProgress(this.loadingProgress, loaded, total);
        }
      } catch (error) {
        console.warn(`Asset load failed: ${path}`, error);
      }
    });

    await Promise.allSettled(promises);
    return {
      loaded: this.loadedAssets.size,
      failed: this.failedAssets.size,
      total: assets.length
    };
  }

  /**
   * Check if an asset exists
   */
  async checkAsset(path) {
    try {
      const response = await fetch(path, { method: 'HEAD' });
      return response.ok;
    } catch {
      return false;
    }
  }

  /**
   * Get loading statistics
   */
  getStats() {
    return {
      loaded: this.loadedAssets.size,
      failed: this.failedAssets.size,
      progress: this.loadingProgress,
      failedPaths: Array.from(this.failedAssets.keys())
    };
  }

  /**
   * Clear all cached assets
   */
  clear() {
    this.loadedAssets.clear();
    this.failedAssets.clear();
    this.loadingProgress = 0;
  }
}

// Singleton instance
export const assetLoader = new AssetLoader();

// Asset verification utility
export async function verifyAssets() {
  const criticalAssets = [
    // Images
    { path: '/images/logo.png', type: 'image' },
    { path: '/images/placeholder_avatar.png', type: 'image' },
    
    // Icons
    { path: '/icons/health.svg', type: 'image' },
    { path: '/icons/energy.svg', type: 'image' },
    { path: '/icons/karma.svg', type: 'image' },
    
    // Models (placeholders)
    { path: '/models/placeholders/character_placeholder.glb', type: 'model' },
    { path: '/models/characters/male_base.glb', type: 'model' },
    { path: '/models/characters/female_base.glb', type: 'model' },
  ];

  console.log('🔍 Verifying critical assets...');
  
  const results = await Promise.allSettled(
    criticalAssets.map(async ({ path, type }) => {
      const exists = await assetLoader.checkAsset(path);
      return { path, type, exists };
    })
  );

  const verified = results
    .filter(r => r.status === 'fulfilled')
    .map(r => r.value);

  const available = verified.filter(a => a.exists);
  const missing = verified.filter(a => !a.exists);

  console.log(`✅ Available: ${available.length}/${criticalAssets.length}`);
  
  if (missing.length > 0) {
    console.warn('⚠️ Missing assets:', missing.map(a => a.path));
  }

  return {
    total: criticalAssets.length,
    available: available.length,
    missing: missing.length,
    missingPaths: missing.map(a => a.path)
  };
}

export default assetLoader;
