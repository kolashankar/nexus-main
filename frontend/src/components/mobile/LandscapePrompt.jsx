import React, { useEffect, useState } from 'react';
import { RotateCcw } from 'lucide-react';

/**
 * Landscape Orientation Prompt
 * Shows a message when device is in portrait mode, prompting user to rotate
 */
const LandscapePrompt = () => {
  const [isPortrait, setIsPortrait] = useState(false);

  useEffect(() => {
    const checkOrientation = () => {
      // Check if device is in portrait mode
      const portrait = window.innerHeight > window.innerWidth;
      setIsPortrait(portrait);
    };

    // Check on mount
    checkOrientation();

    // Listen for orientation changes
    window.addEventListener('resize', checkOrientation);
    window.addEventListener('orientationchange', checkOrientation);

    return () => {
      window.removeEventListener('resize', checkOrientation);
      window.removeEventListener('orientationchange', checkOrientation);
    };
  }, []);

  if (!isPortrait) return null;

  return (
    <div className="fixed inset-0 z-[9999] bg-black/95 backdrop-blur-sm flex items-center justify-center p-8">
      <div className="text-center max-w-md">
        <div className="mb-6 flex justify-center">
          <div className="animate-bounce">
            <RotateCcw className="w-20 h-20 text-purple-500" />
          </div>
        </div>
        <h2 className="text-3xl font-bold text-white mb-4">
          Rotate Your Device
        </h2>
        <p className="text-gray-300 text-lg mb-4">
          For the best gaming experience, please rotate your device to landscape mode.
        </p>
        <div className="inline-flex items-center gap-2 bg-purple-600/20 border-2 border-purple-500 rounded-lg px-6 py-3 text-purple-300">
          <div className="w-12 h-8 border-2 border-purple-400 rounded flex items-center justify-center rotate-90">
            <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
          </div>
          <span className="font-semibold">Turn sideways</span>
        </div>
      </div>
    </div>
  );
};

export default LandscapePrompt;
