import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import AssetLoader from '../../../utils/AssetLoader';
import ProceduralModels from '../../../utils/ProceduralModels';
import './GameWorld.css';

/**
 * Main 3D Game World Component
 * Renders the game environment using Three.js
 */
const GameWorld = ({ player }) => {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const rendererRef = useRef(null);
  const characterRef = useRef(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState(null);

  // Movement state
  const keysPressed = useRef({
    w: false,
    a: false,
    s: false,
    d: false,
    ArrowUp: false,
    ArrowDown: false,
    ArrowLeft: false,
    ArrowRight: false,
    space: false
  });

  const playerPosition = useRef(new THREE.Vector3(0, 1, 0));
  const playerVelocity = useRef(new THREE.Vector3(0, 0, 0));
  const playerRotation = useRef(0);

  useEffect(() => {
    if (!mountRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    scene.fog = new THREE.Fog(0x1a1a2e, 10, 50);
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
    renderer.setPixelRatio(window.devicePixelRatio);
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
    const groundGeometry = new THREE.PlaneGeometry(100, 100);
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
    const gridHelper = new THREE.GridHelper(100, 50, 0x00ff00, 0x404040);
    scene.add(gridHelper);

    // Load character model - Try GLB first, fallback to procedural
    console.log('Loading character model...');
    const characterType = player?.gender === 'female' ? 'female_base' : 'male_base';
    
    // Use AssetLoader with automatic fallback
    AssetLoader.loadCharacter(characterType)
      .then(character => {
        character.position.copy(playerPosition.current);
        scene.add(character);
        characterRef.current = character;
        setIsLoaded(true);
        console.log('✅ Character loaded successfully');
      })
      .catch(error => {
        console.error('Failed to load character:', error);
        setError('Failed to load character model');
      });

    // Load environment - Use procedural buildings
    const buildings = [
      { type: 'tower', position: { x: 10, y: 0, z: -10 } },
      { type: 'shop', position: { x: -8, y: 0, z: -8 } },
      { type: 'warehouse', position: { x: 15, y: 0, z: 5 } },
      { type: 'headquarters', position: { x: -12, y: 0, z: 10 } }
    ];
    
    buildings.forEach(buildingConfig => {
      const building = ProceduralModels.createBuilding(buildingConfig.type);
      building.position.set(buildingConfig.position.x, buildingConfig.position.y, buildingConfig.position.z);
      scene.add(building);
    });
    
    // Add some props
    const container = ProceduralModels.createProp('container');
    container.position.set(5, 1.25, 5);
    scene.add(container);
    
    const vehicle = ProceduralModels.createProp('vehicle');
    vehicle.position.set(-5, 0, 8);
    scene.add(vehicle);
    
    console.log('✅ Environment loaded successfully');
    
    // Add NPC robots
    const npcs = [
      { type: 'scout', position: { x: 3, y: 0, z: 3 } },
      { type: 'trader', position: { x: -3, y: 0, z: -3 } },
      { type: 'medic', position: { x: 7, y: 0, z: 0 } },
      { type: 'combat', position: { x: -6, y: 0, z: 4 } }
    ];
    
    npcs.forEach(npcConfig => {
      const robot = ProceduralModels.createRobot(npcConfig.type);
      robot.position.set(npcConfig.position.x, npcConfig.position.y, npcConfig.position.z);
      scene.add(robot);
    });
    
    console.log('✅ NPCs loaded successfully');

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

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);

      if (characterRef.current) {
        const speed = 0.1;
        const rotationSpeed = 0.05;
        let moved = false;

        // WASD + Arrow key movement
        if (keysPressed.current.w || keysPressed.current.ArrowUp) {
          playerPosition.current.z -= speed;
          moved = true;
        }
        if (keysPressed.current.s || keysPressed.current.ArrowDown) {
          playerPosition.current.z += speed;
          moved = true;
        }
        if (keysPressed.current.a || keysPressed.current.ArrowLeft) {
          playerRotation.current += rotationSpeed;
        }
        if (keysPressed.current.d || keysPressed.current.ArrowRight) {
          playerRotation.current -= rotationSpeed;
        }

        // Apply rotation
        characterRef.current.rotation.y = playerRotation.current;

        // Apply movement
        characterRef.current.position.copy(playerPosition.current);

        // Camera follow
        const cameraOffset = new THREE.Vector3(0, 5, 10);
        cameraOffset.applyAxisAngle(new THREE.Vector3(0, 1, 0), playerRotation.current);
        camera.position.copy(playerPosition.current).add(cameraOffset);
        camera.lookAt(playerPosition.current);
      }

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
  }, []);

  return (
    <div className="game-world-container">
      <div ref={mountRef} className="game-world" />
      
      {!isLoaded && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <p>Loading Game World...</p>
        </div>
      )}

      {error && (
        <div className="error-overlay">
          <p>Error loading game: {error}</p>
        </div>
      )}

      <div className="controls-hint">
        <p><strong>Controls:</strong></p>
        <p>WASD or Arrow Keys: Move</p>
        <p>A/D or Left/Right: Rotate</p>
      </div>
    </div>
  );
};

export default GameWorld;
