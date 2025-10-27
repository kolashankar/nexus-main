/**
 * GameWorld - Main 3D game environment component
 */
import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { PointerLockControls } from 'three/examples/jsm/controls/PointerLockControls';

const GameWorld = ({ player }) => {
  const containerRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const rendererRef = useRef(null);
  const controlsRef = useRef(null);
  const playerMeshRef = useRef(null);
  const clockRef = useRef(new THREE.Clock());
  
  const [isLocked, setIsLocked] = useState(false);

  // Movement state
  const moveState = useRef({
    forward: false,
    backward: false,
    left: false,
    right: false,
    jump: false,
    canJump: true
  });

  const velocity = useRef(new THREE.Vector3());
  const direction = useRef(new THREE.Vector3());

  useEffect(() => {
    if (!containerRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    scene.fog = new THREE.Fog(0x1a1a2e, 50, 200);
    sceneRef.current = scene;

    // Camera setup
    const camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    camera.position.set(0, 1.6, 5);
    cameraRef.current = camera;

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    containerRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(50, 100, 50);
    directionalLight.castShadow = true;
    directionalLight.shadow.camera.left = -50;
    directionalLight.shadow.camera.right = 50;
    directionalLight.shadow.camera.top = 50;
    directionalLight.shadow.camera.bottom = -50;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    scene.add(directionalLight);

    // Hemisphere light for better atmosphere
    const hemiLight = new THREE.HemisphereLight(0x9370db, 0x1a1a2e, 0.5);
    scene.add(hemiLight);

    // Ground/Platform
    const groundGeometry = new THREE.PlaneGeometry(100, 100);
    const groundMaterial = new THREE.MeshStandardMaterial({
      color: 0x2a2a4e,
      roughness: 0.8,
      metalness: 0.2
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    // Grid helper for better spatial awareness
    const gridHelper = new THREE.GridHelper(100, 50, 0x9370db, 0x4a4a6e);
    scene.add(gridHelper);

    // Load 3D Models
    const loader = new GLTFLoader();

    // Load player character model
    const characterModel = player?.gender === 'female' 
      ? '/models/characters/female_base.glb' 
      : '/models/characters/male_base.glb';

    loader.load(
      characterModel,
      (gltf) => {
        const playerModel = gltf.scene;
        playerModel.scale.set(1, 1, 1);
        playerModel.position.set(0, 0, 0);
        playerModel.castShadow = true;
        playerModel.traverse((child) => {
          if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
          }
        });
        scene.add(playerModel);
        playerMeshRef.current = playerModel;
      },
      undefined,
      (error) => {
        console.error('Error loading character model:', error);
        // Fallback to simple geometry
        const fallbackGeometry = new THREE.CapsuleGeometry(0.5, 1.5, 4, 8);
        const fallbackMaterial = new THREE.MeshStandardMaterial({ 
          color: 0x9370db,
          metalness: 0.3,
          roughness: 0.7
        });
        const fallbackPlayer = new THREE.Mesh(fallbackGeometry, fallbackMaterial);
        fallbackPlayer.position.set(0, 1.5, 0);
        fallbackPlayer.castShadow = true;
        scene.add(fallbackPlayer);
        playerMeshRef.current = fallbackPlayer;
      }
    );

    // Load environment buildings
    const buildingModels = [
      { path: '/models/environment/buildings/tower.glb', position: [20, 0, -20], scale: 2 },
      { path: '/models/environment/buildings/headquarters.glb', position: [-20, 0, -20], scale: 2 },
      { path: '/models/environment/buildings/shop.glb', position: [15, 0, 15], scale: 1.5 },
      { path: '/models/environment/buildings/warehouse.glb', position: [-15, 0, 15], scale: 1.5 }
    ];

    buildingModels.forEach(({ path, position, scale }) => {
      loader.load(
        path,
        (gltf) => {
          const building = gltf.scene;
          building.position.set(...position);
          building.scale.set(scale, scale, scale);
          building.traverse((child) => {
            if (child.isMesh) {
              child.castShadow = true;
              child.receiveShadow = true;
            }
          });
          scene.add(building);
        },
        undefined,
        (error) => {
          console.warn(`Could not load building ${path}:`, error);
          // Add fallback cube
          const cubeGeometry = new THREE.BoxGeometry(5, 10, 5);
          const cubeMaterial = new THREE.MeshStandardMaterial({ color: 0x4a4a6e });
          const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
          cube.position.set(...position);
          cube.castShadow = true;
          cube.receiveShadow = true;
          scene.add(cube);
        }
      );
    });

    // Add some props/decorations
    const propModels = [
      { path: '/models/environment/props/container.glb', position: [10, 0, 5], scale: 1 },
      { path: '/models/environment/props/container.glb', position: [-10, 0, 5], scale: 1 },
      { path: '/models/environment/props/vehicle.glb', position: [0, 0, 10], scale: 1.2 }
    ];

    propModels.forEach(({ path, position, scale }) => {
      loader.load(
        path,
        (gltf) => {
          const prop = gltf.scene;
          prop.position.set(...position);
          prop.scale.set(scale, scale, scale);
          prop.traverse((child) => {
            if (child.isMesh) {
              child.castShadow = true;
              child.receiveShadow = true;
            }
          });
          scene.add(prop);
        },
        undefined,
        (error) => console.warn(`Could not load prop ${path}:`, error)
      );
    });

    // Add some robots/NPCs
    const robotModels = [
      { path: '/models/robots/scout.glb', position: [8, 0, -8], scale: 1 },
      { path: '/models/robots/trader.glb', position: [-8, 0, -8], scale: 1 }
    ];

    robotModels.forEach(({ path, position, scale }) => {
      loader.load(
        path,
        (gltf) => {
          const robot = gltf.scene;
          robot.position.set(...position);
          robot.scale.set(scale, scale, scale);
          robot.traverse((child) => {
            if (child.isMesh) {
              child.castShadow = true;
              child.receiveShadow = true;
            }
          });
          scene.add(robot);
        },
        undefined,
        (error) => console.warn(`Could not load robot ${path}:`, error)
      );
    });

    // Pointer Lock Controls
    const controls = new PointerLockControls(camera, renderer.domElement);
    controlsRef.current = controls;

    controls.addEventListener('lock', () => setIsLocked(true));
    controls.addEventListener('unlock', () => setIsLocked(false));

    // Click to enable controls
    renderer.domElement.addEventListener('click', () => {
      controls.lock();
    });

    // Keyboard controls
    const onKeyDown = (event) => {
      switch (event.code) {
        case 'KeyW':
        case 'ArrowUp':
          moveState.current.forward = true;
          break;
        case 'KeyS':
        case 'ArrowDown':
          moveState.current.backward = true;
          break;
        case 'KeyA':
        case 'ArrowLeft':
          moveState.current.left = true;
          break;
        case 'KeyD':
        case 'ArrowRight':
          moveState.current.right = true;
          break;
        case 'Space':
          if (moveState.current.canJump) {
            velocity.current.y = 10;
            moveState.current.canJump = false;
          }
          break;
      }
    };

    const onKeyUp = (event) => {
      switch (event.code) {
        case 'KeyW':
        case 'ArrowUp':
          moveState.current.forward = false;
          break;
        case 'KeyS':
        case 'ArrowDown':
          moveState.current.backward = false;
          break;
        case 'KeyA':
        case 'ArrowLeft':
          moveState.current.left = false;
          break;
        case 'KeyD':
        case 'ArrowRight':
          moveState.current.right = false;
          break;
      }
    };

    document.addEventListener('keydown', onKeyDown);
    document.addEventListener('keyup', onKeyUp);

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);

      const delta = clockRef.current.getDelta();

      if (controls.isLocked) {
        // Apply movement
        velocity.current.x -= velocity.current.x * 10.0 * delta;
        velocity.current.z -= velocity.current.z * 10.0 * delta;
        velocity.current.y -= 9.8 * 10.0 * delta; // Gravity

        direction.current.z = Number(moveState.current.forward) - Number(moveState.current.backward);
        direction.current.x = Number(moveState.current.right) - Number(moveState.current.left);
        direction.current.normalize();

        if (moveState.current.forward || moveState.current.backward) {
          velocity.current.z -= direction.current.z * 40.0 * delta;
        }
        if (moveState.current.left || moveState.current.right) {
          velocity.current.x -= direction.current.x * 40.0 * delta;
        }

        controls.moveRight(-velocity.current.x * delta);
        controls.moveForward(-velocity.current.z * delta);

        camera.position.y += velocity.current.y * delta;

        if (camera.position.y < 1.6) {
          velocity.current.y = 0;
          camera.position.y = 1.6;
          moveState.current.canJump = true;
        }

        // Update player mesh position to follow camera
        if (playerMeshRef.current) {
          playerMeshRef.current.position.set(
            camera.position.x,
            0,
            camera.position.z
          );
          // Rotate player mesh to face movement direction
          if (direction.current.length() > 0) {
            const angle = Math.atan2(direction.current.x, direction.current.z);
            playerMeshRef.current.rotation.y = angle;
          }
        }
      }

      renderer.render(scene, camera);
    };

    animate();

    // Handle window resize
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };

    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      document.removeEventListener('keydown', onKeyDown);
      document.removeEventListener('keyup', onKeyUp);
      
      if (containerRef.current && renderer.domElement) {
        containerRef.current.removeChild(renderer.domElement);
      }
      
      renderer.dispose();
      scene.clear();
    };
  }, [player]);

  return (
    <>
      <div ref={containerRef} className="w-full h-full" />
      {!isLocked && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/50 pointer-events-none">
          <div className="bg-purple-900/90 text-white px-8 py-6 rounded-lg text-center pointer-events-auto">
            <h2 className="text-2xl font-bold mb-2">Click to Play</h2>
            <p className="text-gray-300">Click anywhere to start controlling your character</p>
          </div>
        </div>
      )}
    </>
  );
};

export default GameWorld;
