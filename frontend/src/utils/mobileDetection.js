/**
 * Mobile Detection Utilities
 * Detect if the device is a mobile/touch device
 */

export const isMobileDevice = () => {
  // Check for touch support
  const hasTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  
  // Check user agent for mobile devices
  const mobileRegex = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i;
  const isMobileUA = mobileRegex.test(navigator.userAgent);
  
  // Check screen width (mobile typically < 768px)
  const isSmallScreen = window.innerWidth < 768;
  
  return hasTouch && (isMobileUA || isSmallScreen);
};

export const isTabletDevice = () => {
  const hasTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  const isTabletUA = /iPad|Android/i.test(navigator.userAgent);
  const isMediumScreen = window.innerWidth >= 768 && window.innerWidth <= 1024;
  
  return hasTouch && isTabletUA && isMediumScreen;
};

export const isTouchDevice = () => {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
};

export const getDeviceType = () => {
  if (isMobileDevice()) return 'mobile';
  if (isTabletDevice()) return 'tablet';
  return 'desktop';
};

export const getScreenOrientation = () => {
  return window.innerWidth > window.innerHeight ? 'landscape' : 'portrait';
};

export const useDeviceDetection = () => {
  const [deviceType, setDeviceType] = React.useState(getDeviceType());
  const [orientation, setOrientation] = React.useState(getScreenOrientation());

  React.useEffect(() => {
    const handleResize = () => {
      setDeviceType(getDeviceType());
      setOrientation(getScreenOrientation());
    };

    window.addEventListener('resize', handleResize);
    window.addEventListener('orientationchange', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('orientationchange', handleResize);
    };
  }, []);

  return { deviceType, orientation, isMobile: deviceType === 'mobile', isTablet: deviceType === 'tablet' };
};

// React import for hook
import React from 'react';
