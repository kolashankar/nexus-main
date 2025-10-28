/**
 * WorldItemMarker - 3D marker for world items in the game
 */

import React, { useRef, useState } from 'react';
import { Html } from '@react-three/drei';
import * as THREE from 'three';

const WorldItemMarker = ({ item, onInteract, playerDistance }) => {
  const meshRef = useRef();
  const [hovered, setHovered] = useState(false);

  // Determine color based on item type
  const getItemColor = () => {
    switch (item.item_type) {
      case 'skill':
        return '#3b82f6'; // Blue
      case 'superpower_tool':
        return '#8b5cf6'; // Purple
      case 'meta_trait':
        return '#f59e0b'; // Amber
      default:
        return '#6b7280'; // Gray
    }
  };

  // Determine size based on rarity
  const getItemSize = () => {
    switch (item.rarity) {
      case 'common':
        return 1.0;
      case 'uncommon':
        return 1.2;
      case 'rare':
        return 1.5;
      case 'epic':
        return 1.8;
      case 'legendary':
        return 2.0;
      default:
        return 1.0;
    }
  };

  // Floating animation
  React.useEffect(() => {
    if (!meshRef.current) return;

    let animationId;
    const animate = () => {
      if (meshRef.current) {
        meshRef.current.position.y = item.position.y + Math.sin(Date.now() * 0.001) * 0.3;
        meshRef.current.rotation.y += 0.01;
      }
      animationId = requestAnimationFrame(animate);
    };

    animate();
    return () => cancelAnimationFrame(animationId);
  }, [item.position.y]);

  const size = getItemSize();
  const color = getItemColor();
  const isNearby = playerDistance !== undefined && playerDistance < 5;

  return (
    <group position={[item.position.x, item.position.y, item.position.z]}>
      {/* Main item mesh */}
      <mesh
        ref={meshRef}
        onClick={() => onInteract && onInteract(item)}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <octahedronGeometry args={[size, 0]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={hovered ? 0.8 : 0.3}
          transparent
          opacity={0.9}
        />
      </mesh>

      {/* Glow effect */}
      <mesh position={[0, 0, 0]} scale={[size * 1.3, size * 1.3, size * 1.3]}>
        <sphereGeometry args={[1, 16, 16]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.15}
          side={THREE.BackSide}
        />
      </mesh>

      {/* HTML label */}
      {(hovered || isNearby) && (
        <Html
          position={[0, size + 1, 0]}
          center
          distanceFactor={10}
          style={{
            pointerEvents: 'none',
            userSelect: 'none'
          }}
        >
          <div className="bg-black/80 text-white px-3 py-2 rounded-lg text-sm whitespace-nowrap">
            <div className="font-bold">{item.item_name}</div>
            <div className="text-xs opacity-75">
              {item.item_type.replace('_', ' ').toUpperCase()}
            </div>
            <div className="text-xs text-yellow-400">
              {item.cost} credits
            </div>
            {playerDistance !== undefined && (
              <div className="text-xs text-blue-400">
                {Math.round(playerDistance)}m away
              </div>
            )}
          </div>
        </Html>
      )}
    </group>
  );
};

export default WorldItemMarker;
