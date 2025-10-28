/**
 * Procedural 3D Model Generator
 * Creates detailed 3D models using Three.js primitives when asset files are placeholders
 */

import * as THREE from 'three';

export class ProceduralModels {
  /**
   * Create a detailed humanoid character
   * @param {string} type - 'male_base', 'female_base', 'male_athletic', etc.
   * @returns {THREE.Group} Character mesh group
   */
  static createCharacter(type = 'male_base') {
    const character = new THREE.Group();
    
    // Body parts materials
    const skinColor = 0xffdbac;
    const clothingColor = type.includes('athletic') ? 0x2196F3 : 0x424242;
    const hairColor = 0x3e2723;
    
    // Head
    const headGeometry = new THREE.SphereGeometry(0.35, 16, 16);
    const headMaterial = new THREE.MeshStandardMaterial({ 
      color: skinColor,
      roughness: 0.8,
      metalness: 0.1
    });
    const head = new THREE.Mesh(headGeometry, headMaterial);
    head.position.y = 1.6;
    head.castShadow = true;
    character.add(head);
    
    // Hair
    const hairGeometry = new THREE.SphereGeometry(0.38, 16, 16);
    const hairMaterial = new THREE.MeshStandardMaterial({ 
      color: hairColor,
      roughness: 0.9
    });
    const hair = new THREE.Mesh(hairGeometry, hairMaterial);
    hair.position.y = 1.7;
    hair.scale.set(1, 0.8, 1);
    hair.castShadow = true;
    character.add(hair);
    
    // Eyes (simple)
    const eyeGeometry = new THREE.SphereGeometry(0.05, 8, 8);
    const eyeMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x000000,
      emissive: 0x111111
    });
    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(-0.12, 1.65, 0.3);
    character.add(leftEye);
    
    const rightEye = leftEye.clone();
    rightEye.position.set(0.12, 1.65, 0.3);
    character.add(rightEye);
    
    // Torso
    const torsoGeometry = type.includes('heavy') 
      ? new THREE.BoxGeometry(0.7, 0.9, 0.4)
      : new THREE.BoxGeometry(0.5, 0.9, 0.35);
    const torsoMaterial = new THREE.MeshStandardMaterial({ 
      color: clothingColor,
      roughness: 0.7,
      metalness: 0.2
    });
    const torso = new THREE.Mesh(torsoGeometry, torsoMaterial);
    torso.position.y = 0.9;
    torso.castShadow = true;
    character.add(torso);
    
    // Arms
    const armGeometry = new THREE.CapsuleGeometry(0.1, 0.6, 8, 16);
    const armMaterial = new THREE.MeshStandardMaterial({ 
      color: clothingColor,
      roughness: 0.7
    });
    
    const leftArm = new THREE.Mesh(armGeometry, armMaterial);
    leftArm.position.set(-0.35, 0.9, 0);
    leftArm.rotation.z = Math.PI / 12;
    leftArm.castShadow = true;
    character.add(leftArm);
    
    const rightArm = new THREE.Mesh(armGeometry, armMaterial);
    rightArm.position.set(0.35, 0.9, 0);
    rightArm.rotation.z = -Math.PI / 12;
    rightArm.castShadow = true;
    character.add(rightArm);
    
    // Legs
    const legGeometry = new THREE.CapsuleGeometry(0.12, 0.8, 8, 16);
    const legMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x1a1a1a,
      roughness: 0.8
    });
    
    const leftLeg = new THREE.Mesh(legGeometry, legMaterial);
    leftLeg.position.set(-0.15, 0.05, 0);
    leftLeg.castShadow = true;
    character.add(leftLeg);
    
    const rightLeg = new THREE.Mesh(legGeometry, legMaterial);
    rightLeg.position.set(0.15, 0.05, 0);
    rightLeg.castShadow = true;
    character.add(rightLeg);
    
    // Add glow effect for player character
    const glowGeometry = new THREE.SphereGeometry(0.8, 16, 16);
    const glowMaterial = new THREE.MeshBasicMaterial({
      color: 0x00ff00,
      transparent: true,
      opacity: 0.1,
      side: THREE.BackSide
    });
    const glow = new THREE.Mesh(glowGeometry, glowMaterial);
    glow.position.y = 1;
    character.add(glow);
    
    return character;
  }
  
  /**
   * Create a detailed robot model
   * @param {string} type - 'scout', 'combat', 'medic', etc.
   * @returns {THREE.Group} Robot mesh group
   */
  static createRobot(type = 'scout') {
    const robot = new THREE.Group();
    
    // Color scheme based on type
    const colorMap = {
      scout: { body: 0x2196F3, accent: 0x00BCD4 },
      combat: { body: 0xF44336, accent: 0xFF5722 },
      medic: { body: 0x4CAF50, accent: 0x8BC34A },
      trader: { body: 0xFFB74D, accent: 0xFFA726 },
      hacker: { body: 0x9C27B0, accent: 0xAB47BC },
      guardian: { body: 0x607D8B, accent: 0x78909C },
      harvester: { body: 0x795548, accent: 0x8D6E63 },
      tactical: { body: 0x546E7A, accent: 0x607D8B },
      assault: { body: 0xE53935, accent: 0xD32F2F }
    };
    
    const colors = colorMap[type] || colorMap.scout;
    
    // Main body
    const bodyGeometry = new THREE.BoxGeometry(0.6, 0.8, 0.4);
    const bodyMaterial = new THREE.MeshStandardMaterial({ 
      color: colors.body,
      roughness: 0.3,
      metalness: 0.8
    });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    body.position.y = 0.8;
    body.castShadow = true;
    robot.add(body);
    
    // Head/Sensor unit
    const headGeometry = new THREE.SphereGeometry(0.25, 16, 16);
    const headMaterial = new THREE.MeshStandardMaterial({ 
      color: colors.accent,
      roughness: 0.2,
      metalness: 0.9,
      emissive: colors.accent,
      emissiveIntensity: 0.2
    });
    const head = new THREE.Mesh(headGeometry, headMaterial);
    head.position.y = 1.45;
    head.castShadow = true;
    robot.add(head);
    
    // Visor/Eye
    const visorGeometry = new THREE.PlaneGeometry(0.3, 0.1);
    const visorMaterial = new THREE.MeshBasicMaterial({ 
      color: 0x00ffff,
      emissive: 0x00ffff,
      emissiveIntensity: 0.8
    });
    const visor = new THREE.Mesh(visorGeometry, visorMaterial);
    visor.position.set(0, 1.45, 0.26);
    robot.add(visor);
    
    // Arms/Manipulators
    const armGeometry = new THREE.CylinderGeometry(0.08, 0.08, 0.6, 8);
    const armMaterial = new THREE.MeshStandardMaterial({ 
      color: colors.body,
      roughness: 0.3,
      metalness: 0.8
    });
    
    const leftArm = new THREE.Mesh(armGeometry, armMaterial);
    leftArm.position.set(-0.4, 0.8, 0);
    leftArm.castShadow = true;
    robot.add(leftArm);
    
    const rightArm = new THREE.Mesh(armGeometry, armMaterial);
    rightArm.position.set(0.4, 0.8, 0);
    rightArm.castShadow = true;
    robot.add(rightArm);
    
    // Legs/Treads (depending on type)
    if (type === 'scout' || type === 'trader') {
      // Wheeled base
      const wheelGeometry = new THREE.CylinderGeometry(0.15, 0.15, 0.5, 16);
      const wheelMaterial = new THREE.MeshStandardMaterial({ 
        color: 0x424242,
        roughness: 0.8,
        metalness: 0.6
      });
      const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
      wheel.rotation.z = Math.PI / 2;
      wheel.position.y = 0.15;
      wheel.castShadow = true;
      robot.add(wheel);
    } else {
      // Bipedal legs
      const legGeometry = new THREE.CylinderGeometry(0.1, 0.1, 0.5, 8);
      const legMaterial = new THREE.MeshStandardMaterial({ 
        color: colors.body,
        roughness: 0.3,
        metalness: 0.8
      });
      
      const leftLeg = new THREE.Mesh(legGeometry, legMaterial);
      leftLeg.position.set(-0.15, 0.25, 0);
      leftLeg.castShadow = true;
      robot.add(leftLeg);
      
      const rightLeg = new THREE.Mesh(legGeometry, legMaterial);
      rightLeg.position.set(0.15, 0.25, 0);
      rightLeg.castShadow = true;
      robot.add(rightLeg);
    }
    
    // Antenna/Sensor
    const antennaGeometry = new THREE.CylinderGeometry(0.02, 0.02, 0.3, 8);
    const antennaMaterial = new THREE.MeshStandardMaterial({ 
      color: colors.accent,
      roughness: 0.2,
      metalness: 0.9
    });
    const antenna = new THREE.Mesh(antennaGeometry, antennaMaterial);
    antenna.position.y = 1.75;
    robot.add(antenna);
    
    // Glowing tip
    const tipGeometry = new THREE.SphereGeometry(0.05, 8, 8);
    const tipMaterial = new THREE.MeshBasicMaterial({ 
      color: colors.accent,
      emissive: colors.accent,
      emissiveIntensity: 1
    });
    const tip = new THREE.Mesh(tipGeometry, tipMaterial);
    tip.position.y = 1.9;
    robot.add(tip);
    
    return robot;
  }
  
  /**
   * Create building model
   * @param {string} type - 'tower', 'shop', 'headquarters', etc.
   * @returns {THREE.Group} Building mesh group
   */
  static createBuilding(type = 'tower') {
    const building = new THREE.Group();
    
    const buildingConfig = {
      tower: { height: 8, width: 3, depth: 3, color: 0x546E7A },
      shop: { height: 4, width: 5, depth: 4, color: 0x8D6E63 },
      warehouse: { height: 5, width: 7, depth: 6, color: 0x757575 },
      headquarters: { height: 10, width: 6, depth: 6, color: 0x37474F }
    };
    
    const config = buildingConfig[type] || buildingConfig.tower;
    
    // Main structure
    const buildingGeometry = new THREE.BoxGeometry(config.width, config.height, config.depth);
    const buildingMaterial = new THREE.MeshStandardMaterial({ 
      color: config.color,
      roughness: 0.8,
      metalness: 0.3
    });
    const buildingMesh = new THREE.Mesh(buildingGeometry, buildingMaterial);
    buildingMesh.position.y = config.height / 2;
    buildingMesh.castShadow = true;
    buildingMesh.receiveShadow = true;
    building.add(buildingMesh);
    
    // Windows
    const windowGeometry = new THREE.PlaneGeometry(0.4, 0.6);
    const windowMaterial = new THREE.MeshBasicMaterial({ 
      color: 0x00ffff,
      emissive: 0x00ffff,
      emissiveIntensity: 0.3
    });
    
    // Add windows on front face
    for (let y = 1; y < config.height - 1; y += 1.5) {
      for (let x = -config.width / 2 + 1; x < config.width / 2; x += 1.2) {
        const window = new THREE.Mesh(windowGeometry, windowMaterial);
        window.position.set(x, y, config.depth / 2 + 0.01);
        building.add(window);
      }
    }
    
    // Roof antenna
    if (type === 'tower' || type === 'headquarters') {
      const antennaGeometry = new THREE.CylinderGeometry(0.1, 0.1, 2, 8);
      const antennaMaterial = new THREE.MeshStandardMaterial({ 
        color: 0xFF0000,
        emissive: 0xFF0000,
        emissiveIntensity: 0.5,
        roughness: 0.2,
        metalness: 0.9
      });
      const antenna = new THREE.Mesh(antennaGeometry, antennaMaterial);
      antenna.position.y = config.height + 1;
      building.add(antenna);
    }
    
    return building;
  }
  
  /**
   * Create environment prop
   * @param {string} type - 'container', 'vehicle', 'platform'
   * @returns {THREE.Mesh} Prop mesh
   */
  static createProp(type = 'container') {
    if (type === 'container') {
      const geometry = new THREE.BoxGeometry(2, 2.5, 2);
      const material = new THREE.MeshStandardMaterial({ 
        color: 0x795548,
        roughness: 0.9,
        metalness: 0.4
      });
      const container = new THREE.Mesh(geometry, material);
      container.castShadow = true;
      container.receiveShadow = true;
      return container;
    } else if (type === 'vehicle') {
      const vehicle = new THREE.Group();
      
      // Body
      const bodyGeometry = new THREE.BoxGeometry(2, 1, 4);
      const bodyMaterial = new THREE.MeshStandardMaterial({ 
        color: 0x1565C0,
        roughness: 0.5,
        metalness: 0.7
      });
      const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
      body.position.y = 0.7;
      body.castShadow = true;
      vehicle.add(body);
      
      // Wheels
      const wheelGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.2, 16);
      const wheelMaterial = new THREE.MeshStandardMaterial({ 
        color: 0x212121,
        roughness: 0.8
      });
      
      const positions = [
        { x: -0.8, y: 0.3, z: 1.2 },
        { x: 0.8, y: 0.3, z: 1.2 },
        { x: -0.8, y: 0.3, z: -1.2 },
        { x: 0.8, y: 0.3, z: -1.2 }
      ];
      
      positions.forEach(pos => {
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(pos.x, pos.y, pos.z);
        wheel.castShadow = true;
        vehicle.add(wheel);
      });
      
      return vehicle;
    } else if (type === 'platform') {
      const geometry = new THREE.BoxGeometry(5, 0.3, 5);
      const material = new THREE.MeshStandardMaterial({ 
        color: 0x607D8B,
        roughness: 0.7,
        metalness: 0.5
      });
      const platform = new THREE.Mesh(geometry, material);
      platform.castShadow = true;
      platform.receiveShadow = true;
      return platform;
    }
    
    // Default cube
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshStandardMaterial({ color: 0x888888 });
    return new THREE.Mesh(geometry, material);
  }
}

export default ProceduralModels;
