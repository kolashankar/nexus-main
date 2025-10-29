import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import TraitToggleIcon from '../../traits/TraitToggleIcon/TraitToggleIcon';
import { RoadDetector } from '../../../utils/RoadDetector';
import { NavMesh } from '../../../utils/NavMesh';
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
  
  // Road detection and NavMesh
  const roadDetectorRef = useRef(null);
  const navMeshRef = useRef(null);
  const debugVisualsRef = useRef({ roads: null, navMesh: null });
  const [showDebugVisuals, setShowDebugVisuals] = useState(true);

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

  // City boundaries (to be calculated after loading city model)
  const cityBounds = useRef({
    minX: -50,
    maxX: 50,
    minZ: -50,
    maxZ: 50,
    minY: 0,
    maxY: 20
  });

  // Helper function to load GLB models
  const loadModel = (path, includeAnimations = false) => {
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
          if (includeAnimations && gltf.animations && gltf.animations.length > 0) {
            resolve({ model, animations: gltf.animations });
          } else {
            resolve(model);
          }
        },
        undefined,
        reject
      );
    });
  };

  // Load all character animations
  const loadAnimations = async () => {
    const animationTypes = ['idle', 'walk', 'run', 'jump', 'attack', 'defend', 'victory', 'defeat'];
    const loadedAnims = {};
    
    for (const type of animationTypes) {
      try {
        const result = await loadModel(`/models/animations/${type}.glb`, true);
        if (result.animations) {
          loadedAnims[type] = result.animations[0];
          console.log(`✅ Animation loaded: ${type}`);
        }
      } catch (error) {
        console.warn(`⚠️ Failed to load animation: ${type}`);
      }
    }
    
    return loadedAnims;
  };

  // Play animation on character
  const playAnimation = (animName) => {
    if (!mixerRef.current || !animationsRef.current[animName]) return;
    
    if (currentAnimationRef.current) {
      currentAnimationRef.current.fadeOut(0.3);
    }
    
    const action = mixerRef.current.clipAction(animationsRef.current[animName]);
    action.reset().fadeIn(0.3).play();
    currentAnimationRef.current = action;
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

    // Ground (fallback - city model includes ground)
    const groundGeometry = new THREE.PlaneGeometry(200, 200);
    const groundMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x2a2a3e,
      roughness: 0.8,
      metalness: 0.2
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    ground.visible = false; // Hidden by default, city model has ground
    scene.add(ground);

    // Load player character model
    const loadPlayerCharacter = async () => {
      try {
        const characterModel = player?.appearance?.model || player?.character_model || 'male_base';
        console.log(`🔄 Loading player character: ${characterModel}`);
        
        const character = await loadModel(`/models/characters/${characterModel}.glb`);
        
        // Set random spawn position
        const spawnPos = getRandomSpawnPosition();
        playerPosition.current.copy(spawnPos);
        character.position.copy(playerPosition.current);
        character.scale.set(1, 1, 1);
        
        console.log(`👤 Player spawned at (${spawnPos.x.toFixed(1)}, ${spawnPos.z.toFixed(1)})`);
        
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
        // Fallback to simple cube at random spawn
        const spawnPos = getRandomSpawnPosition();
        playerPosition.current.copy(spawnPos);
        
        const geometry = new THREE.BoxGeometry(1, 2, 1);
        const material = new THREE.MeshStandardMaterial({ color: 0x00ff88 });
        const cube = new THREE.Mesh(geometry, material);
        cube.position.copy(playerPosition.current);
        scene.add(cube);
        characterRef.current = cube;
      }
    };

    // Load city model
    const loadCityModel = async () => {
      try {
        console.log('🔄 Loading city model...');
        const cityModel = await loadModel('/models/city/source/town4new.glb');
        
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
        
        // === NEW: Detect roads and generate NavMesh ===
        await detectRoadsAndGenerateNavMesh(cityModel);
        
        return { size, center };
      } catch (error) {
        console.error('❌ Failed to load city model:', error);
        // Fallback to simple ground plane
        const geometry = new THREE.PlaneGeometry(100, 100);
        const material = new THREE.MeshStandardMaterial({ color: 0x2a2a3e });
        const fallbackGround = new THREE.Mesh(geometry, material);
        fallbackGround.rotation.x = -Math.PI / 2;
        scene.add(fallbackGround);
        throw error;
      }
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

    // === NEW: Detect roads and generate navigation mesh ===
    const detectRoadsAndGenerateNavMesh = async (cityModel) => {
      try {
        console.log('🛣️ Starting road detection and NavMesh generation...');
        
        // Phase 1: Detect roads
        const detector = new RoadDetector(cityModel, {
          debug: true,
          roadColorMin: 0x1a1a1a,
          roadColorMax: 0x606060,
          minFlatness: 0.8,
          minHeight: -2,
          maxHeight: 2
        });
        
        const roadMeshes = detector.detectRoads();
        roadDetectorRef.current = detector;
        
        if (roadMeshes.length === 0) {
          console.warn('⚠️ No roads detected! Movement will not be constrained.');
          return;
        }
        
        // Phase 2: Generate NavMesh
        const navMesh = new NavMesh(roadMeshes, {
          gridSize: 0.5,
          debug: true
        });
        
        const success = navMesh.generate();
        if (success) {
          navMeshRef.current = navMesh;
          console.log('✅ NavMesh successfully generated');
          
          // Phase 3: Create debug visualizations
          createDebugVisualizations(roadMeshes, navMesh);
        } else {
          console.error('❌ Failed to generate NavMesh');
        }
      } catch (error) {
        console.error('❌ Error in road detection:', error);
      }
    };

    // Create debug visualizations for roads and NavMesh
    const createDebugVisualizations = (roadMeshes, navMesh) => {
      // Visualize detected roads with green wireframe
      roadMeshes.forEach(roadMesh => {
        const wireframe = new THREE.LineSegments(
          new THREE.WireframeGeometry(roadMesh.geometry),
          new THREE.LineBasicMaterial({ 
            color: 0x00ff00,  // Green
            transparent: true,
            opacity: 0.3
          })
        );
        wireframe.position.copy(roadMesh.position);
        wireframe.rotation.copy(roadMesh.rotation);
        wireframe.scale.copy(roadMesh.scale);
        wireframe.applyMatrix4(roadMesh.matrixWorld);
        wireframe.visible = showDebugVisuals;
        scene.add(wireframe);
        
        if (!debugVisualsRef.current.roads) {
          debugVisualsRef.current.roads = [];
        }
        debugVisualsRef.current.roads.push(wireframe);
      });
      
      // Visualize NavMesh points
      const navMeshPoints = navMesh.createDebugVisualization();
      if (navMeshPoints) {
        navMeshPoints.visible = showDebugVisuals;
        scene.add(navMeshPoints);
        debugVisualsRef.current.navMesh = navMeshPoints;
      }
      
      console.log('✅ Debug visualizations created (Press V to toggle)');
    };

    // Get random spawn position within city bounds (preferably on roads)
    const getRandomSpawnPosition = () => {
      const bounds = cityBounds.current;
      const margin = 10; // Keep away from edges
      
      // If NavMesh exists, try to spawn on a road
      if (navMeshRef.current && navMeshRef.current.getWalkablePoints().length > 0) {
        const walkablePoints = navMeshRef.current.getWalkablePoints();
        const randomIndex = Math.floor(Math.random() * walkablePoints.length);
        const roadPoint = walkablePoints[randomIndex];
        
        return new THREE.Vector3(
          roadPoint.x,
          roadPoint.y + 1, // Character height offset
          roadPoint.z
        );
      }
      
      // Fallback to random position within bounds
      return new THREE.Vector3(
        bounds.minX + margin + Math.random() * (bounds.maxX - bounds.minX - margin * 2),
        1, // Ground level with character height offset
        bounds.minZ + margin + Math.random() * (bounds.maxZ - bounds.minZ - margin * 2)
      );
    };

    // Load NPC robots with movement behavior
    const loadNPCRobots = async () => {
      const npcs = [
        { type: 'scout', name: 'Scout-01', traits: [{ name: 'Speed', level: 5, type: 'virtue' }] },
        { type: 'trader', name: 'Trader-42', traits: [{ name: 'Charisma', level: 7, type: 'virtue' }] },
        { type: 'medic', name: 'Medic-07', traits: [{ name: 'Compassion', level: 8, type: 'virtue' }] },
        { type: 'combat', name: 'Combat-99', traits: [{ name: 'Strength', level: 9, type: 'virtue' }] },
        { type: 'hacker', name: 'Hacker-13', traits: [{ name: 'Intelligence', level: 10, type: 'virtue' }] },
        { type: 'guardian', name: 'Guardian-77', traits: [{ name: 'Defense', level: 8, type: 'virtue' }] }
      ];

      for (const npcConfig of npcs) {
        const spawnPos = getRandomSpawnPosition();
        
        try {
          const robot = await loadModel(`/models/robots/${npcConfig.type}.glb`);
          robot.position.copy(spawnPos);
          robot.scale.set(1, 1, 1);
          
          // Add NPC data with city-aware behavior
          robot.userData = {
            name: npcConfig.name,
            type: npcConfig.type,
            traits: npcConfig.traits,
            basePosition: spawnPos.clone(),
            targetPosition: spawnPos.clone(),
            moveSpeed: 0.02 + Math.random() * 0.03,
            rotationSpeed: 0.02,
            idleTime: 0,
            isMoving: false
          };
          
          scene.add(robot);
          npcsRef.current.push(robot);
          console.log(`✅ NPC Robot loaded: ${npcConfig.type} at position (${spawnPos.x.toFixed(1)}, ${spawnPos.z.toFixed(1)})`);
        } catch (error) {
          console.warn(`⚠️ Failed to load NPC ${npcConfig.type}, using fallback`);
          // Fallback procedural robot
          const body = new THREE.Mesh(
            new THREE.BoxGeometry(0.8, 1.2, 0.6),
            new THREE.MeshStandardMaterial({ color: 0xff6600 })
          );
          body.position.copy(spawnPos);
          body.userData = {
            name: npcConfig.name,
            type: npcConfig.type,
            traits: npcConfig.traits,
            basePosition: spawnPos.clone(),
            targetPosition: spawnPos.clone(),
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
      await loadCityModel();
      await loadPlayerCharacter();
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
      
      // Toggle debug visuals with 'V' key
      if (key === 'v') {
        setShowDebugVisuals(prev => {
          const newValue = !prev;
          console.log(`🔧 Debug visuals: ${newValue ? 'ON' : 'OFF'}`);
          
          // Update visibility of debug meshes
          if (debugVisualsRef.current.roads) {
            debugVisualsRef.current.roads.forEach(mesh => {
              mesh.visible = newValue;
            });
          }
          if (debugVisualsRef.current.navMesh) {
            debugVisualsRef.current.navMesh.visible = newValue;
          }
          
          return newValue;
        });
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

    // NPC AI: Random movement behavior with boundary awareness and NavMesh constraints
    const updateNPCBehavior = (npc, deltaTime) => {
      const userData = npc.userData;
      const bounds = cityBounds.current;
      
      if (!userData.isMoving) {
        // Idle state
        userData.idleTime += deltaTime;
        
        // Decide to move after random idle time (2-5 seconds)
        if (userData.idleTime > 2000 + Math.random() * 3000) {
          userData.isMoving = true;
          userData.idleTime = 0;
          
          // Set random target within boundaries
          const angle = Math.random() * Math.PI * 2;
          const distance = 5 + Math.random() * 10;
          let targetX = userData.basePosition.x + Math.cos(angle) * distance;
          let targetZ = userData.basePosition.z + Math.sin(angle) * distance;
          
          // Clamp to boundaries
          targetX = Math.max(bounds.minX + 2, Math.min(bounds.maxX - 2, targetX));
          targetZ = Math.max(bounds.minZ + 2, Math.min(bounds.maxZ - 2, targetZ));
          
          // === NEW: Snap target to nearest road if NavMesh exists ===
          if (navMeshRef.current) {
            const nearestRoadPoint = navMeshRef.current.getNearestPoint(targetX, targetZ, 10);
            if (nearestRoadPoint) {
              targetX = nearestRoadPoint.x;
              targetZ = nearestRoadPoint.z;
              userData.targetPosition.set(targetX, nearestRoadPoint.y, targetZ);
            } else {
              userData.targetPosition.set(targetX, userData.basePosition.y, targetZ);
            }
          } else {
            userData.targetPosition.set(targetX, userData.basePosition.y, targetZ);
          }
        }
      } else {
        // Moving state
        const direction = new THREE.Vector3()
          .subVectors(userData.targetPosition, npc.position)
          .normalize();
        
        // Calculate new position
        const newPosition = npc.position.clone().add(direction.multiplyScalar(userData.moveSpeed));
        
        // === NEW: Check NavMesh constraints ===
        let canMove = true;
        if (navMeshRef.current) {
          const nearestRoadPoint = navMeshRef.current.getNearestPoint(
            newPosition.x,
            newPosition.z,
            2.0
          );
          
          if (nearestRoadPoint) {
            // Snap to road
            newPosition.x = nearestRoadPoint.x;
            newPosition.z = nearestRoadPoint.z;
            newPosition.y = nearestRoadPoint.y;
          } else {
            // Off road, stop moving
            canMove = false;
            userData.isMoving = false;
          }
        } else {
          // Check boundaries (fallback)
          if (newPosition.x < bounds.minX || newPosition.x > bounds.maxX ||
              newPosition.z < bounds.minZ || newPosition.z > bounds.maxZ) {
            canMove = false;
            userData.isMoving = false;
          }
        }
        
        if (canMove) {
          npc.position.copy(newPosition);
          
          // Rotate to face movement direction
          const targetRotation = Math.atan2(direction.x, direction.z);
          npc.rotation.y = THREE.MathUtils.lerp(npc.rotation.y, targetRotation, userData.rotationSpeed);
          
          // Check if reached target
          const distance = npc.position.distanceTo(userData.targetPosition);
          if (distance < 0.5) {
            userData.isMoving = false;
          }
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
        const bounds = cityBounds.current;

        // Store previous position for boundary checking
        const prevPosition = playerPosition.current.clone();

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

        // === NEW: NavMesh constraint - slide back to road if off-road ===
        if (navMeshRef.current) {
          const nearestRoadPoint = navMeshRef.current.getNearestPoint(
            playerPosition.current.x,
            playerPosition.current.z,
            2.0  // Max distance to search for road
          );
          
          if (nearestRoadPoint) {
            // Check if player is too far from road
            const dx = playerPosition.current.x - nearestRoadPoint.x;
            const dz = playerPosition.current.z - nearestRoadPoint.z;
            const distanceFromRoad = Math.sqrt(dx * dx + dz * dz);
            
            if (distanceFromRoad > 0.5) {
              // Slide back towards road (smooth correction)
              const slideSpeed = 0.15;
              playerPosition.current.x = THREE.MathUtils.lerp(
                playerPosition.current.x,
                nearestRoadPoint.x,
                slideSpeed
              );
              playerPosition.current.z = THREE.MathUtils.lerp(
                playerPosition.current.z,
                nearestRoadPoint.z,
                slideSpeed
              );
            }
            
            // Update Y position to match road height
            playerPosition.current.y = nearestRoadPoint.y + 1; // Character height offset
          } else {
            // No road found nearby, revert to previous position
            playerPosition.current.copy(prevPosition);
          }
        } else {
          // No NavMesh, use regular boundary constraints
          playerPosition.current.x = Math.max(bounds.minX + 1, Math.min(bounds.maxX - 1, playerPosition.current.x));
          playerPosition.current.z = Math.max(bounds.minZ + 1, Math.min(bounds.maxZ - 1, playerPosition.current.z));
          playerPosition.current.y = Math.max(bounds.minY + 1, Math.min(bounds.maxY, playerPosition.current.y));
        }

        // Apply rotation and position
        characterRef.current.rotation.y = playerRotation.current;
        characterRef.current.position.copy(playerPosition.current);

        // Camera follow with boundary constraints
        const cameraOffset = new THREE.Vector3(0, 5, 10);
        cameraOffset.applyAxisAngle(new THREE.Vector3(0, 1, 0), playerRotation.current);
        const cameraTarget = playerPosition.current.clone().add(cameraOffset);
        
        // Constrain camera position to stay within expanded bounds
        cameraTarget.x = Math.max(bounds.minX - 5, Math.min(bounds.maxX + 5, cameraTarget.x));
        cameraTarget.z = Math.max(bounds.minZ - 5, Math.min(bounds.maxZ + 5, cameraTarget.z));
        
        camera.position.copy(cameraTarget);
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
        <p>V: Toggle Road Debug View</p>
      </div>

      {/* Trait toggle for player */}
      <div className="player-trait-overlay">
        <TraitToggleIcon 
          traits={player?.traits || []} 
          playerName={player?.username || 'You'}
          position="top"
        />
      </div>
      
      {/* NavMesh status indicator */}
      {isLoaded && navMeshRef.current && (
        <div style={{
          position: 'absolute',
          top: '10px',
          right: '10px',
          background: 'rgba(0, 0, 0, 0.7)',
          color: '#00ff00',
          padding: '10px',
          borderRadius: '5px',
          fontSize: '12px',
          fontFamily: 'monospace'
        }}>
          <div>🛣️ Road Detection: Active</div>
          <div>🗺️ NavMesh: {navMeshRef.current.getWalkablePoints().length} points</div>
          <div>👁️ Debug View: {showDebugVisuals ? 'ON' : 'OFF'}</div>
        </div>
      )}
    </div>
  );
};

export default GameWorld;
