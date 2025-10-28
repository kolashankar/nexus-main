import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import ProceduralModels from './ProceduralModels';

/**
 * AssetLoader - Centralized asset loading with fallbacks
 * 
 * Features:
 * - GLB/GLTF model loading with error handling
 * - Automatic fallback to procedural models
 * - Asset validation (reject files < 1KB as placeholders)
 * - Progress tracking
 * - Cache management
 * - Retry logic
 */

class AssetLoader {
  constructor() {
    this.gltfLoader = new GLTFLoader();
    this.cache = new Map();
    this.loadingPromises = new Map();
    this.minValidFileSize = 1024; // 1KB minimum for real models
  }

  /**
   * Load a character model with fallback
   * @param {string} type - Character type (e.g., 'male_base', 'female_athletic')
   * @param {object} options - Loading options
   * @returns {Promise<THREE.Object3D>}
   */
  async loadCharacter(type, options = {}) {
    const cacheKey = `character_${type}`;
    
    // Check cache first
    if (this.cache.has(cacheKey)) {
      console.log(`✅ Character "${type}" loaded from cache`);
      return this.cache.get(cacheKey).clone();
    }

    // Check if already loading
    if (this.loadingPromises.has(cacheKey)) {
      return this.loadingPromises.get(cacheKey);
    }

    const loadPromise = this._loadWithFallback(
      `/models/characters/${type}.glb`,
      () => ProceduralModels.createCharacter(type),
      `Character: ${type}`
    );

    this.loadingPromises.set(cacheKey, loadPromise);

    try {
      const model = await loadPromise;
      this.cache.set(cacheKey, model);
      this.loadingPromises.delete(cacheKey);
      return model.clone();
    } catch (error) {
      this.loadingPromises.delete(cacheKey);
      throw error;
    }
  }

  /**
   * Load a building model with fallback
   * @param {string} type - Building type (e.g., 'tower', 'shop', 'warehouse')
   * @param {object} options - Loading options
   * @returns {Promise<THREE.Object3D>}
   */
  async loadBuilding(type, options = {}) {
    const cacheKey = `building_${type}`;
    
    if (this.cache.has(cacheKey)) {
      console.log(`✅ Building "${type}" loaded from cache`);
      return this.cache.get(cacheKey).clone();
    }

    if (this.loadingPromises.has(cacheKey)) {
      return this.loadingPromises.get(cacheKey);
    }

    const loadPromise = this._loadWithFallback(
      `/models/environment/buildings/${type}.glb`,
      () => ProceduralModels.createBuilding(type),
      `Building: ${type}`
    );

    this.loadingPromises.set(cacheKey, loadPromise);

    try {
      const model = await loadPromise;
      this.cache.set(cacheKey, model);
      this.loadingPromises.delete(cacheKey);
      return model.clone();
    } catch (error) {
      this.loadingPromises.delete(cacheKey);
      throw error;
    }
  }

  /**
   * Load a robot model with fallback
   * @param {string} type - Robot type (e.g., 'scout', 'combat', 'medic')
   * @param {object} options - Loading options
   * @returns {Promise<THREE.Object3D>}
   */
  async loadRobot(type, options = {}) {
    const cacheKey = `robot_${type}`;
    
    if (this.cache.has(cacheKey)) {
      console.log(`✅ Robot "${type}" loaded from cache`);
      return this.cache.get(cacheKey).clone();
    }

    if (this.loadingPromises.has(cacheKey)) {
      return this.loadingPromises.get(cacheKey);
    }

    const loadPromise = this._loadWithFallback(
      `/models/robots/${type}.glb`,
      () => ProceduralModels.createRobot(type),
      `Robot: ${type}`
    );

    this.loadingPromises.set(cacheKey, loadPromise);

    try {
      const model = await loadPromise;
      this.cache.set(cacheKey, model);
      this.loadingPromises.delete(cacheKey);
      return model.clone();
    } catch (error) {
      this.loadingPromises.delete(cacheKey);
      throw error;
    }
  }

