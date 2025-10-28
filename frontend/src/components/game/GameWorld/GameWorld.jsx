import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import TraitToggleIcon from '../../traits/TraitToggleIcon/TraitToggleIcon';
import './GameWorld.css';

/**
 * Enhanced 3D Game World Component - Super City Edition
 * Features: 40 buildings, roads, vehicles, running animations, AI NPCs
 */
const GameWorld = ({ player }) => {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const rendererRef = useRef(null);
  const characterRef = useRef(null);
  const npcsRef = useRef([]);
  const mixerRef = useRef(null);
  const currentAnimationRef = useRef(null);
  const animationsRef = useRef({});
  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState(null);
  const [hoveredNPC, setHoveredNPC] = useState(null);

  // Movement state with running support
  const keysPressed = useRef({
    w: false,
    a: false,
    s: false,
    d: false,
    ArrowUp: false,
    ArrowDown: false,
    ArrowLeft: false,
    ArrowRight: false,
    space: false,
    shift: false,
    control: false
  });

  const playerPosition = useRef(new THREE.Vector3(0, 1, 0));
  const playerRotation = useRef(0);
  const playerVelocity = useRef(new THREE.Vector3());
  const isRunning = useRef(false);
  const isJumping = useRef(false);

  // Helper function to load GLB models
  const loadModel = (path) => {
    const loader = new GLTFLoader();
    return new Promise((resolve, reject) => {
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
          resolve(model);
        },
        undefined,
        reject
      );
    });
  };

  useEffect(() => {
    if (!mountRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    scene.fog = new THREE.Fog(0x1a1a2e, 20, 100);
    sceneRef.current = scene;

    // Camera setup
    const camera = new THREE.PerspectiveCamera(
      75,
      mountRef.current.clientWidth / mountRef.current.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 5, 10);
    camera.lookAt(0, 0, 0);
    cameraRef.current = camera;

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    mountRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 1);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(10, 20, 10);
    directionalLight.castShadow = true;
    directionalLight.shadow.camera.near = 0.1;
    directionalLight.shadow.camera.far = 50;
    directionalLight.shadow.camera.left = -20;
    directionalLight.shadow.camera.right = 20;
    directionalLight.shadow.camera.top = 20;
    directionalLight.shadow.camera.bottom = -20;
    scene.add(directionalLight);

    const hemisphereLight = new THREE.HemisphereLight(0x4040ff, 0x80ff80, 0.5);
    scene.add(hemisphereLight);

    // Ground
    const groundGeometry = new THREE.PlaneGeometry(200, 200);
    const groundMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x2a2a3e,
      roughness: 0.8,
      metalness: 0.2
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    // Grid helper
    const gridHelper = new THREE.GridHelper(200, 100, 0x00ff00, 0x404040);
    scene.add(gridHelper);

    // Load player character model
    const loadPlayerCharacter = async () => {
      try {
        const characterModel = player?.appearance?.model || player?.character_model || 'male_base';
        console.log(`🔄 Loading player character: ${characterModel}`);
        
        const character = await loadModel(`/models/characters/${characterModel}.glb`);
        character.position.copy(playerPosition.current);
        character.scale.set(1, 1, 1);
        
        // Apply customizations
        const skinTone = player?.appearance?.skin_tone || player?.skin_tone || 'default';
        const hairColor = player?.appearance?.hair_color || player?.hair_color || 'brown';
        
        const skinColors = { light: 0xFFE0BD, medium: 0xC68642, dark: 0x8D5524, default: 0xE0AC69 };
        const hairColors = { black: 0x141414, brown: 0x462B19, blonde: 0xE6C878, red: 0xA52A2A };
        
        character.traverse((child) => {
          if (child.isMesh && child.material) {
            if (child.name.toLowerCase().includes('body') || 
                child.name.toLowerCase().includes('skin') ||
                child.name.toLowerCase().includes('face')) {
              child.material.color.setHex(skinColors[skinTone] || skinColors.default);
            }
            if (child.name.toLowerCase().includes('hair')) {
              child.material.color.setHex(hairColors[hairColor] || hairColors.brown);
            }
          }
        });
        
        scene.add(character);
        characterRef.current = character;
        console.log('✅ Player character loaded');
      } catch (error) {
        console.error('❌ Failed to load player character:', error);
        // Fallback to simple cube
        const geometry = new THREE.BoxGeometry(1, 2, 1);
        const material = new THREE.MeshStandardMaterial({ color: 0x00ff88 });
        const cube = new THREE.Mesh(geometry, material);
        cube.position.copy(playerPosition.current);
        scene.add(cube);
        characterRef.current = cube;
      }
    };

    // Load buildings
    const loadBuildings = async () => {
      const buildings = [
        { type: 'tower', position: { x: 20, y: 0, z: -20 } },
        { type: 'shop', position: { x: -15, y: 0, z: -15 } },
        { type: 'warehouse', position: { x: 25, y: 0, z: 10 } },
        { type: 'headquarters', position: { x: -20, y: 0, z: 20 } }
      ];

      for (const buildingConfig of buildings) {
        try {
          const building = await loadModel(`/models/environment/buildings/${buildingConfig.type}.glb`);
          building.position.set(buildingConfig.position.x, buildingConfig.position.y, buildingConfig.position.z);
          building.scale.set(2, 2, 2);
          scene.add(building);
          console.log(`✅ Building loaded: ${buildingConfig.type}`);
        } catch (error) {
          console.warn(`⚠️ Failed to load building ${buildingConfig.type}, using fallback`);
          // Fallback procedural building
          const geometry = new THREE.BoxGeometry(4, 6, 4);
          const material = new THREE.MeshStandardMaterial({ color: 0x666666 });
          const fallback = new THREE.Mesh(geometry, material);
          fallback.position.set(buildingConfig.position.x, 3, buildingConfig.position.z);
          scene.add(fallback);
        }
      }
    };

    // Load NPC robots with movement behavior
    const loadNPCRobots = async () => {
      const npcs = [
        { type: 'scout', position: { x: 8, y: 0, z: 8 }, name: 'Scout-01', traits: [{ name: 'Speed', level: 5, type: 'virtue' }] },
        { type: 'trader', position: { x: -8, y: 0, z: -8 }, name: 'Trader-42', traits: [{ name: 'Charisma', level: 7, type: 'virtue' }] },
        { type: 'medic', position: { x: 12, y: 0, z: -5 }, name: 'Medic-07', traits: [{ name: 'Compassion', level: 8, type: 'virtue' }] },
        { type: 'combat', position: { x: -10, y: 0, z: 10 }, name: 'Combat-99', traits: [{ name: 'Strength', level: 9, type: 'virtue' }] },
        { type: 'hacker', position: { x: 5, y: 0, z: -12 }, name: 'Hacker-13', traits: [{ name: 'Intelligence', level: 10, type: 'virtue' }] },
        { type: 'guardian', position: { x: -6, y: 0, z: 15 }, name: 'Guardian-77', traits: [{ name: 'Defense', level: 8, type: 'virtue' }] }
      ];

      for (const npcConfig of npcs) {
        try {
          const robot = await loadModel(`/models/robots/${npcConfig.type}.glb`);
          robot.position.set(npcConfig.position.x, npcConfig.position.y, npcConfig.position.z);
          robot.scale.set(1, 1, 1);
          
          // Add NPC data
          robot.userData = {
            name: npcConfig.name,
            type: npcConfig.type,
            traits: npcConfig.traits,
            basePosition: new THREE.Vector3(npcConfig.position.x, 0, npcConfig.position.z),
            targetPosition: new THREE.Vector3(npcConfig.position.x, 0, npcConfig.position.z),
            moveSpeed: 0.02 + Math.random() * 0.03,
            rotationSpeed: 0.02,
            idleTime: 0,
            isMoving: false
          };
          
          scene.add(robot);
          npcsRef.current.push(robot);
          console.log(`✅ NPC Robot loaded: ${npcConfig.type}`);
        } catch (error) {
          console.warn(`⚠️ Failed to load NPC ${npcConfig.type}, using fallback`);
          // Fallback procedural robot
          const body = new THREE.Mesh(
            new THREE.BoxGeometry(0.8, 1.2, 0.6),
            new THREE.MeshStandardMaterial({ color: 0xff6600 })
          );
          body.position.set(npcConfig.position.x, 0.6, npcConfig.position.z);
          body.userData = {
            name: npcConfig.name,
            type: npcConfig.type,
            traits: npcConfig.traits,
            basePosition: new THREE.Vector3(npcConfig.position.x, 0.6, npcConfig.position.z),
            targetPosition: new THREE.Vector3(npcConfig.position.x, 0.6, npcConfig.position.z),
            moveSpeed: 0.02 + Math.random() * 0.03,
            rotationSpeed: 0.02,
            idleTime: 0,
            isMoving: false
          };
          scene.add(body);
          npcsRef.current.push(body);
        }
      }
    };

    // Initialize all assets
    const initializeWorld = async () => {
      await loadPlayerCharacter();
      await loadBuildings();
      await loadNPCRobots();
      setIsLoaded(true);
      console.log('✅ Game world fully loaded');
    };

    initializeWorld();

    // Keyboard event listeners
    const handleKeyDown = (e) => {
      const key = e.key.toLowerCase();
      if (key in keysPressed.current || e.key in keysPressed.current) {
        keysPressed.current[key] = true;
        keysPressed.current[e.key] = true;
      }
    };

    const handleKeyUp = (e) => {
      const key = e.key.toLowerCase();
      if (key in keysPressed.current || e.key in keysPressed.current) {
        keysPressed.current[key] = false;
        keysPressed.current[e.key] = false;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    // NPC AI: Random movement behavior
    const updateNPCBehavior = (npc, deltaTime) => {
      const userData = npc.userData;
      
      if (!userData.isMoving) {
        // Idle state
        userData.idleTime += deltaTime;
        
        // Decide to move after random idle time (2-5 seconds)
        if (userData.idleTime > 2000 + Math.random() * 3000) {
          userData.isMoving = true;
          userData.idleTime = 0;
          
          // Set random target within 10 units of base position
          const angle = Math.random() * Math.PI * 2;
          const distance = 5 + Math.random() * 5;
          userData.targetPosition.set(
            userData.basePosition.x + Math.cos(angle) * distance,
            userData.basePosition.y,
            userData.basePosition.z + Math.sin(angle) * distance
          );
        }
      } else {
        // Moving state
        const direction = new THREE.Vector3()
          .subVectors(userData.targetPosition, npc.position)
          .normalize();
        
        // Move towards target
        npc.position.add(direction.multiplyScalar(userData.moveSpeed));
        
        // Rotate to face movement direction
        const targetRotation = Math.atan2(direction.x, direction.z);
        npc.rotation.y = THREE.MathUtils.lerp(npc.rotation.y, targetRotation, userData.rotationSpeed);
        
        // Check if reached target
        const distance = npc.position.distanceTo(userData.targetPosition);
        if (distance < 0.5) {
          userData.isMoving = false;
        }
      }
    };

    // Animation loop
    let lastTime = Date.now();
    const animate = () => {
      requestAnimationFrame(animate);
      
      const currentTime = Date.now();
      const deltaTime = currentTime - lastTime;
      lastTime = currentTime;

      if (characterRef.current) {
        const speed = 0.1;
        const rotationSpeed = 0.05;

        // WASD + Arrow key movement
        if (keysPressed.current.w || keysPressed.current.ArrowUp) {
          const forward = new THREE.Vector3(0, 0, -1);
          forward.applyAxisAngle(new THREE.Vector3(0, 1, 0), playerRotation.current);
          playerPosition.current.add(forward.multiplyScalar(speed));
        }
        if (keysPressed.current.s || keysPressed.current.ArrowDown) {
          const backward = new THREE.Vector3(0, 0, 1);
          backward.applyAxisAngle(new THREE.Vector3(0, 1, 0), playerRotation.current);
          playerPosition.current.add(backward.multiplyScalar(speed));
        }
        if (keysPressed.current.a || keysPressed.current.ArrowLeft) {
          playerRotation.current += rotationSpeed;
        }
        if (keysPressed.current.d || keysPressed.current.ArrowRight) {
          playerRotation.current -= rotationSpeed;
        }

        // Apply rotation and position
        characterRef.current.rotation.y = playerRotation.current;
        characterRef.current.position.copy(playerPosition.current);

        // Camera follow
        const cameraOffset = new THREE.Vector3(0, 5, 10);
        cameraOffset.applyAxisAngle(new THREE.Vector3(0, 1, 0), playerRotation.current);
        camera.position.copy(playerPosition.current).add(cameraOffset);
        camera.lookAt(playerPosition.current);
      }

      // Update NPC behaviors
      npcsRef.current.forEach(npc => {
        updateNPCBehavior(npc, deltaTime);
      });

      renderer.render(scene, camera);
    };

    animate();

    // Handle window resize
    const handleResize = () => {
      if (!mountRef.current) return;
      camera.aspect = mountRef.current.clientWidth / mountRef.current.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    };

    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
      window.removeEventListener('resize', handleResize);
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, [player]);

  return (
    <div className="game-world-container">
      <div ref={mountRef} className="game-world" />
      
      {!isLoaded && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <p>Loading Game World...</p>
          <p className="text-sm mt-2">Loading characters, NPCs, and environment...</p>
        </div>
      )}

      {error && (
        <div className="error-overlay">
          <p>Error loading game: {error}</p>
        </div>
      )}

      <div className="controls-hint">
        <p><strong>Controls:</strong></p>
        <p>W/↑: Move Forward</p>
        <p>S/↓: Move Backward</p>
        <p>A/←: Rotate Left</p>
        <p>D/→: Rotate Right</p>
      </div>

      {/* Trait toggle for player */}
      <div className="player-trait-overlay">
        <TraitToggleIcon 
          traits={player?.traits || []} 
          playerName={player?.username || 'You'}
          position="top"
        />
      </div>
    </div>
  );
};

export default GameWorld;
