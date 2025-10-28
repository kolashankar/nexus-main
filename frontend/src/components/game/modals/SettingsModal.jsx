import React, { useState } from 'react';
import { Card } from '../ui/card';
import { X, Settings as SettingsIcon, Volume2, Monitor, Gamepad, Video } from 'lucide-react';

/**
 * Settings Modal Component
 */
const SettingsModal = ({ onClose }) => {
  const [settings, setSettings] = useState({
    masterVolume: 70,
    musicVolume: 50,
    sfxVolume: 80,
    graphics: 'high',
    fov: 75,
    mouseSensitivity: 50,
    invertY: false,
    showFPS: false,
    vsync: true,
  });

  const handleChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = () => {
    console.log('Settings saved:', settings);
    localStorage.setItem('game-settings', JSON.stringify(settings));
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="bg-gray-900 border-purple-500/30 p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold text-white flex items-center gap-2">
            <SettingsIcon className="w-8 h-8 text-purple-400" />
            Settings
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Audio Settings */}
        <div className="mb-6">
          <h3 className="text-white font-semibold text-lg mb-4 flex items-center gap-2">
            <Volume2 className="w-5 h-5" />
            Audio
          </h3>
          <div className="space-y-4">
            <div>
              <label className="text-gray-300 text-sm mb-2 block">
                Master Volume: {settings.masterVolume}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={settings.masterVolume}
                onChange={(e) => handleChange('masterVolume', parseInt(e.target.value))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
            </div>
            <div>
              <label className="text-gray-300 text-sm mb-2 block">
                Music Volume: {settings.musicVolume}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={settings.musicVolume}
                onChange={(e) => handleChange('musicVolume', parseInt(e.target.value))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
            </div>
            <div>
              <label className="text-gray-300 text-sm mb-2 block">
                SFX Volume: {settings.sfxVolume}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={settings.sfxVolume}
                onChange={(e) => handleChange('sfxVolume', parseInt(e.target.value))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
            </div>
          </div>
        </div>

        {/* Graphics Settings */}
        <div className="mb-6">
          <h3 className="text-white font-semibold text-lg mb-4 flex items-center gap-2">
            <Video className="w-5 h-5" />
            Graphics
          </h3>
          <div className="space-y-4">
            <div>
              <label className="text-gray-300 text-sm mb-2 block">
                Graphics Quality
              </label>
              <select
                value={settings.graphics}
                onChange={(e) => handleChange('graphics', e.target.value)}
                className="w-full bg-gray-800 text-white px-3 py-2 rounded border border-gray-700 focus:border-purple-500 focus:outline-none"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="ultra">Ultra</option>
              </select>
            </div>
            <div>
              <label className="text-gray-300 text-sm mb-2 block">
                Field of View (FOV): {settings.fov}°
              </label>
              <input
                type="range"
                min="60"
                max="120"
                value={settings.fov}
                onChange={(e) => handleChange('fov', parseInt(e.target.value))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-300 text-sm">VSync</span>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.vsync}
                  onChange={(e) => handleChange('vsync', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-purple-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
              </label>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-300 text-sm">Show FPS</span>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.showFPS}
                  onChange={(e) => handleChange('showFPS', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-purple-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
              </label>
            </div>
          </div>
        </div>

        {/* Controls Settings */}
        <div className="mb-6">
          <h3 className="text-white font-semibold text-lg mb-4 flex items-center gap-2">
            <Gamepad className="w-5 h-5" />
            Controls
          </h3>
          <div className="space-y-4">
            <div>
              <label className="text-gray-300 text-sm mb-2 block">
                Mouse Sensitivity: {settings.mouseSensitivity}%
              </label>
              <input
                type="range"
                min="10"
                max="100"
                value={settings.mouseSensitivity}
                onChange={(e) => handleChange('mouseSensitivity', parseInt(e.target.value))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-300 text-sm">Invert Y-Axis</span>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.invertY}
                  onChange={(e) => handleChange('invertY', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-purple-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
              </label>
            </div>
          </div>
        </div>

        {/* Keybindings Info */}
        <div className="mb-6 p-4 bg-black/30 rounded-lg border border-purple-500/30">
          <h4 className="text-white font-semibold mb-2">Default Keybindings</h4>
          <div className="grid grid-cols-2 gap-2 text-sm text-gray-300">
            <div><span className="text-purple-400">WASD:</span> Movement</div>
            <div><span className="text-purple-400">Space:</span> Jump</div>
            <div><span className="text-purple-400">Mouse:</span> Look</div>
            <div><span className="text-purple-400">ESC:</span> Menu</div>
            <div><span className="text-purple-400">E:</span> Interact</div>
            <div><span className="text-purple-400">Tab:</span> Inventory</div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <button
            onClick={handleSave}
            className="flex-1 bg-purple-600 hover:bg-purple-700 text-white py-3 rounded-lg font-semibold transition-colors"
          >
            Save Settings
          </button>
          <button
            onClick={onClose}
            className="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-3 rounded-lg font-semibold transition-colors"
          >
            Cancel
          </button>
        </div>
      </Card>
    </div>
  );
};

export default SettingsModal;
