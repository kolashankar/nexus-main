import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Dimensions, Image } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  interpolate,
} from 'react-native-reanimated';
import { setOnboardingComplete } from '../lib/onboarding';

const { width } = Dimensions.get('window');

interface OnboardingSlide {
  id: number;
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  description: string;
  color: string;
}

const slides: OnboardingSlide[] = [
  {
    id: 1,
    icon: 'briefcase',
    title: 'Discover Opportunities',
    description: 'Find your dream job, internship, or scholarship from thousands of listings tailored to your profile.',
    color: '#3b82f6',
  },
  {
    id: 2,
    icon: 'code-slash',
    title: 'Master DSA',
    description: 'Practice coding problems, track your progress, and prepare for technical interviews with curated question sheets.',
    color: '#8b5cf6',
  },
  {
    id: 3,
    icon: 'book',
    title: 'Learn & Grow',
    description: 'Access quality articles and learning roadmaps to enhance your skills and advance your career.',
    color: '#ec4899',
  },
  {
    id: 4,
    icon: 'rocket',
    title: 'AI-Powered Tools',
    description: 'Get personalized resume reviews, cover letters, and career guidance powered by advanced AI.',
    color: '#10b981',
  },
];

export default function OnboardingScreen() {
  const router = useRouter();
  const [currentSlide, setCurrentSlide] = useState(0);
  const translateX = useSharedValue(0);

  const animatedStyle = useAnimatedStyle(() => {
    return {
      transform: [{ translateX: translateX.value }],
    };
  });

  const goToNextSlide = () => {
    if (currentSlide < slides.length - 1) {
      const nextSlide = currentSlide + 1;
      setCurrentSlide(nextSlide);
      translateX.value = withTiming(-width * nextSlide, { duration: 300 });
    } else {
      completeOnboarding();
    }
  };

  const goToPreviousSlide = () => {
    if (currentSlide > 0) {
      const prevSlide = currentSlide - 1;
      setCurrentSlide(prevSlide);
      translateX.value = withTiming(-width * prevSlide, { duration: 300 });
    }
  };

  const skipOnboarding = async () => {
    await setOnboardingComplete();
    router.replace('/(tabs)/jobs');
  };

  const completeOnboarding = async () => {
    await setOnboardingComplete();
    router.replace('/(tabs)/jobs');
  };

  return (
    <SafeAreaView className="flex-1 bg-gray-900">
      {/* Skip Button */}
      {currentSlide < slides.length - 1 && (
        <TouchableOpacity
          onPress={skipOnboarding}
          className="absolute top-12 right-6 z-10 px-4 py-2 bg-gray-800 rounded-full"
        >
          <Text className="text-blue-400 font-semibold">Skip</Text>
        </TouchableOpacity>
      )}

      {/* Slides Container */}
      <View className="flex-1 justify-center items-center">
        <Animated.View
          style={[
            {
              width: width * slides.length,
              flexDirection: 'row',
            },
            animatedStyle,
          ]}
        >
          {slides.map((slide, index) => (
            <View
              key={slide.id}
              style={{ width }}
              className="justify-center items-center px-8"
            >
              {/* Icon */}
              <View
                className="w-32 h-32 rounded-full justify-center items-center mb-8"
                style={{ backgroundColor: `${slide.color}20` }}
              >
                <Ionicons name={slide.icon} size={80} color={slide.color} />
              </View>

              {/* Title */}
              <Text className="text-white text-3xl font-bold text-center mb-4">
                {slide.title}
              </Text>

              {/* Description */}
              <Text className="text-gray-400 text-lg text-center leading-relaxed">
                {slide.description}
              </Text>
            </View>
          ))}
        </Animated.View>
      </View>

      {/* Pagination Dots */}
      <View className="flex-row justify-center items-center mb-8">
        {slides.map((_, index) => (
          <View
            key={index}
            className={`h-2 rounded-full mx-1 ${
              index === currentSlide ? 'w-8 bg-blue-500' : 'w-2 bg-gray-600'
            }`}
          />
        ))}
      </View>

      {/* Navigation Buttons */}
      <View className="flex-row justify-between items-center px-8 pb-8">
        <TouchableOpacity
          onPress={goToPreviousSlide}
          disabled={currentSlide === 0}
          className={`w-14 h-14 rounded-full justify-center items-center ${
            currentSlide === 0 ? 'bg-gray-800' : 'bg-gray-700'
          }`}
        >
          <Ionicons
            name="chevron-back"
            size={24}
            color={currentSlide === 0 ? '#4b5563' : '#ffffff'}
          />
        </TouchableOpacity>

        <TouchableOpacity
          onPress={goToNextSlide}
          className="flex-1 mx-4 bg-blue-600 rounded-full py-4 justify-center items-center"
        >
          <Text className="text-white text-lg font-semibold">
            {currentSlide === slides.length - 1 ? 'Get Started' : 'Next'}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          onPress={goToNextSlide}
          className="w-14 h-14 bg-blue-600 rounded-full justify-center items-center"
        >
          <Ionicons name="chevron-forward" size={24} color="white" />
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}
