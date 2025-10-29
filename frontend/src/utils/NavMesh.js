/**
 * NavMesh - Navigation mesh for constraining movement to valid areas (roads)
 * Provides pathfinding and nearest-point lookup
 */
import * as THREE from 'three';

export class NavMesh {
  constructor(roadMeshes, options = {}) {
    this.roadMeshes = roadMeshes;
    this.options = {
      gridSize: options.gridSize || 0.5,        // Grid resolution (smaller = more accurate)
      maxRaycastHeight: options.maxRaycastHeight || 10,  // Height to cast rays from
      minRaycastHeight: options.minRaycastHeight || -2,  // Minimum height to check
      debug: options.debug !== undefined ? options.debug : true
    };
    
    this.walkablePoints = [];  // Array of walkable points
    this.spatialGrid = new Map();  // Spatial hash for fast lookup
    this.gridCellSize = 5;  // Size of spatial hash cells
    this.bounds = null;
    this.raycaster = new THREE.Raycaster();
  }

  /**
   * Generate navigation mesh from road meshes
   */
  generate() {
    console.log('🗺️ Generating NavMesh...');
    const startTime = Date.now();
    
    if (!this.roadMeshes || this.roadMeshes.length === 0) {
      console.error('❌ No road meshes provided for NavMesh generation');
      return false;
    }
    
    // Calculate bounding box
    this.bounds = new THREE.Box3();
    this.roadMeshes.forEach(mesh => {
      this.bounds.expandByObject(mesh);
    });
    
    const size = new THREE.Vector3();
    this.bounds.getSize(size);
    
    console.log(`📐 NavMesh bounds: ${size.x.toFixed(1)}x${size.z.toFixed(1)}m`);
    
    // Generate grid of potential walkable points
    this.generateWalkableGrid();
    
    // Build spatial index
    this.buildSpatialIndex();
    
    const duration = Date.now() - startTime;
    console.log(`✅ NavMesh generated: ${this.walkablePoints.length} walkable points in ${duration}ms`);
    
    return true;
  }

  /**
   * Generate grid of walkable points using raycasting
   */
  generateWalkableGrid() {
    const { minX, maxX, minZ, maxZ } = {
      minX: this.bounds.min.x,
      maxX: this.bounds.max.x,
      minZ: this.bounds.min.z,
      maxZ: this.bounds.max.z
    };
    
    const { gridSize, maxRaycastHeight, minRaycastHeight } = this.options;
    const rayOrigin = new THREE.Vector3();
    const rayDirection = new THREE.Vector3(0, -1, 0);  // Cast downward
    
    let totalTests = 0;
    let walkableFound = 0;
    
    // Test grid points
    for (let x = minX; x <= maxX; x += gridSize) {
      for (let z = minZ; z <= maxZ; z += gridSize) {
        totalTests++;
        
        // Cast ray downward from above
        rayOrigin.set(x, maxRaycastHeight, z);
        this.raycaster.set(rayOrigin, rayDirection);
        
        // Check intersection with road meshes
        const intersects = this.raycaster.intersectObjects(this.roadMeshes, false);
        
        if (intersects.length > 0) {
          const hit = intersects[0];
          
          // Verify hit is at valid height
          if (hit.point.y >= minRaycastHeight && hit.point.y <= maxRaycastHeight) {
            this.walkablePoints.push({
              x: hit.point.x,
              y: hit.point.y,
              z: hit.point.z,
              normal: hit.face ? hit.face.normal.clone() : new THREE.Vector3(0, 1, 0)
            });
            walkableFound++;
          }
        }
      }
    }
    
    console.log(`   Tested ${totalTests} points, found ${walkableFound} walkable`);
  }

  /**
   * Build spatial hash grid for fast nearest-point lookup
   */
  buildSpatialIndex() {
    this.spatialGrid.clear();
    
    this.walkablePoints.forEach((point, index) => {
      const cellKey = this.getSpatialCellKey(point.x, point.z);
      
      if (!this.spatialGrid.has(cellKey)) {
        this.spatialGrid.set(cellKey, []);
      }
      
      this.spatialGrid.get(cellKey).push(index);
    });
    
    console.log(`   Spatial index: ${this.spatialGrid.size} cells`);
  }

  /**
   * Get spatial cell key for a position
   */
  getSpatialCellKey(x, z) {
    const cellX = Math.floor(x / this.gridCellSize);
    const cellZ = Math.floor(z / this.gridCellSize);
    return `${cellX},${cellZ}`;
  }

  /**
   * Get neighboring cell keys
   */
  getNeighborCellKeys(x, z) {
    const cellX = Math.floor(x / this.gridCellSize);
    const cellZ = Math.floor(z / this.gridCellSize);
    
    const keys = [];
    for (let dx = -1; dx <= 1; dx++) {
      for (let dz = -1; dz <= 1; dz++) {
        keys.push(`${cellX + dx},${cellZ + dz}`);
      }
    }
    return keys;
  }

