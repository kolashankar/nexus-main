/**
 * RoadNavMesh - Detects roads and generates navigation mesh for city model
 * Uses three-pathfinding for pathfinding and navigation
 */

import * as THREE from 'three';
import { Pathfinding } from 'three-pathfinding';
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

export class RoadNavMesh {
  constructor(cityModel) {
    this.cityModel = cityModel;
    this.pathfinding = new Pathfinding();
    this.navMesh = null;
    this.roadMeshes = [];
    this.roadGeometry = null;
    this.zoneId = 'city-roads';
    
    // Configuration for road detection
    this.config = {
      // Black color threshold (RGB values close to 0)
      blackThreshold: 30, // 0-255, values below this are considered "black"
      // Height tolerance for flat surfaces (roads are typically flat)
      flatnessThreshold: 0.1,
      // Minimum area for a surface to be considered a road
      minRoadArea: 5.0,
      // Maximum height above ground to be considered a road
      maxRoadHeight: 0.5,
    };
  }

  /**
   * Initialize and generate NavMesh from city model
   */
  async generateNavMesh() {
    console.log('🛣️ Starting road detection and NavMesh generation...');
    
    try {
      // Step 1: Detect road surfaces
      this.detectRoadSurfaces();
      
      // Step 2: Merge road geometries
      const mergedRoadGeometry = this.mergeRoadGeometries();
      
      if (!mergedRoadGeometry || mergedRoadGeometry.attributes.position.count === 0) {
        console.warn('⚠️ No road surfaces detected, creating fallback NavMesh');
        this.createFallbackNavMesh();
        return this.navMesh;
      }
      
      // Step 3: Create NavMesh from road geometry
      this.createNavMesh(mergedRoadGeometry);
      
      console.log('✅ NavMesh generated successfully');
      console.log(`   Road meshes detected: ${this.roadMeshes.length}`);
      console.log(`   NavMesh vertices: ${mergedRoadGeometry.attributes.position.count}`);
      
      return this.navMesh;
      
    } catch (error) {
      console.error('❌ Failed to generate NavMesh:', error);
      this.createFallbackNavMesh();
      return this.navMesh;
    }
  }

  /**
   * Detect road surfaces by analyzing material colors and geometry
   */
  detectRoadSurfaces() {
    console.log('🔍 Detecting road surfaces...');
    
    const roadCandidates = [];
    
    this.cityModel.traverse((child) => {
      if (child.isMesh) {
        const score = this.evaluateRoadMesh(child);
        
        if (score > 0.5) { // Threshold for road confidence
          roadCandidates.push({ mesh: child, score });
          console.log(`   ✓ Found road: ${child.name || 'unnamed'} (score: ${score.toFixed(2)})`);
        }
      }
    });
    
    // Sort by score and take the best candidates
    roadCandidates.sort((a, b) => b.score - a.score);
    this.roadMeshes = roadCandidates.map(c => c.mesh);
    
    console.log(`📊 Detected ${this.roadMeshes.length} road surfaces`);
  }

  /**
   * Evaluate if a mesh is likely a road surface
   */
  evaluateRoadMesh(mesh) {
    let score = 0;
    
    // Check 1: Material color (black or dark)
    const colorScore = this.checkMaterialColor(mesh);
    score += colorScore * 0.4;
    
    // Check 2: Flatness (roads are flat)
    const flatnessScore = this.checkFlatness(mesh);
    score += flatnessScore * 0.3;
    
    // Check 3: Height level (roads are near ground)
    const heightScore = this.checkHeightLevel(mesh);
    score += heightScore * 0.2;
    
    // Check 4: Name hints (contains "road", "street", "path")
    const nameScore = this.checkNameHints(mesh);
    score += nameScore * 0.1;
    
    return score;
  }

