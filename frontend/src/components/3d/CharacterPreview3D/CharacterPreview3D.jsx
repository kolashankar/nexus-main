import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import './CharacterPreview3D.css';

/**
 * 3D Character Preview Component
 * Displays a customizable 3D character model with real-time updates
 */
const CharacterPreview3D = ({ 
  characterModel = 'male_base',
  skinTone = 'default',
  hairColor = 'brown',
  className = '' 
}) => {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const rendererRef = useRef(null);
  const characterRef = useRef(null);
  const animationFrameRef = useRef(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Skin tone colors
  const skinToneColors = {
    light: 0xFFE0BD,
    medium: 0xC68642,
    dark: 0x8D5524,
    default: 0xE0AC69
  };

  // Hair colors
  const hairColorValues = {
    black: 0x141414,
    brown: 0x462B19,
    blonde: 0xE6C878,
    red: 0xA52A2A
  };

  useEffect(() => {
    if (!mountRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    sceneRef.current = scene;

    // Camera setup
    const camera = new THREE.PerspectiveCamera(
      50,
      mountRef.current.clientWidth / mountRef.current.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 1.5, 3);
    camera.lookAt(0, 1, 0);
    cameraRef.current = camera;

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    mountRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(2, 3, 2);
    directionalLight.castShadow = true;
    scene.add(directionalLight);

    const fillLight = new THREE.DirectionalLight(0x8888ff, 0.3);
    fillLight.position.set(-2, 1, -2);
    scene.add(fillLight);

    // Add a circular platform
    const platformGeometry = new THREE.CylinderGeometry(1.5, 1.5, 0.1, 32);
    const platformMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x2a2a3e,
      roughness: 0.7,
      metalness: 0.3
    });
    const platform = new THREE.Mesh(platformGeometry, platformMaterial);
    platform.position.y = -0.05;
    platform.receiveShadow = true;
    scene.add(platform);

    // Animation loop
    const animate = () => {
      animationFrameRef.current = requestAnimationFrame(animate);

      // Rotate character slowly
      if (characterRef.current) {
        characterRef.current.rotation.y += 0.005;
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
      window.removeEventListener('resize', handleResize);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  // Load character model
  useEffect(() => {
    if (!sceneRef.current) return;

    const scene = sceneRef.current;
    const loader = new GLTFLoader();

    // Remove existing character
    if (characterRef.current) {
      scene.remove(characterRef.current);
      characterRef.current = null;
    }

    setIsLoading(true);
    setError(null);

    const modelPath = `/models/characters/${characterModel}.glb`;

    loader.load(
      modelPath,
      (gltf) => {
        const character = gltf.scene;
        
        // Position and scale
        character.position.set(0, 0, 0);
        character.scale.set(1, 1, 1);

        // Apply customizations
        character.traverse((child) => {
          if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;

            // Apply skin tone to body/skin materials
            if (child.material && (child.name.toLowerCase().includes('body') || 
                                   child.name.toLowerCase().includes('skin') ||
                                   child.name.toLowerCase().includes('face'))) {
              const skinColor = skinToneColors[skinTone] || skinToneColors.default;
              if (child.material.color) {
                child.material.color.setHex(skinColor);
              }
            }

            // Apply hair color
            if (child.material && child.name.toLowerCase().includes('hair')) {
              const hairColorValue = hairColorValues[hairColor] || hairColorValues.brown;
              if (child.material.color) {
                child.material.color.setHex(hairColorValue);
              }
            }
          }
        });

        scene.add(character);
        characterRef.current = character;
        setIsLoading(false);
        
        console.log(`✅ Character model loaded: ${characterModel}`);
      },
      (progress) => {
        // Loading progress
        if (progress.total > 0) {
          const percent = (progress.loaded / progress.total) * 100;
          console.log(`Loading character: ${percent.toFixed(0)}%`);
        }
      },
      (error) => {
        console.error('Error loading character model:', error);
        setError('Failed to load character model');
        setIsLoading(false);
      }
    );
  }, [characterModel, skinTone, hairColor]);

  return (
    <div className={`character-preview-3d ${className}`}>
      <div ref={mountRef} className="character-preview-canvas" />
      
      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <p>Loading Character...</p>
        </div>
      )}

      {error && (
        <div className="error-overlay">
          <p>{error}</p>
        </div>
      )}
    </div>
  );
};

export default CharacterPreview3D;
