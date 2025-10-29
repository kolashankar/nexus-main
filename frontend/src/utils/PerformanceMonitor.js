/**
 * Performance Monitor for 3D Rendering
 * Tracks FPS, memory usage, and render statistics
 */
import * as THREE from 'three';

export class PerformanceMonitor {
  constructor(renderer, options = {}) {
    this.renderer = renderer;
    this.options = {
      targetFPS: options.targetFPS || 60,
      warnThreshold: options.warnThreshold || 0.8, // Warn if below 80% of target
      sampleSize: options.sampleSize || 60, // Number of frames to average
      showOverlay: options.showOverlay !== false,
      ...options
    };

    this.stats = {
      fps: 0,
      frameTime: 0,
      calls: 0,
      triangles: 0,
      points: 0,
      lines: 0,
      geometries: 0,
      textures: 0,
      memory: 0
    };

    this.frameTimes = [];
    this.lastTime = performance.now();
    this.overlay = null;

    if (this.options.showOverlay) {
      this.createOverlay();
    }
  }

  /**
   * Create performance overlay UI
   */
  createOverlay() {
    this.overlay = document.createElement('div');
    this.overlay.id = 'performance-monitor';
    this.overlay.style.cssText = `
      position: fixed;
      top: 10px;
      left: 10px;
      background: rgba(0, 0, 0, 0.8);
      color: #00ff00;
      font-family: 'Courier New', monospace;
      font-size: 12px;
      padding: 10px;
      border-radius: 5px;
      z-index: 10000;
      min-width: 200px;
      pointer-events: none;
      user-select: none;
    `;
    document.body.appendChild(this.overlay);
  }

  /**
   * Update performance statistics
   */
  update() {
    const currentTime = performance.now();
    const deltaTime = currentTime - this.lastTime;
    this.lastTime = currentTime;

    // Calculate FPS
    this.frameTimes.push(deltaTime);
    if (this.frameTimes.length > this.options.sampleSize) {
      this.frameTimes.shift();
    }

    const avgFrameTime = this.frameTimes.reduce((a, b) => a + b, 0) / this.frameTimes.length;
    this.stats.fps = Math.round(1000 / avgFrameTime);
    this.stats.frameTime = avgFrameTime.toFixed(2);

    // Get renderer info
    if (this.renderer && this.renderer.info) {
      const info = this.renderer.info;
      this.stats.calls = info.render.calls;
      this.stats.triangles = info.render.triangles;
      this.stats.points = info.render.points;
      this.stats.lines = info.render.lines;
      this.stats.geometries = info.memory.geometries;
      this.stats.textures = info.memory.textures;
    }

    // Get memory usage (if available)
    if (performance.memory) {
      this.stats.memory = Math.round(performance.memory.usedJSHeapSize / 1048576); // Convert to MB
    }

    // Update overlay
    if (this.overlay) {
      this.updateOverlay();
    }

    // Check for performance warnings
    this.checkPerformance();
  }

  /**
   * Update overlay display
   */
  updateOverlay() {
    const fpsColor = this.getFPSColor();
    
    this.overlay.innerHTML = `
      <div style="color: ${fpsColor}; font-weight: bold; font-size: 14px;">
        FPS: ${this.stats.fps} / ${this.options.targetFPS}
      </div>
      <div>Frame: ${this.stats.frameTime}ms</div>
      <hr style="border-color: #333; margin: 5px 0;">
      <div>Draw Calls: ${this.stats.calls}</div>
      <div>Triangles: ${this.formatNumber(this.stats.triangles)}</div>
      <div>Geometries: ${this.stats.geometries}</div>
      <div>Textures: ${this.stats.textures}</div>
      ${this.stats.memory > 0 ? `<div>Memory: ${this.stats.memory}MB</div>` : ''}
    `;
  }

  /**
   * Get color based on FPS performance
   */
  getFPSColor() {
    const ratio = this.stats.fps / this.options.targetFPS;
    if (ratio >= 0.9) return '#00ff00'; // Green - Excellent
    if (ratio >= 0.7) return '#ffff00'; // Yellow - Good
    if (ratio >= 0.5) return '#ff9900'; // Orange - Fair
    return '#ff0000'; // Red - Poor
  }

  /**
   * Check for performance issues
   */
  checkPerformance() {
    const minFPS = this.options.targetFPS * this.options.warnThreshold;
    
    if (this.stats.fps < minFPS) {
      console.warn(`⚠️ Performance Warning: FPS dropped to ${this.stats.fps} (target: ${this.options.targetFPS})`);
      console.warn(`   Draw Calls: ${this.stats.calls}, Triangles: ${this.formatNumber(this.stats.triangles)}`);
    }
  }

  /**
   * Format large numbers
   */
  formatNumber(num) {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  }

  /**
   * Get current statistics
   */
  getStats() {
    return { ...this.stats };
  }

  /**
   * Check if performance is acceptable
   */
  isPerformanceGood() {
    return this.stats.fps >= (this.options.targetFPS * this.options.warnThreshold);
  }

  /**
   * Get performance grade
   */
  getPerformanceGrade() {
    const ratio = this.stats.fps / this.options.targetFPS;
    if (ratio >= 0.9) return 'A';
    if (ratio >= 0.8) return 'B';
    if (ratio >= 0.7) return 'C';
    if (ratio >= 0.5) return 'D';
    return 'F';
  }

  /**
   * Reset statistics
   */
  reset() {
    this.frameTimes = [];
    this.lastTime = performance.now();
  }

  /**
   * Dispose and cleanup
   */
  dispose() {
    if (this.overlay && this.overlay.parentNode) {
      this.overlay.parentNode.removeChild(this.overlay);
    }
    this.overlay = null;
  }

  /**
   * Toggle overlay visibility
   */
  toggleOverlay() {
    if (this.overlay) {
      this.overlay.style.display = this.overlay.style.display === 'none' ? 'block' : 'none';
    }
  }

  /**
   * Show/hide overlay
   */
  showOverlay(show = true) {
    if (this.overlay) {
      this.overlay.style.display = show ? 'block' : 'none';
    }
  }

  /**
   * Get recommendations for performance improvement
   */
  getRecommendations() {
    const recommendations = [];

    if (this.stats.calls > 100) {
      recommendations.push('Reduce draw calls by merging geometries or using instancing');
    }

    if (this.stats.triangles > 1000000) {
      recommendations.push('Reduce triangle count using LOD or geometry simplification');
    }

    if (this.stats.textures > 50) {
      recommendations.push('Reduce texture count by using texture atlases');
    }

    if (this.stats.memory > 500) {
      recommendations.push('Memory usage is high - consider reducing texture sizes or geometry complexity');
    }

    if (this.stats.fps < this.options.targetFPS * 0.5) {
      recommendations.push('Critical performance issue - consider disabling shadows, reducing render distance, or lowering quality settings');
    }

    return recommendations;
  }
}

export default PerformanceMonitor;
