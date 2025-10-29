/**
 * RoadDetector - Automatically detects road surfaces in a 3D city model
 * Uses heuristics: color, texture, flatness, height level
 */
import * as THREE from 'three';
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

export class RoadDetector {
  constructor(cityModel, options = {}) {
    this.cityModel = cityModel;
    this.options = {
      // Color detection - typical asphalt/road colors
      roadColorMin: options.roadColorMin || 0x1a1a1a,  // Dark gray
      roadColorMax: options.roadColorMax || 0x606060,  // Medium gray
      colorTolerance: options.colorTolerance || 0.3,
      
      // Flatness detection
      minFlatness: options.minFlatness || 0.85, // How horizontal (0=vertical, 1=horizontal)
      
      // Height detection
      minHeight: options.minHeight || -2,  // Minimum Y position
      maxHeight: options.maxHeight || 2,   // Maximum Y position
      
      // Name patterns (if meshes are named)
      namePatterns: options.namePatterns || [
        'road', 'street', 'asphalt', 'path', 'pavement',
        'highway', 'lane', 'avenue', 'boulevard'
      ],
      
      debug: options.debug !== undefined ? options.debug : true
    };
    
    this.detectedRoads = [];
    this.roadMeshes = [];
  }

  /**
   * Analyze city model and detect all road surfaces
   */
  detectRoads() {
    console.log('🔍 Starting road detection...');
    const startTime = Date.now();
    
    this.roadMeshes = [];
    const candidateMeshes = [];
    
    // Traverse entire city model
    this.cityModel.traverse((child) => {
      if (child.isMesh) {
        const score = this.evaluateRoadMesh(child);
        
        if (score.isRoad) {
          candidateMeshes.push({
            mesh: child,
            score: score.confidence,
            reasons: score.reasons
          });
        }
      }
    });
    
    // Sort by confidence and select high-confidence roads
    candidateMeshes.sort((a, b) => b.score - a.score);
    
    candidateMeshes.forEach(candidate => {
      if (candidate.score >= 0.5) { // 50% confidence threshold
        this.roadMeshes.push(candidate.mesh);
        
        if (this.options.debug) {
          console.log(`✅ Road detected: ${candidate.mesh.name || 'unnamed'}`);
          console.log(`   Confidence: ${(candidate.score * 100).toFixed(1)}%`);
          console.log(`   Reasons: ${candidate.reasons.join(', ')}`);
        }
      }
    });
    
    const duration = Date.now() - startTime;
    console.log(`✅ Road detection complete: ${this.roadMeshes.length} roads found in ${duration}ms`);
    
    return this.roadMeshes;
  }

  /**
   * Evaluate if a mesh is likely to be a road
   * Returns { isRoad: boolean, confidence: number (0-1), reasons: string[] }
   */
  evaluateRoadMesh(mesh) {
    let confidence = 0;
    const reasons = [];
    const weights = {
      name: 0.3,
      color: 0.25,
      flatness: 0.25,
      height: 0.2
    };
    
    // 1. Check mesh name
    const nameScore = this.checkMeshName(mesh);
    if (nameScore > 0) {
      confidence += nameScore * weights.name;
      reasons.push('name match');
    }
    
    // 2. Check material color
    const colorScore = this.checkMeshColor(mesh);
    if (colorScore > 0) {
      confidence += colorScore * weights.color;
      reasons.push('color match');
    }
    
    // 3. Check flatness (horizontal surface)
    const flatnessScore = this.checkMeshFlatness(mesh);
    if (flatnessScore > 0) {
      confidence += flatnessScore * weights.flatness;
      reasons.push('flat surface');
    }
    
    // 4. Check height (ground level)
    const heightScore = this.checkMeshHeight(mesh);
    if (heightScore > 0) {
      confidence += heightScore * weights.height;
      reasons.push('ground level');
    }
    
    return {
      isRoad: confidence > 0.3, // Require at least 30% confidence
      confidence,
      reasons
    };
  }

  /**
   * Check if mesh name suggests it's a road
   */
  checkMeshName(mesh) {
    if (!mesh.name) return 0;
    
    const lowerName = mesh.name.toLowerCase();
    for (const pattern of this.options.namePatterns) {
      if (lowerName.includes(pattern)) {
        return 1.0; // Perfect match
      }
    }
    return 0;
  }

