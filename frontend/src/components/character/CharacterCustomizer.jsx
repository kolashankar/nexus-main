import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { User, Palette } from 'lucide-react';
import useStore from '../../store';

/**
 * Character Customizer Component
 * Allows players to select and customize their character
 */
const CharacterCustomizer = () => {
  const { player, updatePlayer } = useStore();
  
  const [selectedCharacter, setSelectedCharacter] = useState(player?.character_model || 'male_base');
  const [selectedSkin, setSelectedSkin] = useState(player?.skin_tone || 'default');
  const [selectedHair, setSelectedHair] = useState(player?.hair_color || 'brown');
  const [isSaving, setIsSaving] = useState(false);

  // Character options
  const characters = [
    { id: 'male_base', label: 'Male Base', gender: 'male' },
    { id: 'male_athletic', label: 'Male Athletic', gender: 'male' },
    { id: 'male_heavy', label: 'Male Heavy', gender: 'male' },
    { id: 'female_base', label: 'Female Base', gender: 'female' },
    { id: 'female_athletic', label: 'Female Athletic', gender: 'female' },
    { id: 'female_heavy', label: 'Female Heavy', gender: 'female' },
  ];

  // Skin tone options
  const skinTones = [
    { id: 'light', label: 'Light', color: '#FFE0BD' },
    { id: 'medium', label: 'Medium', color: '#C68642' },
    { id: 'dark', label: 'Dark', color: '#8D5524' },
    { id: 'default', label: 'Default', color: '#E0AC69' },
  ];

  // Hair color options
  const hairColors = [
    { id: 'black', label: 'Black', color: '#141414' },
    { id: 'brown', label: 'Brown', color: '#462B19' },
    { id: 'blonde', label: 'Blonde', color: '#E6C878' },
    { id: 'red', label: 'Red', color: '#A52A2A' },
  ];

  const handleSave = async () => {
    setIsSaving(true);
    try {
      // Update both flat fields and appearance object for compatibility
      await updatePlayer({
        character_model: selectedCharacter,
        skin_tone: selectedSkin,
        hair_color: selectedHair,
        appearance: {
          model: selectedCharacter,
          skin_tone: selectedSkin,
          hair_color: selectedHair,
        }
      });
      console.log('✅ Character customization saved!');
      alert('✅ Character saved successfully!');
    } catch (error) {
      console.error('❌ Failed to save customization:', error);
      alert('❌ Failed to save character. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Card className="bg-gradient-to-br from-purple-900/20 to-blue-900/20 border-purple-500/30">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-white">
          <User className="w-5 h-5" />
          Character Customization
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Character Selection */}
        <div>
          <label className="text-white font-semibold mb-3 block">
            Select Character Type
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {characters.map((char) => (
              <button
                key={char.id}
                onClick={() => setSelectedCharacter(char.id)}
                className={`p-4 rounded-lg border-2 transition-all ${
                  selectedCharacter === char.id
                    ? 'border-purple-500 bg-purple-500/30'
                    : 'border-gray-600 bg-gray-800/50 hover:border-purple-400'
                }`}
              >
                <div className="flex flex-col items-center gap-2">
                  <User className={`w-8 h-8 ${
                    selectedCharacter === char.id ? 'text-purple-300' : 'text-gray-400'
                  }`} />
                  <span className="text-sm text-white">{char.label}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Skin Tone Selection */}
        <div>
          <label className="text-white font-semibold mb-3 block flex items-center gap-2">
            <Palette className="w-4 h-4" />
            Skin Tone
          </label>
          <div className="grid grid-cols-4 gap-3">
            {skinTones.map((skin) => (
              <button
                key={skin.id}
                onClick={() => setSelectedSkin(skin.id)}
                className={`p-3 rounded-lg border-2 transition-all ${
                  selectedSkin === skin.id
                    ? 'border-purple-500 bg-purple-500/20'
                    : 'border-gray-600 hover:border-purple-400'
                }`}
              >
                <div className="flex flex-col items-center gap-2">
                  <div
                    className="w-8 h-8 rounded-full border-2 border-white"
                    style={{ backgroundColor: skin.color }}
                  />
                  <span className="text-xs text-white">{skin.label}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Hair Color Selection */}
        <div>
          <label className="text-white font-semibold mb-3 block flex items-center gap-2">
            <Palette className="w-4 h-4" />
            Hair Color
          </label>
          <div className="grid grid-cols-4 gap-3">
            {hairColors.map((hair) => (
              <button
                key={hair.id}
                onClick={() => setSelectedHair(hair.id)}
                className={`p-3 rounded-lg border-2 transition-all ${
                  selectedHair === hair.id
                    ? 'border-purple-500 bg-purple-500/20'
                    : 'border-gray-600 hover:border-purple-400'
                }`}
              >
                <div className="flex flex-col items-center gap-2">
                  <div
                    className="w-8 h-8 rounded-full border-2 border-white"
                    style={{ backgroundColor: hair.color }}
                  />
                  <span className="text-xs text-white">{hair.label}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Save Button */}
        <button
          onClick={handleSave}
          disabled={isSaving}
          className={`w-full py-3 rounded-lg font-semibold transition-all ${
            isSaving
              ? 'bg-gray-600 cursor-not-allowed'
              : 'bg-purple-600 hover:bg-purple-700'
          } text-white`}
        >
          {isSaving ? 'Saving...' : 'Save Character'}
        </button>

        {/* Current Selection Display */}
        <div className="mt-4 p-4 bg-black/30 rounded-lg border border-purple-500/30">
          <h4 className="text-white font-semibold mb-2">Current Selection:</h4>
          <div className="text-sm text-gray-300 space-y-1">
            <p>• Character: <span className="text-purple-300">{characters.find(c => c.id === selectedCharacter)?.label}</span></p>
            <p>• Skin Tone: <span className="text-purple-300">{skinTones.find(s => s.id === selectedSkin)?.label}</span></p>
            <p>• Hair Color: <span className="text-purple-300">{hairColors.find(h => h.id === selectedHair)?.label}</span></p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CharacterCustomizer;
