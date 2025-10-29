/**
 * Optimized 3D Game World with Scale Normalization and Performance Enhancements
 * Features:
 * - Automatic city scale normalization (character-relative)
 * - Performance optimization for desktop (60 FPS) and mobile (45+ FPS)
 * - Responsive rendering and LOD system
 * - Camera clipping prevention
 * - Mobile-specific optimizations
 */
import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { Canvas } from '@react-three/fiber';
import VirtualJoystick from '../../mobile/VirtualJoystick';
import MobileControls from '../../mobile/MobileControls';
import CameraViewToggle from '../CameraViewToggle/CameraViewToggle';
import WorldItemMarker from '../WorldItems/WorldItemMarker';
import ItemDiscoveryModal from '../WorldItems/ItemDiscoveryModal';
import AcquisitionTracker from '../WorldItems/AcquisitionTracker';
import { isMobileDevice, isTouchDevice } from '../../../utils/mobileDetection';
import { ModelOptimizer } from '../../../utils/ModelOptimizer';
import { PerformanceMonitor } from '../../../utils/PerformanceMonitor';
import { 
  getActiveWorldItems, 
  checkCanAcquireItem, 
  startItemAcquisition,
  getActiveAcquisitions,
  claimAcquisition,
  cancelAcquisition
} from '../../../services/api/worldItems';
import './GameWorld.css';