  /**
   * Check if mesh material color matches typical road colors
   */
  checkMeshColor(mesh) {
    if (!mesh.material) return 0;
    
    const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
    let maxScore = 0;
    
    for (const material of materials) {
      if (material.color) {
        const color = material.color;
        const colorHex = color.getHex();
        
        // Check if color is in road color range (grays/darks)
        const { roadColorMin, roadColorMax } = this.options;
        
        if (colorHex >= roadColorMin && colorHex <= roadColorMax) {
          maxScore = Math.max(maxScore, 1.0);
        } else {
          // Check if it's grayscale (R ≈ G ≈ B)
          const r = color.r;
          const g = color.g;
          const b = color.b;
          const avg = (r + g + b) / 3;
          const variance = Math.abs(r - avg) + Math.abs(g - avg) + Math.abs(b - avg);
          
          if (variance < 0.1 && avg < 0.5) { // Low variance + dark = likely road
            maxScore = Math.max(maxScore, 0.8);
          }
        }
      }
      
      // Check texture map for asphalt-like patterns
      if (material.map) {
        // Roads often have darker textures
        maxScore = Math.max(maxScore, 0.5);
      }
    }
    
    return maxScore;
  }

  /**
   * Check if mesh is flat/horizontal
   */
  checkMeshFlatness(mesh) {
    if (!mesh.geometry) return 0;
    
    // Calculate average normal direction
    const geometry = mesh.geometry;
    if (!geometry.attributes.normal) {
      geometry.computeVertexNormals();
    }
    
    const normals = geometry.attributes.normal;
    let upDotSum = 0;
    const up = new THREE.Vector3(0, 1, 0);
    const worldNormal = new THREE.Vector3();
    
    // Sample normals to determine flatness
    const sampleCount = Math.min(100, normals.count);
    const step = Math.floor(normals.count / sampleCount);
    
    for (let i = 0; i < normals.count; i += step) {
      worldNormal.set(
        normals.getX(i),
        normals.getY(i),
        normals.getZ(i)
      );
      
      // Transform normal to world space
      worldNormal.applyMatrix4(mesh.matrixWorld);
      worldNormal.normalize();
      
      // Calculate how much it points up
      upDotSum += Math.abs(worldNormal.dot(up));
    }
    
    const avgUpDot = upDotSum / sampleCount;
    
    // Score based on how horizontal the surface is
    if (avgUpDot >= this.options.minFlatness) {
      return avgUpDot;
    }
    
    return 0;
  }

  /**
   * Check if mesh is at ground level
   */
  checkMeshHeight(mesh) {
    // Get mesh world position
    const position = new THREE.Vector3();
    mesh.getWorldPosition(position);
    
    // Get bounding box to find actual height range
    const box = new THREE.Box3().setFromObject(mesh);
    const minY = box.min.y;
    const maxY = box.max.y;
    const avgY = (minY + maxY) / 2;
    
    // Check if mesh is at ground level
    if (avgY >= this.options.minHeight && avgY <= this.options.maxHeight) {
      // Calculate score based on how close to ideal ground level (0)
      const distanceFromGround = Math.abs(avgY);
      const maxDistance = Math.max(
        Math.abs(this.options.minHeight),
        Math.abs(this.options.maxHeight)
      );
      return 1.0 - (distanceFromGround / maxDistance);
    }
    
    return 0;
  }

  /**
   * Get all detected road meshes
   */
  getRoadMeshes() {
    return this.roadMeshes;
  }

  /**
   * Create a merged geometry from all road meshes for NavMesh generation
   */
  getMergedRoadGeometry() {
    if (this.roadMeshes.length === 0) {
      console.warn('⚠️ No roads detected, cannot create merged geometry');
      return null;
    }
    
    const geometries = [];
    
    this.roadMeshes.forEach(mesh => {
      const geometry = mesh.geometry.clone();
      geometry.applyMatrix4(mesh.matrixWorld);
      geometries.push(geometry);
    });
    
    // Merge all geometries
    try {
      const mergedGeometry = mergeGeometries(geometries);
      return mergedGeometry;
    } catch (error) {
      console.warn('⚠️ Error merging geometries:', error);
      return geometries[0]; // Fallback to first geometry
    }
  }

  /**
   * Get bounding box of all detected roads
   */
  getRoadBoundingBox() {
    if (this.roadMeshes.length === 0) return null;
    
    const box = new THREE.Box3();
    this.roadMeshes.forEach(mesh => {
      box.expandByObject(mesh);
    });
    
    return box;
  }
}

export default RoadDetector;
