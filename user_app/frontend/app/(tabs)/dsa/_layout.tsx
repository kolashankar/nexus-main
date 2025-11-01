import { Stack } from 'expo-router';

export default function DSALayout() {
  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="index" />
      <Stack.Screen name="questions" />
      <Stack.Screen name="topics" />
      <Stack.Screen name="sheets" />
      <Stack.Screen name="companies" />
    </Stack>
  );
}