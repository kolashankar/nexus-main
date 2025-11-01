import React, { useEffect, useState } from 'react';
import { View, Text } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import NetInfo from '@react-native-community/netinfo';

export default function OfflineIndicator() {
  const [isOffline, setIsOffline] = useState(false);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsOffline(!state.isConnected);
    });

    return () => unsubscribe();
  }, []);

  if (!isOffline) return null;

  return (
    <View className="bg-orange-500 px-4 py-2 flex-row items-center justify-center">
      <Ionicons name="cloud-offline" size={16} color="white" />
      <Text className="text-white text-sm font-semibold ml-2">
        You're offline - Viewing cached content
      </Text>
    </View>
  );
}
