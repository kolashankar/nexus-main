import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
/**
 * 3D Scene component
 */
import { useEffect } from 'react';
import { use3DScene } from '../../../hooks/use3DScene';
import * as THREE from 'three';
const Scene = ({ className = '' }) => {
    const { containerRef, scene, camera, isReady } = use3DScene({
        antialias: true,
        alpha: false,
    });
    useEffect(() => {
        if (!scene || !isReady)
            return;
        // Add a simple cube as placeholder
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshStandardMaterial({
            color: 0x00ff88,
            metalness: 0.5,
            roughness: 0.5,
        });
        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);
        // Animate cube
        const animate = () => {
            cube.rotation.x += 0.01;
            cube.rotation.y += 0.01;
        };
        const interval = setInterval(animate, 16);
        return () => {
            clearInterval(interval);
            scene.remove(cube);
            geometry.dispose();
            material.dispose();
        };
    }, [scene, isReady]);
    return (_jsx("div", { ref: containerRef, className: `w-full h-full ${className}`, style: { minHeight: '400px' } }));
};
export default Scene;