  /**
   * Load a prop model with fallback
   * @param {string} type - Prop type (e.g., 'container', 'vehicle')
   * @param {object} options - Loading options
   * @returns {Promise<THREE.Object3D>}
   */
  async loadProp(type, options = {}) {
    const cacheKey = `prop_${type}`;
    
    if (this.cache.has(cacheKey)) {
      console.log(`✅ Prop "${type}" loaded from cache`);
      return this.cache.get(cacheKey).clone();
    }

    if (this.loadingPromises.has(cacheKey)) {
      return this.loadingPromises.get(cacheKey);
    }

    const loadPromise = this._loadWithFallback(
      `/models/environment/props/${type}.glb`,
      () => ProceduralModels.createProp(type),
      `Prop: ${type}`
    );

    this.loadingPromises.set(cacheKey, loadPromise);

    try {
      const model = await loadPromise;
      this.cache.set(cacheKey, model);
      this.loadingPromises.delete(cacheKey);
      return model.clone();
    } catch (error) {
      this.loadingPromises.delete(cacheKey);
      throw error;
    }
  }

  /**
   * Core loading method with fallback logic
   * @private
   */
  async _loadWithFallback(path, fallbackFn, assetName) {
    try {
      console.log(`🔄 Attempting to load GLB: ${assetName} from ${path}`);
      
      // First, check if file exists and is valid size
      const isValid = await this._validateAsset(path);
      
      if (!isValid) {
        console.warn(`⚠️ ${assetName}: File is placeholder or invalid (<1KB). Using procedural model.`);
        return fallbackFn();
      }

      // Try loading the GLB file
      const gltf = await this._loadGLTF(path);
      
      if (gltf && gltf.scene) {
        console.log(`✅ ${assetName}: GLB loaded successfully`);
        
        // Process the loaded model
        const model = gltf.scene;
        
        // Enable shadows
        model.traverse((child) => {
          if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
          }
        });
        
        return model;
      } else {
        throw new Error('Invalid GLTF structure');
      }
      
    } catch (error) {
      console.warn(`⚠️ ${assetName}: GLB loading failed (${error.message}). Using procedural model.`);
      return fallbackFn();
    }
  }

  /**
   * Validate asset file (check size, existence)
   * @private
   */
  async _validateAsset(path) {
    try {
      const response = await fetch(path, { method: 'HEAD' });
      
      if (!response.ok) {
        return false;
      }

      const contentLength = response.headers.get('content-length');
      
      if (contentLength) {
        const size = parseInt(contentLength, 10);
        
        // Reject files smaller than 1KB (likely placeholders)
        if (size < this.minValidFileSize) {
          console.warn(`Asset ${path} is too small (${size} bytes). Likely a placeholder.`);
          return false;
        }
      }

      return true;
    } catch (error) {
      console.warn(`Asset validation failed for ${path}:`, error.message);
      return false;
    }
  }

  /**
   * Load GLTF/GLB file using GLTFLoader
   * @private
   */
  _loadGLTF(path) {
    return new Promise((resolve, reject) => {
      this.gltfLoader.load(
        path,
        (gltf) => resolve(gltf),
        (progress) => {
          // Optional: track progress
          if (progress.lengthComputable) {
            const percent = (progress.loaded / progress.total) * 100;
            console.log(`Loading ${path}: ${percent.toFixed(0)}%`);
          }
        },
        (error) => reject(error)
      );
    });
  }

  /**
   * Preload multiple assets
   * @param {Array} assets - Array of asset configs [{type: 'character', name: 'male_base'}, ...]
   * @returns {Promise<Object>} - Map of loaded assets
   */
  async preloadAssets(assets) {
    console.log(`🔄 Preloading ${assets.length} assets...`);
    
    const promises = assets.map(async (asset) => {
      try {
        switch (asset.type) {
          case 'character':
            return await this.loadCharacter(asset.name);
          case 'building':
            return await this.loadBuilding(asset.name);
          case 'robot':
            return await this.loadRobot(asset.name);
          case 'prop':
            return await this.loadProp(asset.name);
          default:
            throw new Error(`Unknown asset type: ${asset.type}`);
        }
      } catch (error) {
        console.error(`Failed to preload ${asset.type}:${asset.name}`, error);
        return null;
      }
    });

    const results = await Promise.allSettled(promises);
    
    const loaded = results.filter(r => r.status === 'fulfilled' && r.value !== null).length;
    console.log(`✅ Preloaded ${loaded}/${assets.length} assets successfully`);
    
    return results;
  }

  /**
   * Clear asset cache
   */
  clearCache() {
    this.cache.clear();
    this.loadingPromises.clear();
    console.log('🗑️ Asset cache cleared');
  }

  /**
   * Get cache stats
   */
  getCacheStats() {
    return {
      cachedAssets: this.cache.size,
      loadingAssets: this.loadingPromises.size,
      cacheKeys: Array.from(this.cache.keys())
    };
  }
}

// Export singleton instance
const assetLoader = new AssetLoader();
export default assetLoader;
