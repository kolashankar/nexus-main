import React from "react";
import { useEffect } from 'react';
import { use3DModel } from '../../hooks/use3DModel';
/**
 * 3D Model component
 * Loads and displays a 3D model in the scene
 */
export const Model3D = ({ modelUrl, position = [0, 0, 0], rotation = [0, 0, 0], scale = [1, 1, 1], onLoad, onError, sceneManager, autoPlay = true, initialAnimation }) => {
    const { asset, loading, error, animationController } = use3DModel(modelUrl);
    // Add model to scene when loaded
    useEffect(() => {
        if (!asset || !sceneManager)
            return;
        const model = asset.model;
        // Set transform
        model.position.set(...position);
        model.rotation.set(...rotation);
        model.scale.set(...scale);
        // Add to scene
        sceneManager.addObject(modelUrl, model);
        // Play initial animation
        if (autoPlay && initialAnimation && animationController) {
            animationController.play(initialAnimation);
        }
        // Callback
        if (onLoad) {
            onLoad(model);
        }
        // Cleanup
        return () => {
            sceneManager.removeObject(modelUrl);
        };
    }, [asset, sceneManager, position, rotation, scale, modelUrl, autoPlay, initialAnimation, animationController, onLoad]);
    // Handle errors
    useEffect(() => {
        if (error && onError) {
            onError(error);
        }
    }, [error, onError]);
    // Update animation
    useEffect(() => {
        if (!animationController || !sceneManager)
            return;
        const animate = (deltaTime) => {
            animationController.update(deltaTime);
        };
        sceneManager.startAnimationLoop?.(animate);
    }, [animationController, sceneManager]);
    if (loading) {
        return null; // Or show loading indicator
    }
    if (error) {
        console.error('Model loading error:', error);
        return null; // Or show error state
    }
    return null; // Component renders to Three.js scene, not DOM
};