  /**
   * Check if material color is black or dark
   */
  checkMaterialColor(mesh) {
    if (!mesh.material) return 0;
    
    const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
    
    for (const material of materials) {
      if (material.color) {
        const r = material.color.r * 255;
        const g = material.color.g * 255;
        const b = material.color.b * 255;
        
        // Check if color is close to black
        const avgColor = (r + g + b) / 3;
        
        if (avgColor < this.config.blackThreshold) {
          return 1.0; // Perfect match - black color
        } else if (avgColor < this.config.blackThreshold * 3) {
          return 0.5; // Dark gray - possible road
        }
      }
      
      // Check texture/map
      if (material.map && material.map.name && 
          (material.map.name.toLowerCase().includes('road') || 
           material.map.name.toLowerCase().includes('asphalt'))) {
        return 0.8;
      }
    }
    
    return 0;
  }

  /**
   * Check if surface is flat (roads are typically flat)
   */
  checkFlatness(mesh) {
    if (!mesh.geometry) return 0;
    
    const geometry = mesh.geometry;
    const position = geometry.attributes.position;
    
    if (!position) return 0;
    
    // Calculate normal variance
    let normalVariance = 0;
    const normals = geometry.attributes.normal;
    
    if (normals) {
      const upVector = new THREE.Vector3(0, 1, 0);
      let dotSum = 0;
      
      for (let i = 0; i < normals.count; i++) {
        const normal = new THREE.Vector3(
          normals.getX(i),
          normals.getY(i),
          normals.getZ(i)
        );
        dotSum += Math.abs(normal.dot(upVector));
      }
      
      const avgDot = dotSum / normals.count;
      
      // If most normals point up, it's flat
      if (avgDot > 0.9) return 1.0;
      if (avgDot > 0.7) return 0.5;
    }
    
    return 0;
  }

  /**
   * Check if mesh is at ground level
   */
  checkHeightLevel(mesh) {
    const worldPos = new THREE.Vector3();
    mesh.getWorldPosition(worldPos);
    
    const bbox = new THREE.Box3().setFromObject(mesh);
    const minY = bbox.min.y;
    
    // Roads should be near y=0 (ground level)
    if (Math.abs(minY) < this.config.maxRoadHeight) {
      return 1.0;
    } else if (Math.abs(minY) < this.config.maxRoadHeight * 2) {
      return 0.5;
    }
    
    return 0;
  }

  /**
   * Check if mesh name suggests it's a road
   */
  checkNameHints(mesh) {
    if (!mesh.name) return 0;
    
    const name = mesh.name.toLowerCase();
    const roadKeywords = ['road', 'street', 'path', 'lane', 'avenue', 'asphalt', 'pavement'];
    
    for (const keyword of roadKeywords) {
      if (name.includes(keyword)) {
        return 1.0;
      }
    }
    
    return 0;
  }

  /**
   * Merge all detected road geometries into one
   */
  mergeRoadGeometries() {
    if (this.roadMeshes.length === 0) {
      console.warn('⚠️ No road meshes to merge');
      return null;
    }
    
    console.log('🔗 Merging road geometries...');
    
    const geometries = [];
    
    for (const mesh of this.roadMeshes) {
      // Clone geometry and apply world transform
      const geometry = mesh.geometry.clone();
      geometry.applyMatrix4(mesh.matrixWorld);
      
      // Ensure geometry is indexed and has normals
      if (!geometry.index) {
        geometry.computeVertexNormals();
      }
      
      geometries.push(geometry);
    }
    
    // Merge all geometries
    const mergedGeometry = THREE.BufferGeometryUtils.mergeGeometries(geometries, false);
    
    if (!mergedGeometry) {
      console.error('❌ Failed to merge geometries');
      return null;
    }
    
    // Simplify for NavMesh (reduce vertex count)
    // Note: three-pathfinding works best with simplified geometry
    console.log(`   Original vertices: ${mergedGeometry.attributes.position.count}`);
    
    return mergedGeometry;
  }

