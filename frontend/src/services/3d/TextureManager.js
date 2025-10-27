import React from "react";
/**
 * Texture Manager for loading and managing textures
 */

import * as THREE from 'three';

class TextureManager {
  constructor() {
    this.loader = new THREE.TextureLoader();
    this.cache = new Map();
    this.loadingPromises = new Map();
  }

  /**
   * Load a single texture
   */
  async load(url, options = {}) {
    // Check cache
    if (this.cache.has(url)) {
      return this.cache.get(url);
    }

    // Check if already loading
    if (this.loadingPromises.has(url)) {
      return this.loadingPromises.get(url);
    }

    // Load new texture
    const loadPromise = new Promise((resolve, reject) => {
      this.loader.load(
        url,
        (texture) => {
          this.applyOptions(texture, options);
          this.cache.set(url, texture);
          this.loadingPromises.delete(url);
          resolve(texture);
        },
        undefined,
        (error) => {
          this.loadingPromises.delete(url);
          reject(error);
        }
      );
    });

    this.loadingPromises.set(url, loadPromise);
    return loadPromise;
  }

  /**
   * Load multiple textures
   */
  async loadMultiple(urls, options = {}) {
    const promises = urls.map((url) => this.load(url, options));
    return Promise.all(promises);
  }

  /**
   * Apply texture options
   */
  applyOptions(texture, options) {
    if (options.wrapS !== undefined) {
      texture.wrapS = options.wrapS;
    }

    if (options.wrapT !== undefined) {
      texture.wrapT = options.wrapT;
    }

    if (options.repeat) {
      texture.repeat.set(options.repeat[0], options.repeat[1]);
    }

    if (options.encoding !== undefined) {
      texture.encoding = options.encoding;
    }

    if (options.anisotropy !== undefined) {
      texture.anisotropy = options.anisotropy;
    }

    texture.needsUpdate = true;
  }

  /**
   * Create a material with texture
   */
  async createMaterial(textureUrl, materialOptions = {}) {
    const texture = await this.load(textureUrl);
    return new THREE.MeshStandardMaterial({
      map: texture,
      ...materialOptions,
    });
  }

  /**
   * Create PBR material with multiple textures
   */
  async createPBRMaterial(textures) {
    const material = new THREE.MeshStandardMaterial();

    if (textures.diffuse) {
      material.map = await this.load(textures.diffuse);
    }

    if (textures.normal) {
      material.normalMap = await this.load(textures.normal);
    }

    if (textures.roughness) {
      material.roughnessMap = await this.load(textures.roughness);
    }

    if (textures.metalness) {
      material.metalnessMap = await this.load(textures.metalness);
    }

    if (textures.ao) {
      material.aoMap = await this.load(textures.ao);
    }

    if (textures.emissive) {
      material.emissiveMap = await this.load(textures.emissive);
      material.emissive.set(0xffffff);
    }

    return material;
  }

  /**
   * Get cached texture
   */
  getCached(url) {
    return this.cache.get(url);
  }

  /**
   * Remove texture from cache
   */
  remove(url) {
    const texture = this.cache.get(url);
    if (texture) {
      texture.dispose();
      this.cache.delete(url);
    }
  }

  /**
   * Clear all cached textures
   */
  clear() {
    this.cache.forEach((texture) => texture.dispose());
    this.cache.clear();
  }

  /**
   * Get cache size
   */
  getCacheSize() {
    return this.cache.size;
  }
}

// Singleton instance
export const textureManager = new TextureManager();
