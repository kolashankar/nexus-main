import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useRef, useEffect } from 'react';
import { use3DScene } from '../../hooks/use3DScene';
/**
 * Base 3D Scene component
 * Provides a canvas and Three.js scene setup
 */
export const Scene3D = ({ children, onSceneReady, className = '' }) => {
    const canvasRef = useRef(null);
    const { sceneManager, isReady, startAnimationLoop } = use3DScene(canvasRef);
    useEffect(() => {
        if (isReady && sceneManager && onSceneReady) {
            onSceneReady(sceneManager);
        }
    }, [isReady, sceneManager, onSceneReady]);
    useEffect(() => {
        if (!sceneManager)
            return;
        startAnimationLoop((deltaTime) => {
            // Default animation loop
            // Children components can override this
        });
    }, [sceneManager, startAnimationLoop]);
    return (_jsxs("div", { className: `relative w-full h-full ${className}`, children: [_jsx("canvas", { ref: canvasRef, className: "w-full h-full", style: { display: 'block' } }), children] }));
};
