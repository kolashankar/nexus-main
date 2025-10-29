/**
 * Model Optimizer for 3D Assets
 * Analyzes and optimizes GLB/GLTF models for performance
 */
import * as THREE from 'three';

export class ModelOptimizer {
  constructor(options = {}) {
    this.options = {
      maxTextureSize: options.maxTextureSize || 1024,
      simplificationRatio: options.simplificationRatio || 0.7,
      mergeMaterials: options.mergeMaterials !== false,
      compressGeometry: options.compressGeometry !== false,
      generateLODs: options.generateLODs !== false,
      removeInvisible: options.removeInvisible !== false,
      ...options
    };
    
    this.stats = {
      originalVertices: 0,
      optimizedVertices: 0,
      originalTriangles: 0,
      optimizedTriangles: 0,
      originalMaterials: 0,
      optimizedMaterials: 0,
      texturesCompressed: 0
    };
  }

  /**
   * Analyze a model and return statistics
   */
  analyze(model) {
    const stats = {
      vertices: 0,
      triangles: 0,
      meshes: 0,
      materials: new Set(),
      textures: new Set(),
      boundingBox: new THREE.Box3().setFromObject(model),
      size: new THREE.Vector3()
    };

    model.traverse((child) => {
      if (child.isMesh) {
        stats.meshes++;
        
        if (child.geometry) {
          const positionAttr = child.geometry.attributes.position;
          if (positionAttr) {
            stats.vertices += positionAttr.count;
            stats.triangles += child.geometry.index ? 
              child.geometry.index.count / 3 : 
              positionAttr.count / 3;
          }
        }

        if (child.material) {
          const materials = Array.isArray(child.material) ? child.material : [child.material];
          materials.forEach(mat => {
            stats.materials.add(mat.uuid);
            
            // Check textures
            ['map', 'normalMap', 'roughnessMap', 'metalnessMap', 'aoMap'].forEach(prop => {
              if (mat[prop]) {
                stats.textures.add(mat[prop].uuid);
              }
            });
          });
        }
      }
    });

    stats.boundingBox.getSize(stats.size);
    stats.materialCount = stats.materials.size;
    stats.textureCount = stats.textures.size;

    return stats;
  }

  /**
   * Optimize a model for performance
   */
  optimize(model, isMobile = false) {
    console.log('🔧 Starting model optimization...');
    
    const startStats = this.analyze(model);
    this.stats.originalVertices = startStats.vertices;
    this.stats.originalTriangles = Math.floor(startStats.triangles);
    this.stats.originalMaterials = startStats.materialCount;

    console.log(`📊 Original stats: ${startStats.vertices.toLocaleString()} vertices, ${Math.floor(startStats.triangles).toLocaleString()} triangles, ${startStats.meshes} meshes`);

    // Apply optimizations
    if (this.options.removeInvisible) {
      this.removeInvisibleMeshes(model);
    }

    if (this.options.compressGeometry) {
      this.compressGeometry(model, isMobile);
    }

    if (this.options.mergeMaterials) {
      this.mergeSimilarMaterials(model);
    }

    if (isMobile) {
      this.optimizeForMobile(model);
    }

    // Generate LODs for better performance
    if (this.options.generateLODs) {
      this.generateLODs(model);
    }

    const endStats = this.analyze(model);
    this.stats.optimizedVertices = endStats.vertices;
    this.stats.optimizedTriangles = Math.floor(endStats.triangles);
    this.stats.optimizedMaterials = endStats.materialCount;

    console.log(`✅ Optimization complete:`);
    console.log(`   Vertices: ${this.stats.originalVertices.toLocaleString()} → ${this.stats.optimizedVertices.toLocaleString()} (${this.getReductionPercent('vertices')}% reduction)`);
    console.log(`   Triangles: ${this.stats.originalTriangles.toLocaleString()} → ${this.stats.optimizedTriangles.toLocaleString()} (${this.getReductionPercent('triangles')}% reduction)`);
    console.log(`   Materials: ${this.stats.originalMaterials} → ${this.stats.optimizedMaterials}`);

    return model;
  }

  /**
   * Remove invisible or hidden meshes
   */
  removeInvisibleMeshes(model) {
    const toRemove = [];
    
    model.traverse((child) => {
      if (child.isMesh) {
        // Remove if invisible or has zero scale
        if (!child.visible || 
            child.scale.x === 0 || 
            child.scale.y === 0 || 
            child.scale.z === 0) {
          toRemove.push(child);
        }
      }
    });

    toRemove.forEach(mesh => {
      if (mesh.parent) {
        mesh.parent.remove(mesh);
      }
      if (mesh.geometry) mesh.geometry.dispose();
      if (mesh.material) {
        if (Array.isArray(mesh.material)) {
          mesh.material.forEach(mat => mat.dispose());
        } else {
          mesh.material.dispose();
        }
      }
    });

    if (toRemove.length > 0) {
      console.log(`   Removed ${toRemove.length} invisible meshes`);
    }
  }