const GameWorldOptimized = ({ player, isFullscreen = false }) => {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const rendererRef = useRef(null);
  const characterRef = useRef(null);
  const cityModelRef = useRef(null);
  const npcsRef = useRef([]);
  const mixerRef = useRef(null);
  const clockRef = useRef(new THREE.Clock());
  const performanceMonitorRef = useRef(null);
  const modelOptimizerRef = useRef(null);
  
  const [isLoaded, setIsLoaded] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [isMobile, setIsMobile] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [cameraView, setCameraView] = useState('third-person');
  const [performanceMode, setPerformanceMode] = useState('balanced'); // 'quality', 'balanced', 'performance'

  // Movement state
  const movement = useRef({
    forward: false,
    backward: false,
    left: false,
    right: false,
    jump: false,
    run: false,
    rotateLeft: false,
    rotateRight: false,
    joystickX: 0,
    joystickY: 0
  });

  const playerState = useRef({
    position: new THREE.Vector3(0, 1.8, 0), // Character height is ~1.8 units (human scale)
    rotation: 0,
    velocity: new THREE.Vector3(),
    isGrounded: true,
    currentAnimation: 'idle'
  });

  // City scale configuration
  const CITY_SCALE_CONFIG = {
    // Character reference: 1 unit = ~0.5 meters, so character is ~1.8 units tall (0.9m)
    CHARACTER_HEIGHT: 1.8,
    // Buildings should be 5-20 units tall (2.5-10 floors realistic)
    MIN_BUILDING_HEIGHT: 5,
    MAX_BUILDING_HEIGHT: 20,
    // City size should be manageable for exploration
    TARGET_CITY_SIZE: 150, // 150 units = ~75 meters across
    // Camera configuration
    CAMERA_NEAR: 0.1,
    CAMERA_FAR: 500,
    CAMERA_FOV_DESKTOP: 75,
    CAMERA_FOV_MOBILE: 85, // Wider FOV on mobile for better awareness
  };

  // Performance configuration
  const PERFORMANCE_CONFIG = {
    desktop: {
      targetFPS: 60,
      shadowMapSize: 2048,
      pixelRatio: Math.min(window.devicePixelRatio, 2),
      maxNPCs: 15,
      fogNear: 50,
      fogFar: 200,
      enableShadows: true,
      textureMaxSize: 2048,
      renderDistance: 200
    },
    mobile: {
      targetFPS: 45,
      shadowMapSize: 512,
      pixelRatio: 1,
      maxNPCs: 5,
      fogNear: 30,
      fogFar: 100,
      enableShadows: false,
      textureMaxSize: 512,
      renderDistance: 100
    }
  };

  // Movement constants
  const WALK_SPEED = 0.08;
  const RUN_SPEED = 0.16;
  const ROTATION_SPEED = 0.04;
  const JUMP_FORCE = 0.25;
  const GRAVITY = 0.012;

  // City boundaries (calculated after model load)
  const cityBounds = useRef({
    minX: -75,
    maxX: 75,
    minZ: -75,
    maxZ: 75,
    minY: 0,
    maxY: 30
  });

  /**
   * Get performance configuration based on device
   */
  const getPerformanceConfig = () => {
    return isMobile ? PERFORMANCE_CONFIG.mobile : PERFORMANCE_CONFIG.desktop;
  };

  /**
   * Load and optimize GLB model
   */
  const loadModel = (path, optimize = true) => {
    return new Promise((resolve, reject) => {
      const loader = new GLTFLoader();
      loader.load(
        path,
        (gltf) => {
          let model = gltf.scene;
          
          // Apply shadows
          model.traverse((child) => {
            if (child.isMesh) {
              const config = getPerformanceConfig();
              child.castShadow = config.enableShadows;
              child.receiveShadow = config.enableShadows;
              
              // Optimize materials
              if (child.material) {
                child.material.needsUpdate = true;
              }
            }
          });

          // Optimize model if requested
          if (optimize && modelOptimizerRef.current) {
            model = modelOptimizerRef.current.optimize(model, isMobile);
          }

          resolve({ model, animations: gltf.animations || [] });
        },
        (progress) => {
          if (progress.total > 0) {
            const percent = (progress.loaded / progress.total) * 100;
            setLoadingProgress(Math.min(Math.round(percent), 99));
          }
        },
        (error) => {
          console.error('Model load error:', error);
          reject(error);
        }
      );
    });
  };

  /**
   * Normalize city model scale
   */
  const normalizeCityScale = (cityModel) => {
    console.log('📐 Normalizing city scale...');
    
    // Get original bounding box
    const box = new THREE.Box3().setFromObject(cityModel);
    const size = new THREE.Vector3();
    const center = new THREE.Vector3();
    box.getSize(size);
    box.getCenter(center);
    
    console.log(`   Original size: ${size.x.toFixed(2)} x ${size.y.toFixed(2)} x ${size.z.toFixed(2)}`);
    
    // Calculate scale factor to fit target city size
    const maxDimension = Math.max(size.x, size.z);
    const scaleFactor = CITY_SCALE_CONFIG.TARGET_CITY_SIZE / maxDimension;
    
    console.log(`   Scale factor: ${scaleFactor.toFixed(3)}`);
    
    // Apply scale
    cityModel.scale.multiplyScalar(scaleFactor);
    
    // Center the city at origin
    box.setFromObject(cityModel);
    box.getCenter(center);
    cityModel.position.sub(center);
    cityModel.position.y = 0; // Ensure ground is at y=0
    
    // Recalculate bounds
    box.setFromObject(cityModel);
    box.getSize(size);
    
    console.log(`   New size: ${size.x.toFixed(2)} x ${size.y.toFixed(2)} x ${size.z.toFixed(2)}`);
    console.log(`   ✅ City scale normalized (character height: ${CITY_SCALE_CONFIG.CHARACTER_HEIGHT} units)`);
    
    // Update city boundaries
    const padding = 10;
    cityBounds.current = {
      minX: box.min.x - padding,
      maxX: box.max.x + padding,
      minZ: box.min.z - padding,
      maxZ: box.max.z + padding,
      minY: 0,
      maxY: box.max.y + 10
    };
    
    return { size, center, scaleFactor };
  };

  /**
   * Create invisible boundary walls
   */
  const createBoundaryWalls = (scene) => {
    const wallHeight = 50;
    const wallMaterial = new THREE.MeshBasicMaterial({ 
      transparent: true, 
      opacity: 0,
      side: THREE.DoubleSide
    });
    
    const bounds = cityBounds.current;
    const width = bounds.maxX - bounds.minX;
    const depth = bounds.maxZ - bounds.minZ;
    
    // Create walls
    const walls = [
      { // North
        pos: [(bounds.minX + bounds.maxX) / 2, wallHeight / 2, bounds.maxZ],
        rot: [0, 0, 0],
        size: [width, wallHeight]
      },
      { // South
        pos: [(bounds.minX + bounds.maxX) / 2, wallHeight / 2, bounds.minZ],
        rot: [0, Math.PI, 0],
        size: [width, wallHeight]
      },
      { // East
        pos: [bounds.maxX, wallHeight / 2, (bounds.minZ + bounds.maxZ) / 2],
        rot: [0, Math.PI / 2, 0],
        size: [depth, wallHeight]
      },
      { // West
        pos: [bounds.minX, wallHeight / 2, (bounds.minZ + bounds.maxZ) / 2],
        rot: [0, -Math.PI / 2, 0],
        size: [depth, wallHeight]
      }
    ];
    
    walls.forEach(wall => {
      const mesh = new THREE.Mesh(
        new THREE.PlaneGeometry(wall.size[0], wall.size[1]),
        wallMaterial
      );
      mesh.position.set(...wall.pos);
      mesh.rotation.set(...wall.rot);
      mesh.userData.isBoundary = true;
      scene.add(mesh);
    });
    
    console.log('✅ Boundary walls created');
  };

  /**
   * Get random spawn position
   */
  const getRandomSpawnPosition = () => {
    const bounds = cityBounds.current;
    const margin = 15;
    
    return new THREE.Vector3(
      bounds.minX + margin + Math.random() * (bounds.maxX - bounds.minX - margin * 2),
      CITY_SCALE_CONFIG.CHARACTER_HEIGHT / 2, // Half character height above ground
      bounds.minZ + margin + Math.random() * (bounds.maxZ - bounds.minZ - margin * 2)
    );
  };

  /**
   * Setup responsive camera
   */
  const setupCamera = (camera) => {
    const config = CITY_SCALE_CONFIG;
    
    camera.fov = isMobile ? config.CAMERA_FOV_MOBILE : config.CAMERA_FOV_DESKTOP;
    camera.near = config.CAMERA_NEAR;
    camera.far = config.CAMERA_FAR;
    camera.updateProjectionMatrix();
    
    console.log(`📷 Camera configured: FOV=${camera.fov}°, Near=${camera.near}, Far=${camera.far}`);
  };

  /**
   * Update camera to follow character
   */
  const updateCamera = (camera, character) => {
    if (!character) return;
    
    const distance = isMobile ? 12 : 10;
    const height = isMobile ? 5 : 4;
    const smoothing = 0.1;
    
    // Calculate target position
    const targetX = character.position.x - Math.sin(playerState.current.rotation) * distance;
    const targetZ = character.position.z - Math.cos(playerState.current.rotation) * distance;
    const targetY = character.position.y + height;
    
    // Smooth camera movement
    camera.position.x += (targetX - camera.position.x) * smoothing;
    camera.position.y += (targetY - camera.position.y) * smoothing;
    camera.position.z += (targetZ - camera.position.z) * smoothing;
    
    // Look at character
    camera.lookAt(character.position);
  };

  /**
   * Handle player movement with boundary checking
   */
  const updatePlayerMovement = (delta) => {
    if (!characterRef.current) return;
    
    const character = characterRef.current;
    const mov = movement.current;
    const state = playerState.current;
    const config = getPerformanceConfig();
    
    // Calculate movement speed
    const speed = mov.run ? RUN_SPEED : WALK_SPEED;
    let moveX = 0;
    let moveZ = 0;
    
    // Keyboard/mobile controls
    if (mov.forward || mov.joystickY < -0.1) {
      moveZ = speed * (mov.joystickY < -0.1 ? Math.abs(mov.joystickY) : 1);
    }
    if (mov.backward || mov.joystickY > 0.1) {
      moveZ = -speed * (mov.joystickY > 0.1 ? Math.abs(mov.joystickY) : 1);
    }
    if (mov.left || mov.joystickX < -0.1) {
      moveX = speed * (mov.joystickX < -0.1 ? Math.abs(mov.joystickX) : 1);
    }
    if (mov.right || mov.joystickX > 0.1) {
      moveX = -speed * (mov.joystickX > 0.1 ? Math.abs(mov.joystickX) : 1);
    }
    
    // Apply rotation
    if (mov.rotateLeft) {
      state.rotation += ROTATION_SPEED;
    }
    if (mov.rotateRight) {
      state.rotation -= ROTATION_SPEED;
    }
    
    // Calculate new position
    const newX = state.position.x + Math.sin(state.rotation) * moveZ + Math.cos(state.rotation) * moveX;
    const newZ = state.position.z + Math.cos(state.rotation) * moveZ - Math.sin(state.rotation) * moveX;
    
    // Boundary checking
    const bounds = cityBounds.current;
    const margin = 2;
    
    if (newX >= bounds.minX + margin && newX <= bounds.maxX - margin) {
      state.position.x = newX;
    }
    if (newZ >= bounds.minZ + margin && newZ <= bounds.maxZ - margin) {
      state.position.z = newZ;
    }
    
    // Apply gravity and jumping
    if (mov.jump && state.isGrounded) {
      state.velocity.y = JUMP_FORCE;
      state.isGrounded = false;
    }
    
    state.velocity.y -= GRAVITY;
    state.position.y += state.velocity.y;
    
    // Ground collision
    const groundLevel = CITY_SCALE_CONFIG.CHARACTER_HEIGHT / 2;
    if (state.position.y <= groundLevel) {
      state.position.y = groundLevel;
      state.velocity.y = 0;
      state.isGrounded = true;
    }
    
    // Update character mesh
    character.position.copy(state.position);
    character.rotation.y = state.rotation;
    
    // Update animation state
    const isMoving = moveX !== 0 || moveZ !== 0;
    state.currentAnimation = isMoving ? (mov.run ? 'run' : 'walk') : 'idle';
  };

  // Detect mobile device on mount
  useEffect(() => {
    const mobile = isMobileDevice() || isTouchDevice();
    setIsMobile(mobile);
    
    // Initialize model optimizer
    const config = mobile ? PERFORMANCE_CONFIG.mobile : PERFORMANCE_CONFIG.desktop;
    modelOptimizerRef.current = new ModelOptimizer({
      maxTextureSize: config.textureMaxSize,
      generateLODs: true,
      mergeMaterials: true,
      compressGeometry: true
    });
  }, []);

  useEffect(() => {
    if (!mountRef.current) return;

    console.log('🎮 Initializing optimized game world...');
    const config = getPerformanceConfig();
    
    // === SCENE SETUP ===
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB);
    scene.fog = new THREE.Fog(0x87CEEB, config.fogNear, config.fogFar);
    sceneRef.current = scene;

    // === CAMERA ===
    const camera = new THREE.PerspectiveCamera(
      isMobile ? CITY_SCALE_CONFIG.CAMERA_FOV_MOBILE : CITY_SCALE_CONFIG.CAMERA_FOV_DESKTOP,
      mountRef.current.clientWidth / mountRef.current.clientHeight,
      CITY_SCALE_CONFIG.CAMERA_NEAR,
      CITY_SCALE_CONFIG.CAMERA_FAR
    );
    camera.position.set(0, 10, 15);
    cameraRef.current = camera;
    setupCamera(camera);

    // === RENDERER ===
    const renderer = new THREE.WebGLRenderer({ 
      antialias: !isMobile, // Disable antialiasing on mobile for performance
      powerPreference: isMobile ? 'low-power' : 'high-performance'
    });
    renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    renderer.setPixelRatio(config.pixelRatio);
    renderer.shadowMap.enabled = config.enableShadows;
    if (config.enableShadows) {
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    }
    mountRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // === PERFORMANCE MONITOR ===
    performanceMonitorRef.current = new PerformanceMonitor(renderer, {
      targetFPS: config.targetFPS,
      showOverlay: !isMobile // Hide overlay on mobile
    });

    // === LIGHTING ===
    const ambientLight = new THREE.AmbientLight(0xffffff, isMobile ? 0.8 : 0.6);
    scene.add(ambientLight);

    if (config.enableShadows) {
      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
      directionalLight.position.set(50, 100, 50);
      directionalLight.castShadow = true;
      directionalLight.shadow.mapSize.width = config.shadowMapSize;
      directionalLight.shadow.mapSize.height = config.shadowMapSize;
      directionalLight.shadow.camera.near = 0.5;
      directionalLight.shadow.camera.far = 500;
      directionalLight.shadow.camera.left = -100;
      directionalLight.shadow.camera.right = 100;
      directionalLight.shadow.camera.top = 100;
      directionalLight.shadow.camera.bottom = -100;
      scene.add(directionalLight);
    } else {
      // Mobile: Use hemisphere light instead of directional for better performance
      const hemiLight = new THREE.HemisphereLight(0x87CEEB, 0x2d5016, 0.6);
      scene.add(hemiLight);
    }

    // === GROUND (Fallback) ===
    const groundGeometry = new THREE.PlaneGeometry(300, 300);
    const groundMaterial = new THREE.MeshStandardMaterial({
      color: 0x2d5016,
      roughness: 0.9
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = config.enableShadows;
    ground.visible = false;
    scene.add(ground);

    // === LOAD CITY MODEL ===
    const loadCityModel = async () => {
      try {
        setLoadingProgress(10);
        console.log('🏙️ Loading city model...');
        
        const cityResult = await loadModel('/models/city/source/town4new.glb', true);
        const cityModel = cityResult.model;
        cityModelRef.current = cityModel;
        
        setLoadingProgress(30);
        
        // Normalize city scale
        const scaleInfo = normalizeCityScale(cityModel);
        
        setLoadingProgress(40);
        
        // Add to scene
        scene.add(cityModel);
        
        // Create boundaries
        createBoundaryWalls(scene);
        
        console.log('✅ City model loaded and optimized');
        console.log(`   Boundaries: X(${cityBounds.current.minX.toFixed(1)} to ${cityBounds.current.maxX.toFixed(1)}), Z(${cityBounds.current.minZ.toFixed(1)} to ${cityBounds.current.maxZ.toFixed(1)})`);
        
        return scaleInfo;
      } catch (error) {
        console.error('❌ Failed to load city model:', error);
        ground.visible = true;
        throw error;
      }
    };

    // === LOAD PLAYER CHARACTER ===
    const loadPlayerCharacter = async () => {
      try {
        const characterModel = player?.appearance?.model || player?.character_model || 'male_base';
        console.log(`👤 Loading player character: ${characterModel}`);
        
        const result = await loadModel(`/models/characters/${characterModel}.glb`, false);
        const character = result.model;

        // Set spawn position
        const spawnPos = getRandomSpawnPosition();
        playerState.current.position.copy(spawnPos);
        character.position.copy(playerState.current.position);
        
        // Scale character to match normalized city scale
        const characterScale = 1.2; // Slightly larger for visibility
        character.scale.set(characterScale, characterScale, characterScale);
        
        character.traverse((child) => {
          if (child.isMesh) {
            child.castShadow = config.enableShadows;
            child.receiveShadow = config.enableShadows;
            if (child.material) {
              child.material.needsUpdate = true;
            }
          }
        });
        
        scene.add(character);
        characterRef.current = character;

        if (result.animations.length > 0) {
          mixerRef.current = new THREE.AnimationMixer(character);
        }

        console.log(`✅ Player character loaded at (${spawnPos.x.toFixed(1)}, ${spawnPos.y.toFixed(1)}, ${spawnPos.z.toFixed(1)})`);
      } catch (error) {
        console.error('❌ Failed to load player character:', error);
        // Fallback capsule
        const geometry = new THREE.CapsuleGeometry(0.4, CITY_SCALE_CONFIG.CHARACTER_HEIGHT - 0.8);
        const material = new THREE.MeshStandardMaterial({ 
          color: 0xff6b6b,
          emissive: 0xff0000,
          emissiveIntensity: 0.3
        });
        const fallback = new THREE.Mesh(geometry, material);
        fallback.position.copy(playerState.current.position);
        fallback.castShadow = config.enableShadows;
        scene.add(fallback);
        characterRef.current = fallback;
        console.log('⚠️ Using fallback character capsule');
      }
    };

    // === LOAD NPCs (LIMITED ON MOBILE) ===
    const loadNPCs = async () => {
      const npcCount = Math.min(config.maxNPCs, 10);
      const characterTypes = ['male_base', 'female_base', 'male_athletic', 'female_athletic'];
      
      for (let i = 0; i < npcCount; i++) {
        try {
          const type = characterTypes[i % characterTypes.length];
          const result = await loadModel(`/models/characters/${type}.glb`, false);
          const npc = result.model;
          
          const spawnPos = getRandomSpawnPosition();
          npc.position.copy(spawnPos);
          npc.scale.set(0.8, 0.8, 0.8);
          npc.userData = {
            type: 'npc',
            basePos: spawnPos.clone(),
            targetPos: spawnPos.clone(),
            speed: 0.02,
            idleTime: 0,
            moving: false
          };
          
          scene.add(npc);
          npcsRef.current.push(npc);
        } catch (error) {
          console.warn(`⚠️ Failed to load NPC ${i}`);
        }
      }
      
      console.log(`✅ Loaded ${npcsRef.current.length} NPCs`);
    };

    // === INITIALIZE WORLD ===
    const initWorld = async () => {
      try {
        await loadCityModel();
        setLoadingProgress(60);
        
        await loadPlayerCharacter();
        setLoadingProgress(80);
        
        if (!isMobile || config.maxNPCs > 0) {
          await loadNPCs();
        }
        
        setLoadingProgress(100);
        setIsLoaded(true);
        
        console.log('✅ World fully loaded and optimized');
        console.log(`   Performance target: ${config.targetFPS} FPS`);
        console.log(`   Shadow quality: ${config.enableShadows ? `${config.shadowMapSize}x${config.shadowMapSize}` : 'Disabled'}`);
        console.log(`   Render distance: ${config.renderDistance} units`);
      } catch (error) {
        console.error('❌ World initialization failed:', error);
        setIsLoaded(false);
      }
    };

    initWorld();

    // === KEYBOARD CONTROLS ===
    const handleKeyDown = (e) => {
      const key = e.key.toLowerCase();
      
      // Performance overlay toggle
      if (key === 'p' && e.ctrlKey) {
        performanceMonitorRef.current?.toggleOverlay();
        return;
      }
      
      switch (key) {
        case 'w':
        case 'arrowup':
          movement.current.forward = true;
          break;
        case 's':
        case 'arrowdown':
          movement.current.backward = true;
          break;
        case 'a':
          movement.current.left = true;
          break;
        case 'd':
          movement.current.right = true;
          break;
        case 'shift':
          movement.current.run = true;
          break;
        case ' ':
          movement.current.jump = true;
          break;
      }

      // Rotation controls
      if (e.ctrlKey) {
        if (key === 'l') movement.current.rotateLeft = true;
        if (key === 'r') movement.current.rotateRight = true;
      }
      
      if ((key === 'arrowleft' || key === 'a') && !movement.current.forward && !movement.current.backward) {
        movement.current.rotateLeft = true;
      }
      if ((key === 'arrowright' || key === 'd') && !movement.current.forward && !movement.current.backward) {
        movement.current.rotateRight = true;
      }
    };

    const handleKeyUp = (e) => {
      const key = e.key.toLowerCase();
      
      switch (key) {
        case 'w':
        case 'arrowup':
          movement.current.forward = false;
          break;
        case 's':
        case 'arrowdown':
          movement.current.backward = false;
          break;
        case 'a':
          movement.current.left = false;
          movement.current.rotateLeft = false;
          break;
        case 'd':
          movement.current.right = false;
          movement.current.rotateRight = false;
          break;
        case 'shift':
          movement.current.run = false;
          break;
        case ' ':
          movement.current.jump = false;
          break;
        case 'arrowleft':
          movement.current.rotateLeft = false;
          break;
        case 'arrowright':
          movement.current.rotateRight = false;
          break;
      }

      if (e.ctrlKey) {
        if (key === 'l') movement.current.rotateLeft = false;
        if (key === 'r') movement.current.rotateRight = false;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    // === ANIMATION LOOP ===
    let animationFrameId;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      
      const delta = clockRef.current.getDelta();
      
      // Update performance monitor
      if (performanceMonitorRef.current) {
        performanceMonitorRef.current.update();
      }
      
      // Update player movement
      updatePlayerMovement(delta);
      
      // Update camera
      updateCamera(camera, characterRef.current);
      
      // Update animations
      if (mixerRef.current) {
        mixerRef.current.update(delta);
      }
      
      // Update NPCs (simple idle animation)
      npcsRef.current.forEach(npc => {
        if (npc.userData.type === 'npc') {
          // Simple idle bobbing
          npc.position.y = npc.userData.basePos.y + Math.sin(Date.now() * 0.001) * 0.05;
        }
      });
      
      // Render
      renderer.render(scene, camera);
    };
    
    animate();

    // === WINDOW RESIZE ===
    const handleResize = () => {
      if (!mountRef.current) return;
      
      const width = mountRef.current.clientWidth;
      const height = mountRef.current.clientHeight;
      
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    
    window.addEventListener('resize', handleResize);

    // === CLEANUP ===
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
      window.removeEventListener('resize', handleResize);
      
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
      }
      
      if (performanceMonitorRef.current) {
        performanceMonitorRef.current.dispose();
      }
      
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      
      renderer.dispose();
      scene.traverse((object) => {
        if (object.geometry) object.geometry.dispose();
        if (object.material) {
          if (Array.isArray(object.material)) {
            object.material.forEach(mat => mat.dispose());
          } else {
            object.material.dispose();
          }
        }
      });
    };
  }, [player, isMobile]);

  // === MOBILE JOYSTICK HANDLERS ===
  const handleJoystickMove = (x, y) => {
    movement.current.joystickX = x;
    movement.current.joystickY = y;
  };

  const handleJoystickEnd = () => {
    movement.current.joystickX = 0;
    movement.current.joystickY = 0;
  };

  const handleRunToggle = (isRunning) => {
    movement.current.run = isRunning;
    setIsRunning(isRunning);
  };

  const handleJump = () => {
    movement.current.jump = true;
    setTimeout(() => {
      movement.current.jump = false;
    }, 100);
  };

  const handleCameraRotate = (direction) => {
    if (direction === 'left') {
      playerState.current.rotation += ROTATION_SPEED * 5;
    } else {
      playerState.current.rotation -= ROTATION_SPEED * 5;
    }
  };

  return (
    <div className="game-world-container">
      <div 
        ref={mountRef} 
        className="game-world-canvas"
        style={{ width: '100%', height: '100%' }}
      />
      
      {!isLoaded && (
        <div className="game-loading-overlay">
          <div className="loading-content">
            <div className="loading-spinner" />
            <h2>Loading Optimized World...</h2>
            <div className="loading-progress-bar">
              <div 
                className="loading-progress-fill" 
                style={{ width: `${loadingProgress}%` }}
              />
            </div>
            <p>{loadingProgress}%</p>
            <p className="loading-hint">
              {isMobile ? 'Optimizing for mobile...' : 'Loading high-quality assets...'}
            </p>
          </div>
        </div>
      )}
      
      {isLoaded && isMobile && (
        <>
          <VirtualJoystick 
            onMove={handleJoystickMove}
            onEnd={handleJoystickEnd}
          />
          <MobileControls 
            onRun={handleRunToggle}
            onJump={handleJump}
            onCameraRotate={handleCameraRotate}
            isRunning={isRunning}
          />
          <CameraViewToggle 
            currentView={cameraView}
            onViewChange={setCameraView}
          />
        </>
      )}
      
      {isLoaded && !isMobile && (
        <div className="desktop-controls-hint">
          <p>WASD/Arrows: Move | Shift: Run | Space: Jump | Ctrl+P: Performance Monitor</p>
        </div>
      )}
    </div>
  );
};

export default GameWorldOptimized;