  /**
   * Create NavMesh from merged road geometry
   */
  createNavMesh(geometry) {
    console.log('🗺️ Creating NavMesh from geometry...');
    
    // Store road geometry for visualization
    this.roadGeometry = geometry;
    
    // Create a mesh for pathfinding
    const navMeshMesh = new THREE.Mesh(geometry);
    
    // Build the navigation mesh
    const zone = Pathfinding.createZone(geometry);
    this.pathfinding.setZoneData(this.zoneId, zone);
    
    this.navMesh = {
      mesh: navMeshMesh,
      zone: zone,
      geometry: geometry
    };
    
    console.log('✅ NavMesh created');
  }

  /**
   * Create fallback NavMesh (flat grid) when road detection fails
   */
  createFallbackNavMesh() {
    console.log('🔄 Creating fallback NavMesh (flat grid)...');
    
    // Create a large flat plane as fallback
    const size = 100;
    const segments = 20;
    const geometry = new THREE.PlaneGeometry(size, size, segments, segments);
    
    // Rotate to horizontal
    geometry.rotateX(-Math.PI / 2);
    
    // Create NavMesh
    this.createNavMesh(geometry);
    
    console.log('✅ Fallback NavMesh created');
  }

  /**
   * Find nearest point on NavMesh
   */
  getClosestNode(position) {
    if (!this.navMesh) return position;
    
    const group = this.pathfinding.getGroup(this.zoneId, position);
    const closestNode = this.pathfinding.getClosestNode(position, this.zoneId, group);
    
    return closestNode ? closestNode.centroid : position;
  }

  /**
   * Check if position is on NavMesh
   */
  isOnNavMesh(position, tolerance = 2.0) {
    if (!this.navMesh) return true; // Allow if no NavMesh
    
    const closestPoint = this.getClosestNode(position);
    const distance = position.distanceTo(closestPoint);
    
    return distance < tolerance;
  }

  /**
   * Clamp position to NavMesh
   */
  clampToNavMesh(position) {
    if (!this.navMesh) return position;
    
    const closestPoint = this.getClosestNode(position);
    return closestPoint;
  }

  /**
   * Find path between two points on NavMesh
   */
  findPath(start, end) {
    if (!this.navMesh) return [start, end];
    
    const startGroup = this.pathfinding.getGroup(this.zoneId, start);
    const endGroup = this.pathfinding.getGroup(this.zoneId, end);
    
    if (!startGroup || !endGroup) {
      console.warn('⚠️ Start or end position not on NavMesh');
      return [start, end];
    }
    
    const path = this.pathfinding.findPath(start, end, this.zoneId, startGroup);
    
    return path && path.length > 0 ? path : [start, end];
  }

  /**
   * Create visual debug mesh for roads
   */
  createDebugVisualization() {
    if (!this.roadGeometry) return null;
    
    const material = new THREE.MeshBasicMaterial({
      color: 0x00ff00,
      wireframe: true,
      transparent: true,
      opacity: 0.3
    });
    
    const debugMesh = new THREE.Mesh(this.roadGeometry, material);
    debugMesh.position.y += 0.1; // Slightly above ground
    
    return debugMesh;
  }

  /**
   * Get road boundaries for collision
   */
  getRoadBoundaries() {
    if (!this.roadGeometry) {
      // Fallback boundaries
      return {
        minX: -50,
        maxX: 50,
        minZ: -50,
        maxZ: 50,
        minY: -1,
        maxY: 10
      };
    }
    
    const bbox = new THREE.Box3().setFromBufferAttribute(
      this.roadGeometry.attributes.position
    );
    
    return {
      minX: bbox.min.x,
      maxX: bbox.max.x,
      minZ: bbox.min.z,
      maxZ: bbox.max.z,
      minY: bbox.min.y,
      maxY: bbox.max.y
    };
  }

  /**
   * Dispose resources
   */
  dispose() {
    if (this.roadGeometry) {
      this.roadGeometry.dispose();
    }
    
    this.roadMeshes = [];
    this.navMesh = null;
  }
}

export default RoadNavMesh;
