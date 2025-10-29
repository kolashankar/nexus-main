import React, { useEffect, useRef, useState } from 'react';
import './VirtualJoystick.css';

/**
 * Virtual Joystick Component for Mobile Touch Controls
 * Returns normalized x, y values (-1 to 1) for movement direction
 */
const VirtualJoystick = ({ onMove, size = 120, maxDistance = 50 }) => {
  const joystickRef = useRef(null);
  const stickRef = useRef(null);
  const [isActive, setIsActive] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const touchId = useRef(null);
  const basePosition = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const joystick = joystickRef.current;
    if (!joystick) return;

    const handleTouchStart = (e) => {
      e.preventDefault();
      const touch = e.touches[0];
      touchId.current = touch.identifier;
      
      // Get joystick center position
      const rect = joystick.getBoundingClientRect();
      basePosition.current = {
        x: rect.left + rect.width / 2,
        y: rect.top + rect.height / 2
      };

      setIsActive(true);
      handleTouchMove(e);
    };

    const handleTouchMove = (e) => {
      e.preventDefault();
      if (touchId.current === null) return;

      // Find the touch that started on this joystick
      const touch = Array.from(e.touches).find(t => t.identifier === touchId.current);
      if (!touch) return;

      // Calculate offset from center
      const deltaX = touch.clientX - basePosition.current.x;
      const deltaY = touch.clientY - basePosition.current.y;

      // Calculate distance and angle
      const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
      const angle = Math.atan2(deltaY, deltaX);

      // Limit stick movement to maxDistance
      const limitedDistance = Math.min(distance, maxDistance);

      // Calculate stick position
      const stickX = limitedDistance * Math.cos(angle);
      const stickY = limitedDistance * Math.sin(angle);

      setPosition({ x: stickX, y: stickY });

      // Normalize values (-1 to 1) for game controls
      const normalizedX = stickX / maxDistance;
      const normalizedY = stickY / maxDistance;

      if (onMove) {
        onMove({ x: normalizedX, y: normalizedY, distance: limitedDistance / maxDistance });
      }
    };

    const handleTouchEnd = (e) => {
      e.preventDefault();
      
      // Check if the released touch is ours
      const stillTouching = Array.from(e.touches).some(t => t.identifier === touchId.current);
      if (stillTouching) return;

      touchId.current = null;
      setIsActive(false);
      setPosition({ x: 0, y: 0 });

      if (onMove) {
        onMove({ x: 0, y: 0, distance: 0 });
      }
    };

    joystick.addEventListener('touchstart', handleTouchStart, { passive: false });
    joystick.addEventListener('touchmove', handleTouchMove, { passive: false });
    joystick.addEventListener('touchend', handleTouchEnd, { passive: false });
    joystick.addEventListener('touchcancel', handleTouchEnd, { passive: false });

    return () => {
      joystick.removeEventListener('touchstart', handleTouchStart);
      joystick.removeEventListener('touchmove', handleTouchMove);
      joystick.removeEventListener('touchend', handleTouchEnd);
      joystick.removeEventListener('touchcancel', handleTouchEnd);
    };
  }, [onMove, maxDistance]);

  return (
    <div className="virtual-joystick-container">
      <div
        ref={joystickRef}
        className={`joystick-base ${isActive ? 'active' : ''}`}
        style={{
          width: `${size}px`,
          height: `${size}px`
        }}
      >
        <div
          ref={stickRef}
          className="joystick-stick"
          style={{
            transform: `translate(${position.x}px, ${position.y}px)`,
            opacity: isActive ? 1 : 0.6
          }}
        />
      </div>
    </div>
  );
};

export default VirtualJoystick;
