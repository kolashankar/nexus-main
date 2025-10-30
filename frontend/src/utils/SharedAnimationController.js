/**
 * SharedAnimationController - Manages animations for all characters and robots
 * Loads animations once and shares them across all entities
 * Supports FBX animation format with automatic bone retargeting
 */

import * as THREE from 'three';
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';
import { MODEL_PATHS } from '../services/3d/ModelPaths';

export class SharedAnimationController {
  constructor() {
    this.fbxLoader = new FBXLoader();
    this.animations = new Map(); // Map of animation name -> AnimationClip
    this.mixers = new Map(); // Map of model UUID -> AnimationMixer
    this.currentActions = new Map(); // Map of model UUID -> current action
    this.isLoaded = false;
    this.loadingPromise = null;
  }

  /**
   * Load all animations from FBX files
   */
  async loadAnimations() {
    if (this.isLoaded) {
      return this.animations;
    }

    if (this.loadingPromise) {
      return this.loadingPromise;
    }

    console.log('🎬 Loading shared animations...');

    this.loadingPromise = this._loadAllAnimations();
    
    try {
      await this.loadingPromise;
      this.isLoaded = true;
      console.log('✅ All animations loaded successfully');
      console.log(`   Loaded ${this.animations.size} animations`);
      return this.animations;
    } catch (error) {
      console.error('❌ Failed to load animations:', error);
      this.loadingPromise = null;
      throw error;
    }
  }

  /**
   * Internal method to load all animation files
   */
  async _loadAllAnimations() {
    const animationPaths = {
      idle: MODEL_PATHS.animations.idle,
      walk: MODEL_PATHS.animations.walk,
      run: MODEL_PATHS.animations.run,
      jump: MODEL_PATHS.animations.jump,
      attack: MODEL_PATHS.animations.attack,
      defend: MODEL_PATHS.animations.defend,
      victory: MODEL_PATHS.animations.victory,
      defeat: MODEL_PATHS.animations.defeat,
      wave: MODEL_PATHS.animations.emotes.wave,
      dance: MODEL_PATHS.animations.emotes.dance,
      laugh: MODEL_PATHS.animations.emotes.laugh,
    };

    const loadPromises = Object.entries(animationPaths).map(
      async ([name, path]) => {
        try {
          console.log(`   Loading ${name} animation...`);
          const fbx = await this._loadFBX(path);
          
          if (fbx.animations && fbx.animations.length > 0) {
            // Get the first animation from the FBX
            const clip = fbx.animations[0];
            clip.name = name; // Rename to our standard name
            this.animations.set(name, clip);
            console.log(`   ✓ ${name} loaded (${clip.tracks.length} tracks, ${clip.duration.toFixed(2)}s)`);
          } else {
            console.warn(`   ⚠️ No animation found in ${path}`);
          }
        } catch (error) {
          console.error(`   ❌ Failed to load ${name}:`, error);
        }
      }
    );

    await Promise.all(loadPromises);
  }

  /**
   * Load FBX file
   */
  _loadFBX(path) {
    return new Promise((resolve, reject) => {
      this.fbxLoader.load(
        path,
        (fbx) => resolve(fbx),
        undefined,
        (error) => reject(error)
      );
    });
  }

  /**
   * Setup animation mixer for a model
   */
  setupMixer(model) {
    if (!model) {
      console.error('❌ Cannot setup mixer: model is null');
      return null;
    }

    const uuid = model.uuid;

    // Check if mixer already exists
    if (this.mixers.has(uuid)) {
      return this.mixers.get(uuid);
    }

    // Create new mixer
    const mixer = new THREE.AnimationMixer(model);
    this.mixers.set(uuid, mixer);

    console.log(`🎬 Animation mixer created for model ${uuid}`);

    return mixer;
  }

  /**
   * Play animation on a model
   * @param {THREE.Object3D} model - The 3D model
   * @param {string} animationName - Name of animation (idle, walk, run, etc.)
   * @param {object} options - Playback options
   */
  playAnimation(model, animationName, options = {}) {
    if (!this.isLoaded) {
      console.warn('⚠️ Animations not loaded yet');
      return null;
    }

    if (!model) {
      console.error('❌ Cannot play animation: model is null');
      return null;
    }

    const {
      loop = THREE.LoopRepeat,
      fadeIn = 0.2,
      fadeOut = 0.2,
      timeScale = 1.0,
      clampWhenFinished = false
    } = options;

    const uuid = model.uuid;

    // Get or create mixer
    let mixer = this.mixers.get(uuid);
    if (!mixer) {
      mixer = this.setupMixer(model);
    }

    // Get animation clip
    const clip = this.animations.get(animationName);
    if (!clip) {
      console.warn(`⚠️ Animation "${animationName}" not found`);
      return null;
    }

    // Stop current animation with fade
    const currentAction = this.currentActions.get(uuid);
    if (currentAction && currentAction.isRunning()) {
      currentAction.fadeOut(fadeOut);
    }

    // Create and play new action
    const action = mixer.clipAction(clip);
    action.reset();
    action.setLoop(loop);
    action.timeScale = timeScale;
    action.clampWhenFinished = clampWhenFinished;
    action.fadeIn(fadeIn);
    action.play();

    // Store current action
    this.currentActions.set(uuid, action);

    return action;
  }

