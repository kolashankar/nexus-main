import React from "react";
/**
 * Scene Manager for managing Three.js scenes
 */

import * as THREE from 'three';

export class SceneManager {
  constructor(canvas, config) {
    // Initialize scene
    this.scene = new THREE.Scene();

    // Initialize camera
    this.camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    this.camera.position.set(0, 2, 5);

    // Initialize renderer
    this.renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      alpha: true,
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.outputEncoding = THREE.sRGBEncoding;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1;

    // Initialize collections
    this.lights = new Map();
    this.objects = new Map();

    // Apply configuration
    if (config) {
      this.applyConfig(config);
    } else {
      this.setupDefaultLighting();
    }

    // Setup resize handler
    window.addEventListener('resize', this.handleResize.bind(this));
  }

  /**
   * Apply scene configuration
   */
  applyConfig(config) {
    if (config.background) {
      this.scene.background = config.background;
    }

    if (config.fog) {
      this.scene.fog = new THREE.Fog(config.fog.color, config.fog.near, config.fog.far);
    }

    if (config.ambient) {
      this.addAmbientLight('ambient', config.ambient.color, config.ambient.intensity);
    }

    if (config.directional) {
      this.addDirectionalLight(
        'directional',
        config.directional.color,
        config.directional.intensity,
        config.directional.position
      );
    }
  }

  /**
   * Setup default lighting
   */
  setupDefaultLighting() {
    // Ambient light
    this.addAmbientLight('ambient', new THREE.Color(0xffffff), 0.4);

    // Directional light (sun)
    this.addDirectionalLight('sun', new THREE.Color(0xffffff), 0.8, new THREE.Vector3(5, 10, 5));
  }

  /**
   * Add ambient light
   */
  addAmbientLight(name, color, intensity) {
    const light = new THREE.AmbientLight(color, intensity);
    this.lights.set(name, light);
    this.scene.add(light);
    return light;
  }

  /**
   * Add directional light
   */
  addDirectionalLight(name, color, intensity, position) {
    const light = new THREE.DirectionalLight(color, intensity);
    light.position.copy(position);
    light.castShadow = true;
    light.shadow.mapSize.width = 2048;
    light.shadow.mapSize.height = 2048;
    light.shadow.camera.near = 0.5;
    light.shadow.camera.far = 50;

    this.lights.set(name, light);
    this.scene.add(light);
    return light;
  }

  /**
   * Add point light
   */
  addPointLight(name, color, intensity, position, distance = 0) {
    const light = new THREE.PointLight(color, intensity, distance);
    light.position.copy(position);
    light.castShadow = true;

    this.lights.set(name, light);
    this.scene.add(light);
    return light;
  }

  /**
   * Add object to scene
   */
  addObject(name, object) {
    this.objects.set(name, object);
    this.scene.add(object);
  }

  /**
   * Remove object from scene
   */
  removeObject(name) {
    const object = this.objects.get(name);
    if (object) {
      this.scene.remove(object);
      this.objects.delete(name);
    }
  }

  /**
   * Get object by name
   */
  getObject(name) {
    return this.objects.get(name);
  }

  /**
   * Get light by name
   */
  getLight(name) {
    return this.lights.get(name);
  }

  /**
   * Handle window resize
   */
  handleResize() {
    const width = window.innerWidth;
    const height = window.innerHeight;

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();

    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  }

  /**
   * Render scene
   */
  render() {
    this.renderer.render(this.scene, this.camera);
  }

  /**
   * Set camera position
   */
  setCameraPosition(x, y, z) {
    this.camera.position.set(x, y, z);
  }

  /**
   * Look at target
   */
  lookAt(target) {
    this.camera.lookAt(target);
  }

  /**
   * Dispose of resources
   */
  dispose() {
    window.removeEventListener('resize', this.handleResize.bind(this));

    // Dispose renderer
    this.renderer.dispose();

    // Clear scene
    this.scene.traverse((object) => {
      if (object instanceof THREE.Mesh) {
        object.geometry.dispose();
        if (Array.isArray(object.material)) {
          object.material.forEach((mat) => mat.dispose());
        } else {
          object.material.dispose();
        }
      }
    });

    this.lights.clear();
    this.objects.clear();
  }
}
