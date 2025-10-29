import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import './GameWorld.css';

/**
 * Enhanced 3D Game World - Super City with 40+ Buildings
 * Features: Running animations, roads, vehicles, AI NPCs, Ctrl+L/R controls
 */
const GameWorldEnhanced = ({ player, isFullscreen = false }) => {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const rendererRef = useRef(null);
  const characterRef = useRef(null);
  const npcsRef = useRef([]);
  const mixerRef = useRef(null);
  const clockRef = useRef(new THREE.Clock());
  const [isLoaded, setIsLoaded] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(0);

  // Movement state
  const movement = useRef({
    forward: false,
    backward: false,
    left: false,
    right: false,
    jump: false,
    run: false,
    rotateLeft: false,
    rotateRight: false
  });

  const playerState = useRef({
    position: new THREE.Vector3(0, 1, 0),
    rotation: 0,
    velocity: new THREE.Vector3(),
    isGrounded: true,
    currentAnimation: 'idle'
  });

  // City boundaries (to be calculated after loading city model)
  const cityBounds = useRef({
    minX: -50,
    maxX: 50,
    minZ: -50,
    maxZ: 50,
    minY: 0,
    maxY: 20
  });

  // Constants
  const WALK_SPEED = 0.1;
  const RUN_SPEED = 0.25;
  const ROTATION_SPEED = 0.05;
  const JUMP_FORCE = 0.3;
  const GRAVITY = 0.015;

  // Helper: Load GLB model
  const loadModel = (path) => {
    return new Promise((resolve, reject) => {
      const loader = new GLTFLoader();
      loader.load(
        path,
        (gltf) => {
          const model = gltf.scene;
          model.traverse((child) => {
            if (child.isMesh) {
              child.castShadow = true;
              child.receiveShadow = true;
            }
          });
          resolve({ model, animations: gltf.animations || [] });
        },
        (progress) => {
          const percent = (progress.loaded / progress.total) * 100;
          setLoadingProgress(Math.round(percent));
        },
        reject
      );
    });
  };

  useEffect(() => {
    if (!mountRef.current) return;

    // === SCENE SETUP ===
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB); // Sky blue
    scene.fog = new THREE.Fog(0x87CEEB, 50, 200);
    sceneRef.current = scene;

    // === CAMERA ===
    const camera = new THREE.PerspectiveCamera(
      75,
      mountRef.current.clientWidth / mountRef.current.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 10, 15);
    cameraRef.current = camera;

    // === RENDERER ===
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    mountRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // === LIGHTING ===
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(50, 100, 50);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    directionalLight.shadow.camera.near = 0.5;
    directionalLight.shadow.camera.far = 500;
    directionalLight.shadow.camera.left = -100;
    directionalLight.shadow.camera.right = 100;
    directionalLight.shadow.camera.top = 100;
    directionalLight.shadow.camera.bottom = -100;
    scene.add(directionalLight);

    // === GROUND (Fallback - city model includes ground) ===
    const groundGeometry = new THREE.PlaneGeometry(300, 300);
    const groundMaterial = new THREE.MeshStandardMaterial({
      color: 0x2d5016,
      roughness: 0.9
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    ground.visible = false; // Hidden by default, city model has ground
    scene.add(ground);

    // === CITY MODEL FUNCTIONS ===
    
    // Get random spawn position within city bounds
    const getRandomSpawnPosition = () => {
      const bounds = cityBounds.current;
      const margin = 10; // Keep away from edges
      
      return new THREE.Vector3(
        bounds.minX + margin + Math.random() * (bounds.maxX - bounds.minX - margin * 2),
        1, // Ground level with character height offset
        bounds.minZ + margin + Math.random() * (bounds.maxZ - bounds.minZ - margin * 2)
      );
    };

    // Create invisible boundary walls
    const createBoundaryWalls = () => {
      const wallHeight = 100;
      const wallMaterial = new THREE.MeshBasicMaterial({ 
        transparent: true, 
        opacity: 0,
        side: THREE.DoubleSide
      });
      
      const bounds = cityBounds.current;
      const width = bounds.maxX - bounds.minX;
      const depth = bounds.maxZ - bounds.minZ;
      
      // North wall
      const northWall = new THREE.Mesh(
        new THREE.PlaneGeometry(width, wallHeight),
        wallMaterial
      );
      northWall.position.set((bounds.minX + bounds.maxX) / 2, wallHeight / 2, bounds.maxZ);
      northWall.userData.isBoundary = true;
      scene.add(northWall);
      
      // South wall
      const southWall = new THREE.Mesh(
        new THREE.PlaneGeometry(width, wallHeight),
        wallMaterial
      );
      southWall.position.set((bounds.minX + bounds.maxX) / 2, wallHeight / 2, bounds.minZ);
      southWall.rotation.y = Math.PI;
      southWall.userData.isBoundary = true;
      scene.add(southWall);
      
      // East wall
      const eastWall = new THREE.Mesh(
        new THREE.PlaneGeometry(depth, wallHeight),
        wallMaterial
      );
      eastWall.position.set(bounds.maxX, wallHeight / 2, (bounds.minZ + bounds.maxZ) / 2);
      eastWall.rotation.y = Math.PI / 2;
      eastWall.userData.isBoundary = true;
      scene.add(eastWall);
      
      // West wall
      const westWall = new THREE.Mesh(
        new THREE.PlaneGeometry(depth, wallHeight),
        wallMaterial
      );
      westWall.position.set(bounds.minX, wallHeight / 2, (bounds.minZ + bounds.maxZ) / 2);
      westWall.rotation.y = -Math.PI / 2;
      westWall.userData.isBoundary = true;
      scene.add(westWall);
      
      console.log('✅ Boundary walls created');
    };

    // Load city model
    const loadCityModel = async () => {
      try {
        console.log('🔄 Loading city model...');
        const cityResult = await loadModel('/models/city/source/town4new.glb');
        const cityModel = cityResult.model;
        
        // Position city at origin
        cityModel.position.set(0, 0, 0);
        scene.add(cityModel);
        
        // Calculate bounding box for city boundaries
        const box = new THREE.Box3().setFromObject(cityModel);
        const size = new THREE.Vector3();
        box.getSize(size);
        const center = new THREE.Vector3();
        box.getCenter(center);
        
        // Set city boundaries with padding
        const padding = 5;
        cityBounds.current = {
          minX: box.min.x - padding,
          maxX: box.max.x + padding,
          minZ: box.min.z - padding,
          maxZ: box.max.z + padding,
          minY: 0,
          maxY: box.max.y + 10
        };
        
        console.log('✅ City model loaded');
        console.log(`📐 City bounds: X(${cityBounds.current.minX.toFixed(1)} to ${cityBounds.current.maxX.toFixed(1)}), Z(${cityBounds.current.minZ.toFixed(1)} to ${cityBounds.current.maxZ.toFixed(1)})`);
        
        // Create invisible boundary walls
        createBoundaryWalls();
        
        return { size, center };
      } catch (error) {
        console.error('❌ Failed to load city model:', error);
        // Show fallback ground if city fails
        ground.visible = true;
        throw error;
      }
    };

    // === OLD LOADING FUNCTIONS REMOVED === 
    // These are no longer needed as we now use a single city model
    const loadBuildings = async () => { console.log('⏭️ Skipping old buildings - using city model'); };
    const loadVehicles = async () => { console.log('⏭️ Skipping old vehicles - city model includes environment'); };
    const loadProps = async () => { console.log('⏭️ Skipping old props - city model includes environment'); };

    // === LOAD PLAYER CHARACTER ===
    const loadPlayerCharacter = async () => {
      try {
        const characterModel = player?.character_model || 'male_base';
        const result = await loadModel(`/models/characters/${characterModel}.glb`);
        const character = result.model;

        // Set random spawn position
        const spawnPos = getRandomSpawnPosition();
        playerState.current.position.copy(spawnPos);
        character.position.copy(playerState.current.position);
        character.scale.set(1, 1, 1);
        
        console.log(`👤 Player spawned at (${spawnPos.x.toFixed(1)}, ${spawnPos.z.toFixed(1)})`);
        
        scene.add(character);
        characterRef.current = character;

        // Setup animation mixer
        if (result.animations.length > 0) {
          mixerRef.current = new THREE.AnimationMixer(character);
        }

        console.log('✅ Player character loaded');
      } catch (error) {
        console.error('❌ Failed to load player character:', error);
        // Fallback cube
        const geometry = new THREE.CapsuleGeometry(0.5, 1.5);
        const material = new THREE.MeshStandardMaterial({ color: 0x00ff88 });
        const fallback = new THREE.Mesh(geometry, material);
        fallback.position.copy(playerState.current.position);
        scene.add(fallback);
        characterRef.current = fallback;
      }
    };

    // === LOAD NPC CHARACTERS ===
    const loadNPCCharacters = async () => {
      const characterTypes = [
        'male_base', 'male_athletic', 'male_heavy',
        'female_base', 'female_athletic', 'female_heavy'
      ];

      for (let i = 0; i < 10; i++) {
        const spawnPos = getRandomSpawnPosition();
        
        try {
          const type = characterTypes[i % characterTypes.length];
          const result = await loadModel(`/models/characters/${type}.glb`);
          const npc = result.model;

          npc.position.copy(spawnPos);
          npc.scale.set(1, 1, 1);
          npc.userData = {
            type: 'npc_character',
            name: `Citizen ${i + 1}`,
            basePos: spawnPos.clone(),
            targetPos: spawnPos.clone(),
            speed: 0.03 + Math.random() * 0.02,
            idleTime: 0,
            moving: false
          };

          scene.add(npc);
          npcsRef.current.push(npc);
          console.log(`✅ NPC ${i+1} spawned at (${spawnPos.x.toFixed(1)}, ${spawnPos.z.toFixed(1)})`);
        } catch (error) {
          console.warn(`⚠️ Failed to load NPC character ${i}`);
        }
      }

      console.log(`✅ NPC characters loaded`);
    };

    // === LOAD ROBOT NPCs ===
    const loadRobotNPCs = async () => {
      const robotTypes = [
        'scout', 'trader', 'medic', 'combat', 'hacker', 
        'guardian', 'assault', 'tactical', 'harvester'
      ];

      for (let i = 0; i < robotTypes.length; i++) {
        try {
          const result = await loadModel(`/models/robots/${robotTypes[i]}.glb`);
          const robot = result.model;

          robot.position.set(
            (Math.random() - 0.5) * 100,
            0,
            (Math.random() - 0.5) * 100
          );
          robot.scale.set(1.2, 1.2, 1.2);
          robot.userData = {
            type: 'robot',
            name: `${robotTypes[i].toUpperCase()}-${String(i).padStart(2, '0')}`,
            basePos: robot.position.clone(),
            targetPos: robot.position.clone(),
            speed: 0.05 + Math.random() * 0.03,
            idleTime: 0,
            moving: false,
            patrolRadius: 20
          };

          scene.add(robot);
          npcsRef.current.push(robot);
        } catch (error) {
          console.warn(`⚠️ Failed to load robot ${robotTypes[i]}`);
        }
      }

      console.log(`✅ Robot NPCs loaded`);
    };

    // === INITIALIZE WORLD ===
    const initWorld = async () => {
      setLoadingProgress(10);
      await loadCityModel();
      setLoadingProgress(40);
      await loadPlayerCharacter();
      setLoadingProgress(70);
      await loadNPCCharacters();
      setLoadingProgress(90);
      await loadRobotNPCs();
      setLoadingProgress(100);
      setIsLoaded(true);
      console.log('✅ World fully loaded');
    };

    initWorld();

    // === KEYBOARD CONTROLS ===
    const handleKeyDown = (e) => {
      switch (e.key.toLowerCase()) {
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
        case 'control':
          if (e.key === 'Control') {
            // Next keypress will be L or R
          }
          break;
      }

      // Ctrl+L and Ctrl+R for rotation
      if (e.ctrlKey) {
        if (e.key.toLowerCase() === 'l') {
          movement.current.rotateLeft = true;
        } else if (e.key.toLowerCase() === 'r') {
          movement.current.rotateRight = true;
        }
      }

      // Arrow keys for rotation when NOT moving
      if (e.key === 'ArrowLeft' && !movement.current.forward && !movement.current.backward) {
        movement.current.rotateLeft = true;
      } else if (e.key === 'ArrowRight' && !movement.current.forward && !movement.current.backward) {
        movement.current.rotateRight = true;
      }
    };

    const handleKeyUp = (e) => {
      switch (e.key.toLowerCase()) {
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
          break;
        case 'd':
          movement.current.right = false;
          break;
        case 'shift':
          movement.current.run = false;
          break;
        case ' ':
          movement.current.jump = false;
          break;
      }

      if (e.key === 'ArrowLeft') {
        movement.current.rotateLeft = false;
      } else if (e.key === 'ArrowRight') {
        movement.current.rotateRight = false;
      }

      if (e.key.toLowerCase() === 'l' || e.key.toLowerCase() === 'r') {
        movement.current.rotateLeft = false;
        movement.current.rotateRight = false;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    // === NPC AI MOVEMENT ===
    const updateNPCMovement = (npc, deltaTime) => {
      if (!npc.userData || npc.userData.type === 'building') return;

      const data = npc.userData;

      if (!data.moving) {
        data.idleTime += deltaTime;
        if (data.idleTime > 3 + Math.random() * 4) {
          data.moving = true;
          data.idleTime = 0;

          // Set new random target
          const angle = Math.random() * Math.PI * 2;
          const distance = 10 + Math.random() * (data.patrolRadius || 15);
          data.targetPos = new THREE.Vector3(
            data.basePos.x + Math.cos(angle) * distance,
            data.basePos.y,
            data.basePos.z + Math.sin(angle) * distance
          );
        }
      } else {
        // Move toward target
        const direction = new THREE.Vector3()
          .subVectors(data.targetPos, npc.position)
          .normalize();

        npc.position.add(direction.multiplyScalar(data.speed));

        // Rotate to face direction
        const targetAngle = Math.atan2(direction.x, direction.z);
        npc.rotation.y = targetAngle;

        // Check if reached target
        if (npc.position.distanceTo(data.targetPos) < 0.5) {
          data.moving = false;
        }
      }
    };

    // === ANIMATION LOOP ===
    const animate = () => {
      requestAnimationFrame(animate);

      const delta = clockRef.current.getDelta();
      const deltaMs = delta * 1000;

      // Update animation mixer
      if (mixerRef.current) {
        mixerRef.current.update(delta);
      }

      // Update NPCs
      npcsRef.current.forEach(npc => {
        updateNPCMovement(npc, deltaMs);
      });

      // Player movement
      if (characterRef.current) {
        const speed = movement.current.run ? RUN_SPEED : WALK_SPEED;
        const state = playerState.current;
        const bounds = cityBounds.current;
        let isMoving = false;

        // Forward/Backward
        if (movement.current.forward) {
          state.position.x += Math.sin(state.rotation) * speed;
          state.position.z += Math.cos(state.rotation) * speed;
          isMoving = true;
        }
        if (movement.current.backward) {
          state.position.x -= Math.sin(state.rotation) * speed;
          state.position.z -= Math.cos(state.rotation) * speed;
          isMoving = true;
        }

        // Strafe
        if (movement.current.left) {
          state.position.x -= Math.cos(state.rotation) * speed;
          state.position.z += Math.sin(state.rotation) * speed;
          isMoving = true;
        }
        if (movement.current.right) {
          state.position.x += Math.cos(state.rotation) * speed;
          state.position.z -= Math.sin(state.rotation) * speed;
          isMoving = true;
        }

        // Apply boundary constraints
        state.position.x = Math.max(bounds.minX + 1, Math.min(bounds.maxX - 1, state.position.x));
        state.position.z = Math.max(bounds.minZ + 1, Math.min(bounds.maxZ - 1, state.position.z));

        // Rotation (Ctrl+L / Ctrl+R or Arrow keys)
        if (movement.current.rotateLeft) {
          state.rotation += ROTATION_SPEED;
        }
        if (movement.current.rotateRight) {
          state.rotation -= ROTATION_SPEED;
        }

        // Jump
        if (movement.current.jump && state.isGrounded) {
          state.velocity.y = JUMP_FORCE;
          state.isGrounded = false;
        }

        // Apply gravity
        if (!state.isGrounded) {
          state.velocity.y -= GRAVITY;
          state.position.y += state.velocity.y;

          if (state.position.y <= 1) {
            state.position.y = 1;
            state.velocity.y = 0;
            state.isGrounded = true;
          }
        }

        // Update character
        characterRef.current.position.copy(state.position);
        characterRef.current.rotation.y = state.rotation;

        // Update animation state
        const newAnim = !state.isGrounded ? 'jump' 
          : isMoving ? (movement.current.run ? 'run' : 'walk')
          : 'idle';

        if (newAnim !== state.currentAnimation) {
          state.currentAnimation = newAnim;
          // Play animation if available
        }

        // Camera follow
        const cameraOffset = new THREE.Vector3(
          -Math.sin(state.rotation) * 10,
          8,
          -Math.cos(state.rotation) * 10
        );
        cameraRef.current.position.copy(state.position).add(cameraOffset);
        cameraRef.current.lookAt(state.position);
      }

      renderer.render(scene, camera);
    };

    animate();

    // === CLEANUP ===
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, [player]);

  return (
    <div 
      ref={mountRef} 
      className={`game-world ${isFullscreen ? 'fullscreen' : ''}`}
      style={{ width: '100%', height: '100%', position: 'relative' }}
    >
      {!isLoaded && (
        <div className="loading-overlay">
          <div className="loading-content">
            <div className="loading-spinner"></div>
            <h2>Loading Super City...</h2>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${loadingProgress}%` }}></div>
            </div>
            <p>{loadingProgress}% Complete</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameWorldEnhanced;