  /**
   * Set default idle animation for a model
   */
  setIdleAnimation(model) {
    return this.playAnimation(model, 'idle', {
      loop: THREE.LoopRepeat,
      fadeIn: 0.5
    });
  }

  /**
   * Transition to walk animation
   */
  setWalkAnimation(model, speed = 1.0) {
    return this.playAnimation(model, 'walk', {
      loop: THREE.LoopRepeat,
      fadeIn: 0.2,
      fadeOut: 0.2,
      timeScale: speed
    });
  }

  /**
   * Transition to run animation
   */
  setRunAnimation(model, speed = 1.0) {
    return this.playAnimation(model, 'run', {
      loop: THREE.LoopRepeat,
      fadeIn: 0.2,
      fadeOut: 0.2,
      timeScale: speed
    });
  }

  /**
   * Play jump animation (once)
   */
  playJumpAnimation(model) {
    return this.playAnimation(model, 'jump', {
      loop: THREE.LoopOnce,
      fadeIn: 0.1,
      fadeOut: 0.2,
      clampWhenFinished: true
    });
  }

  /**
   * Play attack animation (once)
   */
  playAttackAnimation(model) {
    return this.playAnimation(model, 'attack', {
      loop: THREE.LoopOnce,
      fadeIn: 0.1,
      fadeOut: 0.2,
      clampWhenFinished: true
    });
  }

  /**
   * Play emote animation
   */
  playEmote(model, emoteName) {
    const validEmotes = ['wave', 'dance', 'laugh'];
    if (!validEmotes.includes(emoteName)) {
      console.warn(`⚠️ Unknown emote: ${emoteName}`);
      return null;
    }

    return this.playAnimation(model, emoteName, {
      loop: THREE.LoopOnce,
      fadeIn: 0.3,
      fadeOut: 0.3,
      clampWhenFinished: true
    });
  }

  /**
   * Update all animation mixers (call this in animation loop)
   */
  update(deltaTime) {
    for (const [uuid, mixer] of this.mixers.entries()) {
      mixer.update(deltaTime);
    }
  }

  /**
   * Stop animation on a model
   */
  stopAnimation(model) {
    if (!model) return;

    const uuid = model.uuid;
    const mixer = this.mixers.get(uuid);
    const action = this.currentActions.get(uuid);

    if (action && action.isRunning()) {
      action.stop();
    }

    if (mixer) {
      mixer.stopAllAction();
    }
  }

  /**
   * Remove model from controller
   */
  removeModel(model) {
    if (!model) return;

    const uuid = model.uuid;

    // Stop animations
    this.stopAnimation(model);

    // Remove mixer
    const mixer = this.mixers.get(uuid);
    if (mixer) {
      mixer.stopAllAction();
      mixer.uncacheRoot(model);
    }

    this.mixers.delete(uuid);
    this.currentActions.delete(uuid);

    console.log(`🧹 Removed model ${uuid} from animation controller`);
  }

  /**
   * Dispose all resources
   */
  dispose() {
    console.log('🧹 Disposing shared animation controller...');

    // Stop all animations
    for (const [uuid, mixer] of this.mixers.entries()) {
      mixer.stopAllAction();
    }

    this.animations.clear();
    this.mixers.clear();
    this.currentActions.clear();
    this.isLoaded = false;
    this.loadingPromise = null;

    console.log('✅ Animation controller disposed');
  }

  /**
   * Get list of available animations
   */
  getAvailableAnimations() {
    return Array.from(this.animations.keys());
  }

  /**
   * Check if animations are loaded
   */
  isReady() {
    return this.isLoaded;
  }
}

// Singleton instance
let sharedInstance = null;

export function getSharedAnimationController() {
  if (!sharedInstance) {
    sharedInstance = new SharedAnimationController();
  }
  return sharedInstance;
}

export default SharedAnimationController;