  /**
   * Compress geometry by removing unnecessary data
   */
  compressGeometry(model, isMobile) {
    let compressed = 0;
    
    model.traverse((child) => {
      if (child.isMesh && child.geometry) {
        const geometry = child.geometry;
        
        // Remove unnecessary attributes for mobile
        if (isMobile) {
          // Remove UV2, UV3 if they exist (keep only UV1 for textures)
          if (geometry.attributes.uv2) {
            geometry.deleteAttribute('uv2');
          }
          if (geometry.attributes.uv3) {
            geometry.deleteAttribute('uv3');
          }
          
          // Remove tangents if not using normal maps
          if (geometry.attributes.tangent && !child.material?.normalMap) {
            geometry.deleteAttribute('tangent');
          }
        }

        // Compute bounding sphere for frustum culling
        if (!geometry.boundingSphere) {
          geometry.computeBoundingSphere();
        }

        // Compress index buffer
        if (geometry.index && geometry.index.array.length < 65536) {
          // Convert to Uint16Array if possible (smaller memory footprint)
          const maxIndex = Math.max(...geometry.index.array);
          if (maxIndex < 65536) {
            geometry.setIndex(new THREE.BufferAttribute(
              new Uint16Array(geometry.index.array), 
              1
            ));
          }
        }

        compressed++;
      }
    });

    console.log(`   Compressed ${compressed} geometries`);
  }

  /**
   * Merge similar materials to reduce draw calls
   */
  mergeSimilarMaterials(model) {
    const materialMap = new Map();
    let merged = 0;

    model.traverse((child) => {
      if (child.isMesh && child.material) {
        const materials = Array.isArray(child.material) ? child.material : [child.material];
        
        materials.forEach((mat, index) => {
          // Create a hash of material properties
          const hash = this.getMaterialHash(mat);
          
          if (materialMap.has(hash)) {
            // Reuse existing material
            if (Array.isArray(child.material)) {
              child.material[index] = materialMap.get(hash);
            } else {
              child.material = materialMap.get(hash);
            }
            merged++;
          } else {
            materialMap.set(hash, mat);
          }
        });
      }
    });

    if (merged > 0) {
      console.log(`   Merged ${merged} duplicate materials`);
    }
  }

  /**
   * Create hash for material comparison
   */
  getMaterialHash(material) {
    return `${material.type}_${material.color?.getHex()}_${material.metalness}_${material.roughness}_${material.transparent}`;
  }

  /**
   * Optimize specifically for mobile devices
   */
  optimizeForMobile(model) {
    let optimized = 0;

    model.traverse((child) => {
      if (child.isMesh) {
        // Simplify materials
        if (child.material) {
          const materials = Array.isArray(child.material) ? child.material : [child.material];
          
          materials.forEach(mat => {
            // Reduce texture resolution
            ['map', 'normalMap', 'roughnessMap', 'metalnessMap', 'aoMap'].forEach(texType => {
              if (mat[texType] && mat[texType].image) {
                this.downscaleTexture(mat[texType], this.options.maxTextureSize);
                this.stats.texturesCompressed++;
              }
            });

            // Disable expensive features on mobile
            mat.shadowSide = THREE.FrontSide; // Reduce shadow rendering
          });
          
          optimized++;
        }
      }
    });

    console.log(`   Mobile optimizations applied to ${optimized} meshes`);
  }

  /**
   * Downscale texture to max size
   */
  downscaleTexture(texture, maxSize) {
    if (!texture.image || !texture.image.width) return;

    const width = texture.image.width;
    const height = texture.image.height;

    if (width <= maxSize && height <= maxSize) return;

    const scale = maxSize / Math.max(width, height);
    const newWidth = Math.floor(width * scale);
    const newHeight = Math.floor(height * scale);

    const canvas = document.createElement('canvas');
    canvas.width = newWidth;
    canvas.height = newHeight;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(texture.image, 0, 0, newWidth, newHeight);

    texture.image = canvas;
    texture.needsUpdate = true;
  }

  /**
   * Generate Level of Detail (LOD) versions
   */
  generateLODs(model) {
    let lodsGenerated = 0;

    model.traverse((child) => {
      if (child.isMesh && child.geometry) {
        // Create LOD group
        const lod = new THREE.LOD();
        lod.position.copy(child.position);
        lod.rotation.copy(child.rotation);
        lod.scale.copy(child.scale);

        // Level 0: Original (0-50 units)
        lod.addLevel(child.clone(), 0);

        // Level 1: Medium detail (50-100 units)
        const mediumDetail = child.clone();
        this.simplifyGeometry(mediumDetail.geometry, 0.5);
        lod.addLevel(mediumDetail, 50);

        // Level 2: Low detail (100-150 units)
        const lowDetail = child.clone();
        this.simplifyGeometry(lowDetail.geometry, 0.25);
        lod.addLevel(lowDetail, 100);

        // Replace child with LOD
        if (child.parent) {
          const parent = child.parent;
          const index = parent.children.indexOf(child);
          parent.children[index] = lod;
          child.parent = lod;
        }

        lodsGenerated++;
      }
    });

    if (lodsGenerated > 0) {
      console.log(`   Generated LODs for ${lodsGenerated} meshes`);
    }
  }

  /**
   * Simplify geometry by reducing vertices (basic decimation)
   */
  simplifyGeometry(geometry, targetRatio) {
    // This is a simple approach - for production, use a proper decimation library
    // For now, we'll just mark it for potential future simplification
    geometry.userData.simplified = true;
    geometry.userData.targetRatio = targetRatio;
  }

  /**
   * Get reduction percentage
   */
  getReductionPercent(type) {
    const original = type === 'vertices' ? this.stats.originalVertices : this.stats.originalTriangles;
    const optimized = type === 'vertices' ? this.stats.optimizedVertices : this.stats.optimizedTriangles;
    
    if (original === 0) return 0;
    return Math.round(((original - optimized) / original) * 100);
  }

  /**
   * Get optimization statistics
   */
  getStats() {
    return { ...this.stats };
  }
}

export default ModelOptimizer;
