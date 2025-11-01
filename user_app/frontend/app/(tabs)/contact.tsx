import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView, TextInput, Linking, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

export default function ContactScreen() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = () => {
    if (!formData.name || !formData.email || !formData.subject || !formData.message) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      Alert.alert('Success', 'Message sent successfully! We\'ll get back to you soon.');
      setFormData({ name: '', email: '', subject: '', message: '' });
      setIsSubmitting(false);
    }, 1500);
  };

  const contactInfo = [
    {
      icon: 'mail' as keyof typeof Ionicons.glyphMap,
      title: 'Email Us',
      content: 'support@careerguide.com',
      action: () => Linking.openURL('mailto:support@careerguide.com'),
      color: '#3b82f6',
    },
    {
      icon: 'call' as keyof typeof Ionicons.glyphMap,
      title: 'Call Us',
      content: '+91 1234567890',
      action: () => Linking.openURL('tel:+911234567890'),
      color: '#10b981',
    },
    {
      icon: 'location' as keyof typeof Ionicons.glyphMap,
      title: 'Visit Us',
      content: 'Bangalore, Karnataka',
      action: () => {},
      color: '#8b5cf6',
    },
  ];

  const socialLinks = [
    { icon: 'logo-linkedin' as keyof typeof Ionicons.glyphMap, name: 'LinkedIn', color: '#0077b5' },
    { icon: 'logo-twitter' as keyof typeof Ionicons.glyphMap, name: 'Twitter', color: '#1da1f2' },
    { icon: 'logo-whatsapp' as keyof typeof Ionicons.glyphMap, name: 'WhatsApp', color: '#25d366' },
  ];

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      <ScrollView className="flex-1">
        {/* Hero Header */}
        <LinearGradient
          colors={['#2563eb', '#4f46e5', '#6366f1']}
          className="px-6 py-10"
        >
          <Text className="text-white text-3xl font-extrabold mb-2">Get in Touch</Text>
          <Text className="text-blue-100 text-base">
            We're here to help you succeed in your career journey
          </Text>
        </LinearGradient>

        {/* Contact Info Cards */}
        <View className="px-4 py-6">
          <Text className="text-gray-900 text-xl font-bold mb-4">Contact Information</Text>
          {contactInfo.map((info, index) => (
            <TouchableOpacity
              key={index}
              onPress={info.action}
              className="bg-white rounded-xl p-5 mb-3 flex-row items-center shadow-sm border border-gray-100"
            >
              <View style={{ backgroundColor: info.color + '20' }} className="w-12 h-12 rounded-full items-center justify-center mr-4">
                <Ionicons name={info.icon} size={24} color={info.color} />
              </View>
              <View className="flex-1">
                <Text className="text-gray-900 text-base font-bold">{info.title}</Text>
                <Text className="text-gray-600 text-sm mt-1">{info.content}</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
            </TouchableOpacity>
          ))}
        </View>

        {/* Contact Form */}
        <View className="px-4 py-6">
          <Text className="text-gray-900 text-xl font-bold mb-2">Send Us a Message</Text>
          <Text className="text-gray-600 text-sm mb-6">
            Fill out the form below and we'll get back to you within 24 hours
          </Text>

          <View className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
            <View className="mb-4">
              <Text className="text-gray-900 text-sm font-semibold mb-2">Your Name *</Text>
              <TextInput
                className="bg-gray-50 border border-gray-300 rounded-lg px-4 py-3 text-gray-900"
                placeholder="John Doe"
                value={formData.name}
                onChangeText={(text) => setFormData({ ...formData, name: text })}
              />
            </View>

            <View className="mb-4">
              <Text className="text-gray-900 text-sm font-semibold mb-2">Email Address *</Text>
              <TextInput
                className="bg-gray-50 border border-gray-300 rounded-lg px-4 py-3 text-gray-900"
                placeholder="john@example.com"
                keyboardType="email-address"
                autoCapitalize="none"
                value={formData.email}
                onChangeText={(text) => setFormData({ ...formData, email: text })}
              />
            </View>

            <View className="mb-4">
              <Text className="text-gray-900 text-sm font-semibold mb-2">Subject *</Text>
              <TextInput
                className="bg-gray-50 border border-gray-300 rounded-lg px-4 py-3 text-gray-900"
                placeholder="How can we help you?"
                value={formData.subject}
                onChangeText={(text) => setFormData({ ...formData, subject: text })}
              />
            </View>

            <View className="mb-6">
              <Text className="text-gray-900 text-sm font-semibold mb-2">Message *</Text>
              <TextInput
                className="bg-gray-50 border border-gray-300 rounded-lg px-4 py-3 text-gray-900"
                placeholder="Tell us more about your inquiry..."
                multiline
                numberOfLines={6}
                textAlignVertical="top"
                value={formData.message}
                onChangeText={(text) => setFormData({ ...formData, message: text })}
              />
            </View>

            <TouchableOpacity
              onPress={handleSubmit}
              disabled={isSubmitting}
              className={`${isSubmitting ? 'bg-blue-400' : 'bg-blue-600'} rounded-lg py-4 flex-row items-center justify-center`}
            >
              <Ionicons name="send" size={20} color="#fff" />
              <Text className="text-white font-bold text-base ml-2">
                {isSubmitting ? 'Sending...' : 'Send Message'}
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Social Links */}
        <View className="px-4 py-6">
          <Text className="text-gray-900 text-xl font-bold mb-2 text-center">Connect With Us</Text>
          <Text className="text-gray-600 text-sm mb-6 text-center">
            Follow us on social media for updates and career tips
          </Text>
          <View className="flex-row justify-center gap-4">
            {socialLinks.map((social, index) => (
              <TouchableOpacity
                key={index}
                className="bg-gray-100 w-14 h-14 rounded-full items-center justify-center"
                style={{ backgroundColor: social.color + '20' }}
              >
                <Ionicons name={social.icon} size={28} color={social.color} />
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* FAQ Section */}
        <View className="px-4 py-6 mb-6">
          <Text className="text-gray-900 text-xl font-bold mb-4">Frequently Asked Questions</Text>
          {[
            {
              q: 'How quickly will I receive a response?',
              a: 'We typically respond to all inquiries within 24 hours during business days.',
            },
            {
              q: 'Can I schedule a call with your team?',
              a: 'Yes! Please mention your preferred time in the message, and we\'ll arrange a call.',
            },
            {
              q: 'Do you offer support for job seekers?',
              a: 'Absolutely! We provide comprehensive support including resume reviews, interview prep, and career guidance.',
            },
          ].map((faq, index) => (
            <View key={index} className="bg-white rounded-lg p-4 mb-3 shadow-sm border border-gray-100">
              <Text className="text-gray-900 font-bold text-base mb-2">{faq.q}</Text>
              <Text className="text-gray-600 text-sm">{faq.a}</Text>
            </View>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
