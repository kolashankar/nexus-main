import React from "react";
/**
 * React hook for managing Three.js scenes
 */

import { useEffect, useRef, useState } from 'react';
import { SceneManager } from '../services/3d/SceneManager';

export function use3DScene(canvasRef) {
  const sceneManagerRef = useRef(null);
  const [isReady, setIsReady] = useState(false);
  const animationFrameRef = useRef();

  useEffect(() => {
    if (!canvasRef.current) return;

    // Initialize scene
    sceneManagerRef.current = new SceneManager(canvasRef.current);
    setIsReady(true);

    // Cleanup
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      if (sceneManagerRef.current) {
        sceneManagerRef.current.dispose();
      }
    };
  }, [canvasRef]);

  const startAnimationLoop = (callback) => {
    if (!sceneManagerRef.current) return;

    let lastTime = performance.now();

    const animate = () => {
      const currentTime = performance.now();
      const deltaTime = (currentTime - lastTime) / 1000;
      lastTime = currentTime;

      callback(deltaTime);

      if (sceneManagerRef.current) {
        sceneManagerRef.current.render();
      }

      animationFrameRef.current = requestAnimationFrame(animate);
    };

    animate();
  };

  const stopAnimationLoop = () => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
  };

  return {
    sceneManager: sceneManagerRef.current,
    isReady,
    startAnimationLoop,
    stopAnimationLoop,
  };
}
