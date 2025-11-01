import React from 'react';
import { TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface ShareButtonProps {
  onPress: () => void;
  size?: number;
  color?: string;
}

export default function ShareButton({ onPress, size = 24, color = '#3b82f6' }: ShareButtonProps) {
  return (
    <TouchableOpacity
      onPress={onPress}
      className="p-2 rounded-full bg-gray-800"
      activeOpacity={0.7}
    >
      <Ionicons name="share-social" size={size} color={color} />
    </TouchableOpacity>
  );
}
