import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Volume2, VolumeX, Monitor, Smartphone, Globe, Shield } from 'lucide-react';

const SettingsTab = ({ player }) => {
  const [settings, setSettings] = useState({
    soundEnabled: true,
    musicEnabled: true,
    graphicsQuality: 'high',
    showNotifications: true,
    language: 'en'
  });

  const toggleSetting = (key) => {
    setSettings(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="tab-content-wrapper">
      <h3 className="tab-content-title">Settings</h3>
      
      {/* Audio Settings */}
      <Card className="p-6 bg-black/30 border-purple-500/30 mb-6">
        <h4 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
          <Volume2 className="w-5 h-5 text-purple-400" />
          Audio
        </h4>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-300">Sound Effects</span>
            <Button
              onClick={() => toggleSetting('soundEnabled')}
              variant={settings.soundEnabled ? 'default' : 'outline'}
              className={settings.soundEnabled ? 'bg-purple-600' : ''}
            >
              {settings.soundEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            </Button>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-300">Background Music</span>
            <Button
              onClick={() => toggleSetting('musicEnabled')}
              variant={settings.musicEnabled ? 'default' : 'outline'}
              className={settings.musicEnabled ? 'bg-purple-600' : ''}
            >
              {settings.musicEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            </Button>
          </div>
        </div>
      </Card>

      {/* Graphics Settings */}
      <Card className="p-6 bg-black/30 border-purple-500/30 mb-6">
        <h4 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
          <Monitor className="w-5 h-5 text-blue-400" />
          Graphics
        </h4>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-300">Quality</span>
            <select
              value={settings.graphicsQuality}
              onChange={(e) => setSettings(prev => ({ ...prev, graphicsQuality: e.target.value }))}
              className="bg-black/50 text-white border border-purple-500/30 rounded px-3 py-2"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>
      </Card>

      {/* General Settings */}
      <Card className="p-6 bg-black/30 border-purple-500/30">
        <h4 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
          <Globe className="w-5 h-5 text-green-400" />
          General
        </h4>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-300">Notifications</span>
            <Button
              onClick={() => toggleSetting('showNotifications')}
              variant={settings.showNotifications ? 'default' : 'outline'}
              className={settings.showNotifications ? 'bg-purple-600' : ''}
            >
              {settings.showNotifications ? 'ON' : 'OFF'}
            </Button>
          </div>
        </div>
      </Card>

      <style jsx>{`
        .tab-content-wrapper { padding: 0; }
        .tab-content-title {
          font-size: 24px;
          font-weight: bold;
          color: white;
          margin-bottom: 24px;
        }
      `}</style>
    </div>
  );
};

export default SettingsTab;