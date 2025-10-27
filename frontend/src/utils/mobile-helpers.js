import React from "react";
/**
 * Mobile-specific helper utilities for Karma Nexus
 */

/**
 * Detect if device is mobile
 */
export const isMobile = () => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
};

/**
 * Detect if device is iOS
 */
export const isIOS = () => {
  return /iPad|iPhone|iPod/.test(navigator.userAgent);
};

/**
 * Detect if device is Android
 */
export const isAndroid = () => {
  return /Android/.test(navigator.userAgent);
};

/**
 * Check if device supports touch
 */
export const hasTouch = () => {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;
};

/**
 * Get viewport dimensions
 */
export const getViewport = () => {
  return {
    width: window.innerWidth,
    height: window.innerHeight,
  };
};

/**
 * Check if device is in landscape mode
 */
export const isLandscape = () => {
  return window.innerWidth > window.innerHeight;
};

/**
 * Lock screen orientation (if supported)
 */
export const lockOrientation = async (orientation) => {
  // eslint-disable-next-line no-restricted-globals
  if ('orientation' in screen && 'lock' in screen.orientation) {
    try {
      // eslint-disable-next-line no-restricted-globals
      await screen.orientation.lock(orientation);
      return true;
    } catch (error) {
      console.warn('Screen orientation lock not supported:', error);
      return false;
    }
  }
  return false;
};

/**
 * Unlock screen orientation
 */
export const unlockOrientation = () => {
  // eslint-disable-next-line no-restricted-globals
  if ('orientation' in screen && 'unlock' in screen.orientation) {
    // eslint-disable-next-line no-restricted-globals
    screen.orientation.unlock();
  }
};

/**
 * Vibrate device (if supported)
 */
export const vibrate = (pattern) => {
  if ('vibrate' in navigator) {
    return navigator.vibrate(pattern);
  }
  return false;
};

/**
 * Haptic feedback patterns
 */
export const haptic = {
  light: () => vibrate(10),
  medium: () => vibrate(20),
  heavy: () => vibrate(30),
  success: () => vibrate([10, 50, 10]),
  error: () => vibrate([30, 50, 30, 50, 30]),
  warning: () => vibrate([20, 100, 20]),
};

/**
 * Prevent body scroll (useful for modals)
 */
export const preventBodyScroll = (prevent) => {
  if (prevent) {
    document.body.style.overflow = 'hidden';
    document.body.style.position = 'fixed';
    document.body.style.width = '100%';
  } else {
    document.body.style.overflow = '';
    document.body.style.position = '';
    document.body.style.width = '';
  }
};

/**
 * Safe area insets for notched devices
 */
export const getSafeAreaInsets = () => {
  const getInset = (side) => {
    const value = getComputedStyle(document.documentElement).getPropertyValue(
      `--safe-area-inset-${side}`
    );
    return value ? parseInt(value, 10) : 0;
  };

  return {
    top: getInset('top'),
    right: getInset('right'),
    bottom: getInset('bottom'),
    left: getInset('left'),
  };
};

/**
 * Touch gesture detector
 */
export class TouchGestureDetector {
  constructor(element) {
    this.startX = 0;
    this.startY = 0;
    this.startTime = 0;
    this.element = element;
    this.setupListeners();
  }

  setupListeners() {
    this.element.addEventListener('touchstart', this.handleTouchStart, {
      passive: true,
    });
    this.element.addEventListener('touchend', this.handleTouchEnd, {
      passive: true,
    });
  }

  handleTouchStart = (event) => {
    this.startX = event.touches[0].clientX;
    this.startY = event.touches[0].clientY;
    this.startTime = Date.now();
  };

  handleTouchEnd = (event) => {
    const endX = event.changedTouches[0].clientX;
    const endY = event.changedTouches[0].clientY;
    const endTime = Date.now();

    const deltaX = endX - this.startX;
    const deltaY = endY - this.startY;
    const duration = endTime - this.startTime;

    const distance = Math.sqrt(deltaX ** 2 + deltaY ** 2);

    // Tap
    if (distance < 10 && duration < 200) {
      this.onTap?.();
    }

    // Swipe
    if (distance > 50 && duration < 300) {
      if (Math.abs(deltaX) > Math.abs(deltaY)) {
        // Horizontal swipe
        if (deltaX > 0) {
          this.onSwipeRight?.();
        } else {
          this.onSwipeLeft?.();
        }
      } else {
        // Vertical swipe
        if (deltaY > 0) {
          this.onSwipeDown?.();
        } else {
          this.onSwipeUp?.();
        }
      }
    }

    // Long press
    if (distance < 10 && duration > 500) {
      this.onLongPress?.();
    }
  };

  destroy() {
    this.element.removeEventListener('touchstart', this.handleTouchStart);
    this.element.removeEventListener('touchend', this.handleTouchEnd);
  }
}

/**
 * Pull to refresh handler
 */
export class PullToRefresh {
  constructor(element, threshold = 80) {
    this.startY = 0;
    this.pulling = false;
    this.element = element;
    this.threshold = threshold;
    this.setupListeners();
  }

  setupListeners() {
    this.element.addEventListener('touchstart', this.handleTouchStart, {
      passive: true,
    });
    this.element.addEventListener('touchmove', this.handleTouchMove);
    this.element.addEventListener('touchend', this.handleTouchEnd);
  }

  handleTouchStart = (event) => {
    if (this.element.scrollTop === 0) {
      this.startY = event.touches[0].clientY;
      this.pulling = true;
    }
  };

  handleTouchMove = (event) => {
    if (!this.pulling) return;

    const currentY = event.touches[0].clientY;
    const distance = currentY - this.startY;

    if (distance > 0 && this.element.scrollTop === 0) {
      event.preventDefault();
      this.onPull?.(Math.min(distance, this.threshold));

      if (distance >= this.threshold) {
        this.onThresholdReached?.();
      }
    }
  };

  handleTouchEnd = () => {
    if (!this.pulling) return;

    this.pulling = false;
    this.onRelease?.();
  };

  destroy() {
    this.element.removeEventListener('touchstart', this.handleTouchStart);
    this.element.removeEventListener('touchmove', this.handleTouchMove);
    this.element.removeEventListener('touchend', this.handleTouchEnd);
  }
}

/**
 * Network information (if available)
 */
export const getNetworkInfo = () => {
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;

  if (connection) {
    return {
      type: connection.effectiveType, // '4g', '3g', '2g', 'slow-2g'
      downlink: connection.downlink, // Mbps
      rtt: connection.rtt, // Round-trip time in ms
      saveData: connection.saveData, // User preference
    };
  }

  return null;
};

/**
 * Check if connection is slow
 */
export const isSlowConnection = () => {
  const info = getNetworkInfo();
  if (!info) return false;

  return info.type === 'slow-2g' || info.type === '2g' || info.saveData;
};

/**
 * Add to home screen prompt
 */
export const promptInstallPWA = () => {
  return new Promise((resolve) => {
    const deferredPrompt = window.deferredPrompt;

    if (deferredPrompt) {
      deferredPrompt.prompt();

      deferredPrompt.userChoice.then((choiceResult) => {
        resolve(choiceResult.outcome === 'accepted');
        window.deferredPrompt = null;
      });
    } else {
      resolve(false);
    }
  });
};
