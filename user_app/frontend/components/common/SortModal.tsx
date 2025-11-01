import React from 'react';
import { View, Text, TouchableOpacity, Modal } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export type SortOption = {
  label: string;
  value: string;
};

interface SortModalProps {
  visible: boolean;
  onClose: () => void;
  onSelect: (option: string) => void;
  currentSort: string;
  options: SortOption[];
  title?: string;
}

export default function SortModal({
  visible,
  onClose,
  onSelect,
  currentSort,
  options,
  title = 'Sort By',
}: SortModalProps) {
  const handleSelect = (value: string) => {
    onSelect(value);
    onClose();
  };

  return (
    <Modal visible={visible} animationType="slide" transparent>
      <View className="flex-1 bg-black/50 justify-end">
        <View className="bg-dark-400 rounded-t-3xl">
          {/* Header */}
          <View className="flex-row justify-between items-center px-6 py-4 border-b border-gray-700">
            <Text className="text-white text-xl font-bold">{title}</Text>
            <TouchableOpacity onPress={onClose}>
              <Ionicons name="close" size={24} color="#fff" />
            </TouchableOpacity>
          </View>

          {/* Options */}
          <View className="px-6 py-4">
            {options.map((option) => (
              <TouchableOpacity
                key={option.value}
                className="flex-row justify-between items-center py-4 border-b border-gray-700"
                onPress={() => handleSelect(option.value)}
              >
                <Text
                  className={`text-lg ${\n                    currentSort === option.value ? 'text-primary-600' : 'text-white'\n                  }`}
                >
                  {option.label}
                </Text>
                {currentSort === option.value && (
                  <Ionicons name="checkmark" size={24} color="#3b82f6" />
                )}
              </TouchableOpacity>
            ))}
          </View>

          {/* Safe area padding */}
          <View className="h-8" />
        </View>
      </View>
    </Modal>
  );
}
