import React, { useEffect, useState } from 'react';
import { X } from 'lucide-react';
import { Button } from './button';

const shortcuts = [
  { key: '?', description: 'Open shortcuts', category: 'General' },
  { key: 'esc', description: 'Close modal/dialog', category: 'General' },
  { key: 'c', description: 'Open chat', category: 'Social' },
  { key: 'i', description: 'Open inventory', category: 'Player' },
  { key: 'm', description: 'Open map', category: 'World' },
  { key: 'q', description: 'Open quest log', category: 'Quests' },
  { key: '1-5', description: 'Use combat ability', category: 'Combat' },
  { key: 'space', description: 'Confirm action', category: 'General' },
  { key: 'tab', description: 'Cycle targets', category: 'Combat' },
  { key: 'g', description: 'Open guild panel', category: 'Social' },
  { key: 'p', description: 'Open profile', category: 'Player' },
];

export const KeyboardShortcutsModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  const groupedShortcuts = shortcuts.reduce((acc, shortcut) => {
    if (!acc[shortcut.category]) {
      acc[shortcut.category] = [];
    }
    acc[shortcut.category].push(shortcut);
    return acc;
  }, {});

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70"
      onClick={onClose}
    >
      <div
        className="relative max-w-2xl w-full mx-4 bg-gray-900/95 border border-cyan-500/30 rounded-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-6 pb-4 border-b border-white/10">
          <h2 className="text-2xl font-bold text-white">Keyboard Shortcuts</h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            className="text-white hover:bg-white/10"
          >
            <X className="h-6 w-6" />
          </Button>
        </div>

        <div className="space-y-6">
          {Object.entries(groupedShortcuts).map(([category, items]) => (
            <div key={category} className="space-y-2">
              <h3 className="text-lg font-semibold text-cyan-400 mb-3">{category}</h3>
              <div className="space-y-2">
                {items.map((shortcut, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between py-2 px-3 rounded bg-white/5"
                  >
                    <kbd className="px-2 py-1 text-xs font-mono bg-gray-800 border border-gray-600 rounded">
                      {shortcut.key}
                    </kbd>
                    <span className="flex-1 ml-4 text-white/80 text-sm">
                      {shortcut.description}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export const useKeyboardShortcuts = () => {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleKeyPress = (event) => {
      // Ignore if user is typing in an input
      if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) {
        return;
      }

      switch (event.key) {
        case '?':
          event.preventDefault();
          setIsOpen(true);
          break;
        case 'Escape':
          if (isOpen) {
            event.preventDefault();
            setIsOpen(false);
          }
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [isOpen]);

  return {
    isOpen,
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
  };
};