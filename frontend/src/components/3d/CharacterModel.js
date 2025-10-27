import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Model3D } from './Model3D';
import { MODEL_PATHS } from '../../services/3d/ModelPaths';
/**
 * Character Model component
 * Specialized component for player characters
 */
export const CharacterModel = ({ gender, bodyType = 'base', position, rotation, scale = [1, 1, 1], animation = 'idle', sceneManager, onLoad }) => {
    const [modelUrl, setModelUrl] = useState('');
    useEffect(() => {
        // Get character model path
        const path = MODEL_PATHS.characters[gender][bodyType];
        setModelUrl(path);
    }, [gender, bodyType]);
    if (!modelUrl)
        return null;
    return (_jsx(Model3D, { modelUrl: modelUrl, position: position, rotation: rotation, scale: scale, initialAnimation: animation, autoPlay: true, sceneManager: sceneManager, onLoad: onLoad }));
};