  /**
   * Check if a point is on the navigation mesh
   */
  isPointOnNavMesh(x, z, tolerance = 0.5) {
    return this.getNearestPoint(x, z, tolerance) !== null;
  }

  /**
   * Get nearest walkable point on the NavMesh
   * Returns { x, y, z } or null if none found within maxDistance
   */
  getNearestPoint(x, z, maxDistance = 5) {
    if (this.walkablePoints.length === 0) return null;
    
    // Use spatial grid for fast lookup
    const cellKeys = this.getNeighborCellKeys(x, z);
    const candidateIndices = new Set();
    
    cellKeys.forEach(key => {
      const indices = this.spatialGrid.get(key);
      if (indices) {
        indices.forEach(idx => candidateIndices.add(idx));
      }
    });
    
    // Find closest point among candidates
    let nearestPoint = null;
    let nearestDistSq = maxDistance * maxDistance;
    
    candidateIndices.forEach(idx => {
      const point = this.walkablePoints[idx];
      const dx = point.x - x;
      const dz = point.z - z;
      const distSq = dx * dx + dz * dz;
      
      if (distSq < nearestDistSq) {
        nearestDistSq = distSq;
        nearestPoint = point;
      }
    });
    
    // Fallback to brute force if no candidates found
    if (!nearestPoint && candidateIndices.size === 0) {
      this.walkablePoints.forEach(point => {
        const dx = point.x - x;
        const dz = point.z - z;
        const distSq = dx * dx + dz * dz;
        
        if (distSq < nearestDistSq) {
          nearestDistSq = distSq;
          nearestPoint = point;
        }
      });
    }
    
    return nearestPoint ? { 
      x: nearestPoint.x, 
      y: nearestPoint.y, 
      z: nearestPoint.z 
    } : null;
  }

  /**
   * Get height at a specific XZ position using raycasting
   */
  getHeightAt(x, z) {
    const rayOrigin = new THREE.Vector3(x, this.options.maxRaycastHeight, z);
    const rayDirection = new THREE.Vector3(0, -1, 0);
    
    this.raycaster.set(rayOrigin, rayDirection);
    const intersects = this.raycaster.intersectObjects(this.roadMeshes, false);
    
    if (intersects.length > 0) {
      return intersects[0].point.y;
    }
    
    return null;
  }

  /**
   * Simple A* pathfinding between two points on the NavMesh
   */
  findPath(startX, startZ, endX, endZ) {
    // For now, return direct path if both points are on navmesh
    // Full A* implementation would be more complex
    const startPoint = this.getNearestPoint(startX, startZ);
    const endPoint = this.getNearestPoint(endX, endZ);
    
    if (!startPoint || !endPoint) {
      return null;
    }
    
    // Simple straight-line path (can be enhanced with A* later)
    return [
      { x: startPoint.x, y: startPoint.y, z: startPoint.z },
      { x: endPoint.x, y: endPoint.y, z: endPoint.z }
    ];
  }

  /**
   * Get smooth path along roads using waypoints
   */
  getSmoothPath(startX, startZ, endX, endZ, segments = 10) {
    const startPoint = this.getNearestPoint(startX, startZ);
    const endPoint = this.getNearestPoint(endX, endZ);
    
    if (!startPoint || !endPoint) {
      return null;
    }
    
    const path = [];
    
    // Generate intermediate waypoints
    for (let i = 0; i <= segments; i++) {
      const t = i / segments;
      const x = startPoint.x + (endPoint.x - startPoint.x) * t;
      const z = startPoint.z + (endPoint.z - startPoint.z) * t;
      
      // Snap each waypoint to nearest road point
      const waypoint = this.getNearestPoint(x, z);
      if (waypoint) {
        path.push(waypoint);
      }
    }
    
    return path;
  }

  /**
   * Get all walkable points (for debug visualization)
   */
  getWalkablePoints() {
    return this.walkablePoints;
  }

  /**
   * Get bounds of the NavMesh
   */
  getBounds() {
    return this.bounds;
  }

  /**
   * Create debug visualization mesh
   */
  createDebugVisualization() {
    if (this.walkablePoints.length === 0) return null;
    
    const geometry = new THREE.BufferGeometry();
    const positions = [];
    
    // Create points for each walkable location
    this.walkablePoints.forEach(point => {
      positions.push(point.x, point.y + 0.1, point.z);  // Slightly above ground
    });
    
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    
    const material = new THREE.PointsMaterial({
      color: 0xffff00,  // Yellow
      size: 0.3,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.6
    });
    
    return new THREE.Points(geometry, material);
  }
}

export default NavMesh;
