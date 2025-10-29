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

    // === GROUND (Grass Areas) ===
    const groundGeometry = new THREE.PlaneGeometry(300, 300);
    const groundMaterial = new THREE.MeshStandardMaterial({
      color: 0x2d5016,
      roughness: 0.9
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    // === ROADS SYSTEM ===
    const createRoad = (x, z, width, length, rotation = 0) => {
      const roadGeometry = new THREE.PlaneGeometry(width, length);
      const roadMaterial = new THREE.MeshStandardMaterial({
        color: 0x3a3a3a,
        roughness: 0.95
      });
      const road = new THREE.Mesh(roadGeometry, roadMaterial);
      road.rotation.x = -Math.PI / 2;
      road.rotation.z = rotation;
      road.position.set(x, 0.02, z);
      road.receiveShadow = true;
      scene.add(road);

      // Add road markings
      const markingGeometry = new THREE.PlaneGeometry(width * 0.1, length * 0.9);
      const markingMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });
      const marking = new THREE.Mesh(markingGeometry, markingMaterial);
      marking.rotation.x = -Math.PI / 2;
      marking.rotation.z = rotation;
      marking.position.set(x, 0.03, z);
      scene.add(marking);
    };

    // Create grid of roads (city layout)
    const roadWidth = 6;
    const blockSize = 25;
    const citySize = 6; // 6x6 grid of blocks

    // Horizontal roads
    for (let i = -citySize; i <= citySize; i++) {
      createRoad(0, i * blockSize, blockSize * citySize * 2, roadWidth);
    }

    // Vertical roads
    for (let i = -citySize; i <= citySize; i++) {
      createRoad(i * blockSize, 0, roadWidth, blockSize * citySize * 2, Math.PI / 2);
    }

    // === LOAD 40 BUILDINGS ===
    const loadBuildings = async () => {
      const buildingTypes = ['tower', 'shop', 'warehouse', 'headquarters'];
      const buildingModels = {};

      // Pre-load building models
      for (const type of buildingTypes) {
        try {
          const result = await loadModel(`/models/environment/buildings/${type}.glb`);
          buildingModels[type] = result.model;
          console.log(`✅ Building template loaded: ${type}`);
        } catch (error) {
          console.warn(`⚠️ Failed to load ${type}, using fallback`);
          // Create fallback procedural building
          const height = 10 + Math.random() * 20;
          const geometry = new THREE.BoxGeometry(8, height, 8);
          const material = new THREE.MeshStandardMaterial({
            color: new THREE.Color().setHSL(Math.random(), 0.3, 0.5)
          });
          const fallback = new THREE.Mesh(geometry, material);
          fallback.position.y = height / 2;
          buildingModels[type] = fallback;
        }
      }

      // Place 40 buildings in city blocks
      let buildingCount = 0;
      const positions = [];

      for (let x = -citySize + 1; x < citySize; x++) {
        for (let z = -citySize + 1; z < citySize; z++) {
          if (buildingCount >= 40) break;

          // Skip center block (player spawn area)
          if (x === 0 && z === 0) continue;

          const baseX = x * blockSize;
          const baseZ = z * blockSize;

          // Random offset within block
          const offsetX = (Math.random() - 0.5) * 8;
          const offsetZ = (Math.random() - 0.5) * 8;

          positions.push({
            x: baseX + offsetX,
            z: baseZ + offsetZ,
            type: buildingTypes[buildingCount % buildingTypes.length],
            rotation: Math.random() * Math.PI * 2,
            scale: 1.5 + Math.random() * 1.5
          });

          buildingCount++;
        }
        if (buildingCount >= 40) break;
      }

      // Place buildings
      positions.forEach((pos, index) => {
        const building = buildingModels[pos.type].clone();
        building.position.set(pos.x, 0, pos.z);
        building.rotation.y = pos.rotation;
        building.scale.multiplyScalar(pos.scale);
        building.userData = { type: 'building', name: `Building ${index + 1}` };
        scene.add(building);
      });

      console.log(`✅ ${positions.length} buildings placed`);
    };

    // === LOAD VEHICLES (TRAFFIC) ===
    const loadVehicles = async () => {
      try {
        const vehicleResult = await loadModel('/models/environment/props/vehicle.glb');
        const vehicleModel = vehicleResult.model;

        // Place vehicles on roads
        for (let i = 0; i < 15; i++) {
          const vehicle = vehicleModel.clone();
          const roadIndex = Math.floor(Math.random() * (citySize * 2));
          const isHorizontal = Math.random() > 0.5;

          if (isHorizontal) {
            vehicle.position.set(
              (Math.random() - 0.5) * blockSize * citySize * 2,
              0.2,
              (roadIndex - citySize) * blockSize
            );
            vehicle.rotation.y = Math.random() > 0.5 ? 0 : Math.PI;
          } else {
            vehicle.position.set(
              (roadIndex - citySize) * blockSize,
              0.2,
              (Math.random() - 0.5) * blockSize * citySize * 2
            );
            vehicle.rotation.y = Math.random() > 0.5 ? Math.PI / 2 : -Math.PI / 2;
          }

          vehicle.scale.set(1.2, 1.2, 1.2);
          vehicle.userData = { type: 'vehicle', speed: 0.05 + Math.random() * 0.1 };
          scene.add(vehicle);
          npcsRef.current.push(vehicle);
        }

        console.log('✅ Vehicles placed');
      } catch (error) {
        console.warn('⚠️ Failed to load vehicles');
      }
    };

    // === LOAD CONTAINERS (PROPS) ===
    const loadProps = async () => {
      try {
        const containerResult = await loadModel('/models/environment/props/container.glb');
        const platformResult = await loadModel('/models/environment/terrain/platform.glb');

        // Place containers randomly
        for (let i = 0; i < 10; i++) {
          const container = containerResult.model.clone();
          container.position.set(
            (Math.random() - 0.5) * 100,
            0,
            (Math.random() - 0.5) * 100
          );
          container.rotation.y = Math.random() * Math.PI * 2;
          container.scale.set(0.8, 0.8, 0.8);
          scene.add(container);
        }

        // Place platforms
        for (let i = 0; i < 8; i++) {
          const platform = platformResult.model.clone();
          platform.position.set(
            (Math.random() - 0.5) * 120,
            0,
            (Math.random() - 0.5) * 120
          );
          platform.scale.set(2, 1, 2);
          scene.add(platform);
        }

        console.log('✅ Props placed');
      } catch (error) {
        console.warn('⚠️ Failed to load props');
      }
    };

    // === LOAD PLAYER CHARACTER ===
    const loadPlayerCharacter = async () => {
      try {
        const characterModel = player?.character_model || 'male_base';
        const result = await loadModel(`/models/characters/${characterModel}.glb`);
        const character = result.model;

        character.position.copy(playerState.current.position);
        character.scale.set(1, 1, 1);
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
        try {
          const type = characterTypes[i % characterTypes.length];
          const result = await loadModel(`/models/characters/${type}.glb`);
          const npc = result.model;

          npc.position.set(
            (Math.random() - 0.5) * 80,
            1,
            (Math.random() - 0.5) * 80
          );
          npc.scale.set(1, 1, 1);
          npc.userData = {
            type: 'npc_character',
            name: `Citizen ${i + 1}`,
            basePos: npc.position.clone(),
            targetPos: npc.position.clone(),
            speed: 0.03 + Math.random() * 0.02,
            idleTime: 0,
            moving: false
          };

          scene.add(npc);
          npcsRef.current.push(npc);
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
      await loadBuildings();
      setLoadingProgress(30);
      await loadVehicles();
      setLoadingProgress(45);
      await loadProps();
      setLoadingProgress(60);
      await loadPlayerCharacter();
      setLoadingProgress(75);
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
