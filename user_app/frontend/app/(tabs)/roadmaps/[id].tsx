import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  Modal,
  Dimensions,
  RefreshControl
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import Svg, { Circle, Line, Text as SvgText, G, Rect } from 'react-native-svg';
import api from '@/lib/api';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import EmptyState from '@/components/common/EmptyState';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
const NODE_RADIUS = 30;
const NODE_SPACING_X = 120;
const NODE_SPACING_Y = 100;

interface RoadmapNode {
  id: string;
  title: string;
  description: string;
  type: 'content' | 'roadmap_link' | 'article_link';
  position_x: number;
  position_y: number;
  content?: string;
  video_url?: string;
  article_link?: string;
  roadmap_link?: string;
  connections: string[];
  is_completed?: boolean;
}

interface Roadmap {
  _id: string;
  title: string;
  description: string;
  category: string;
  difficulty_level: string;
  estimated_duration: string;
  nodes: RoadmapNode[];
}

export default function RoadmapDetailScreen() {
  const { id } = useLocalSearchParams();
  const [refreshing, setRefreshing] = useState(false);
  const [selectedNode, setSelectedNode] = useState<RoadmapNode | null>(null);
  const [showNodeModal, setShowNodeModal] = useState(false);
  const [scale, setScale] = useState(1);
  const [panOffset, setPanOffset] = useState({ x: 0, y: 0 });
  const scrollViewRef = useRef<ScrollView>(null);

  const { data: roadmap, isLoading, refetch } = useQuery({
    queryKey: ['roadmap', id],
    queryFn: async () => {
      const response = await api.get(`/admin/roadmaps/${id}`);
      return response.data.data;
    }
  });

  const onRefresh = async () => {
    setRefreshing(true);
    await refetch();
    setRefreshing(false);
  };

  const handleNodePress = (node: RoadmapNode) => {
    setSelectedNode(node);
    setShowNodeModal(true);
  };

  const toggleNodeCompletion = async (nodeId: string) => {
    // Here you would make an API call to update node completion status
    // For now, we'll just update the local state
    if (selectedNode) {
      setSelectedNode({
        ...selectedNode,
        is_completed: !selectedNode.is_completed
      });
    }
  };

  const getNodeColor = (node: RoadmapNode) => {
    if (node.is_completed) return '#10b981'; // Green for completed
    if (node.type === 'content') return '#3b82f6'; // Blue for content
    if (node.type === 'roadmap_link') return '#8b5cf6'; // Purple for roadmap links
    if (node.type === 'article_link') return '#f59e0b'; // Orange for article links
    return '#6b7280'; // Gray default
  };

  const calculateCompletionPercentage = () => {
    if (!roadmap?.nodes) return 0;
    const completedNodes = roadmap.nodes.filter((n: RoadmapNode) => n.is_completed).length;
    return Math.round((completedNodes / roadmap.nodes.length) * 100);
  };

  const renderFlowchart = () => {
    if (!roadmap?.nodes || roadmap.nodes.length === 0) return null;

    // Calculate bounds for the flowchart
    const maxX = Math.max(...roadmap.nodes.map((n: RoadmapNode) => n.position_x));
    const maxY = Math.max(...roadmap.nodes.map((n: RoadmapNode) => n.position_y));
    
    const svgWidth = Math.max(SCREEN_WIDTH, maxX + 200);
    const svgHeight = Math.max(600, maxY + 200);

    return (
      <Svg width={svgWidth} height={svgHeight}>
        {/* Render connections first (lines) */}
        {roadmap.nodes.map((node: RoadmapNode) => 
          node.connections?.map((targetId: string) => {
            const targetNode = roadmap.nodes.find((n: RoadmapNode) => n.id === targetId);
            if (!targetNode) return null;

            return (
              <Line
                key={`${node.id}-${targetId}`}
                x1={node.position_x}
                y1={node.position_y}
                x2={targetNode.position_x}
                y2={targetNode.position_y}
                stroke={node.is_completed && targetNode.is_completed ? '#10b981' : '#e5e7eb'}
                strokeWidth="2"
              />
            );
          })
        )}

        {/* Render nodes */}
        {roadmap.nodes.map((node: RoadmapNode, index: number) => {
          const nodeColor = getNodeColor(node);
          
          return (
            <G key={node.id}>
              {/* Node circle */}
              <Circle
                cx={node.position_x}
                cy={node.position_y}
                r={NODE_RADIUS}
                fill={nodeColor}
                stroke={node.is_completed ? '#10b981' : '#fff'}
                strokeWidth="3"
                onPress={() => handleNodePress(node)}
              />
              
              {/* Checkmark for completed nodes */}
              {node.is_completed && (
                <SvgText
                  x={node.position_x}
                  y={node.position_y + 5}
                  fontSize="24"
                  fill="#fff"
                  textAnchor="middle"
                >
                  ✓
                </SvgText>
              )}

              {/* Node label */}
              <SvgText
                x={node.position_x}
                y={node.position_y + NODE_RADIUS + 20}
                fontSize="12"
                fill="#1f2937"
                textAnchor="middle"
                fontWeight="600"
              >
                {node.title.substring(0, 15)}
              </SvgText>
            </G>
          );
        })}
      </Svg>
    );
  };

  if (isLoading) return <LoadingSpinner />;
  if (!roadmap) return <EmptyState message="Roadmap not found" />;

  const completionPercentage = calculateCompletionPercentage();

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      <ScrollView
        ref={scrollViewRef}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* Header */}
        <View className="bg-white p-6 border-b border-gray-200">
          <TouchableOpacity
            onPress={() => router.back()}
            className="mb-4"
          >
            <Ionicons name="arrow-back" size={24} color="#000" />
          </TouchableOpacity>

          <Text className="text-2xl font-bold text-gray-900 mb-2">
            {roadmap.title}
          </Text>
          <Text className="text-gray-600 mb-4">{roadmap.description}</Text>

          {/* Stats */}
          <View className="flex-row items-center space-x-4">
            <View className="flex-1 bg-blue-50 p-3 rounded-lg">
              <Text className="text-xs text-gray-600 mb-1">Difficulty</Text>
              <Text className="text-base font-semibold text-blue-600">
                {roadmap.difficulty_level}
              </Text>
            </View>
            <View className="flex-1 bg-green-50 p-3 rounded-lg">
              <Text className="text-xs text-gray-600 mb-1">Duration</Text>
              <Text className="text-base font-semibold text-green-600">
                {roadmap.estimated_duration}h
              </Text>
            </View>
            <View className="flex-1 bg-purple-50 p-3 rounded-lg">
              <Text className="text-xs text-gray-600 mb-1">Topics</Text>
              <Text className="text-base font-semibold text-purple-600">
                {roadmap.nodes?.length || 0}
              </Text>
            </View>
          </View>

          {/* Progress */}
          <View className="mt-4">
            <View className="flex-row justify-between mb-2">
              <Text className="text-sm font-semibold text-gray-700">Your Progress</Text>
              <Text className="text-sm font-semibold text-blue-600">
                {completionPercentage}%
              </Text>
            </View>
            <View className="h-3 bg-gray-200 rounded-full overflow-hidden">
              <View
                className="h-full bg-blue-500"
                style={{ width: `${completionPercentage}%` }}
              />
            </View>
          </View>
        </View>

        {/* Legend */}
        <View className="bg-white p-4 mt-2 border-b border-gray-200">
          <Text className="text-sm font-semibold text-gray-700 mb-3">Legend</Text>
          <View className="flex-row flex-wrap">
            <View className="flex-row items-center mr-4 mb-2">
              <View className="w-4 h-4 rounded-full bg-blue-500 mr-2" />
              <Text className="text-xs text-gray-600">Content</Text>
            </View>
            <View className="flex-row items-center mr-4 mb-2">
              <View className="w-4 h-4 rounded-full bg-purple-500 mr-2" />
              <Text className="text-xs text-gray-600">Roadmap</Text>
            </View>
            <View className="flex-row items-center mr-4 mb-2">
              <View className="w-4 h-4 rounded-full bg-orange-500 mr-2" />
              <Text className="text-xs text-gray-600">Article</Text>
            </View>
            <View className="flex-row items-center mb-2">
              <View className="w-4 h-4 rounded-full bg-green-500 mr-2" />
              <Text className="text-xs text-gray-600">Completed</Text>
            </View>
          </View>
        </View>

        {/* Flowchart */}
        <View className="bg-white p-4 mt-2">
          <View className="flex-row justify-between items-center mb-4">
            <Text className="text-lg font-semibold text-gray-900">Learning Path</Text>
            <View className="flex-row space-x-2">
              <TouchableOpacity
                onPress={() => setScale(Math.max(0.5, scale - 0.1))}
                className="bg-gray-100 p-2 rounded-lg"
              >
                <Ionicons name="remove" size={20} color="#000" />
              </TouchableOpacity>
              <TouchableOpacity
                onPress={() => setScale(Math.min(2, scale + 0.1))}
                className="bg-gray-100 p-2 rounded-lg"
              >
                <Ionicons name="add" size={20} color="#000" />
              </TouchableOpacity>
            </View>
          </View>

          <ScrollView horizontal showsHorizontalScrollIndicator>
            <View style={{ transform: [{ scale }] }}>
              {renderFlowchart()}
            </View>
          </ScrollView>
        </View>

        {/* Tips */}
        <View className="bg-white p-6 mt-2 mb-6">
          <Text className="text-lg font-semibold text-gray-900 mb-4">How to Use</Text>
          <View className="space-y-3">
            <View className="flex-row">
              <Ionicons name="hand-left-outline" size={20} color="#3b82f6" />
              <Text className="flex-1 ml-3 text-gray-700">
                Tap on any node to view its content and resources
              </Text>
            </View>
            <View className="flex-row">
              <Ionicons name="checkmark-circle-outline" size={20} color="#3b82f6" />
              <Text className="flex-1 ml-3 text-gray-700">
                Mark nodes as complete to track your progress
              </Text>
            </View>
            <View className="flex-row">
              <Ionicons name="git-network-outline" size={20} color="#3b82f6" />
              <Text className="flex-1 ml-3 text-gray-700">
                Follow the connections to see the recommended learning path
              </Text>
            </View>
          </View>
        </View>
      </ScrollView>

      {/* Node Detail Modal */}
      <Modal
        visible={showNodeModal}
        animationType="slide"
        transparent
        onRequestClose={() => setShowNodeModal(false)}
      >
        <View className="flex-1 justify-end bg-black/50">
          <View className="bg-white rounded-t-3xl max-h-4/5">
            <ScrollView>
              {selectedNode && (
                <View className="p-6">
                  {/* Header */}
                  <View className="flex-row justify-between items-start mb-4">
                    <View className="flex-1 mr-4">
                      <Text className="text-2xl font-bold text-gray-900 mb-2">
                        {selectedNode.title}
                      </Text>
                      <View className={`self-start px-3 py-1 rounded-full ${
                        selectedNode.type === 'content' ? 'bg-blue-100' :
                        selectedNode.type === 'roadmap_link' ? 'bg-purple-100' :
                        'bg-orange-100'
                      }`}>
                        <Text className="text-xs font-semibold">
                          {selectedNode.type.replace('_', ' ').toUpperCase()}
                        </Text>
                      </View>
                    </View>
                    <TouchableOpacity
                      onPress={() => setShowNodeModal(false)}
                      className="bg-gray-100 p-2 rounded-full"
                    >
                      <Ionicons name="close" size={24} color="#000" />
                    </TouchableOpacity>
                  </View>

                  {/* Description */}
                  <Text className="text-gray-700 text-base mb-6 leading-6">
                    {selectedNode.description}
                  </Text>

                  {/* Content */}
                  {selectedNode.content && (
                    <View className="mb-6">
                      <Text className="text-lg font-semibold text-gray-900 mb-3">
                        Content
                      </Text>
                      <Text className="text-gray-700 leading-6">
                        {selectedNode.content}
                      </Text>
                    </View>
                  )}

                  {/* Video URL */}
                  {selectedNode.video_url && (
                    <TouchableOpacity className="bg-red-50 p-4 rounded-lg mb-4 flex-row items-center">
                      <Ionicons name="play-circle" size={24} color="#ef4444" />
                      <Text className="ml-3 text-red-600 font-semibold">
                        Watch Video Tutorial
                      </Text>
                    </TouchableOpacity>
                  )}

                  {/* Article Link */}
                  {selectedNode.article_link && (
                    <TouchableOpacity
                      className="bg-orange-50 p-4 rounded-lg mb-4 flex-row items-center"
                      onPress={() => {
                        setShowNodeModal(false);
                        router.push(`/learning/${selectedNode.article_link}`);
                      }}
                    >
                      <Ionicons name="document-text" size={24} color="#f59e0b" />
                      <Text className="ml-3 text-orange-600 font-semibold">
                        Read Article
                      </Text>
                    </TouchableOpacity>
                  )}

                  {/* Roadmap Link */}
                  {selectedNode.roadmap_link && (
                    <TouchableOpacity
                      className="bg-purple-50 p-4 rounded-lg mb-4 flex-row items-center"
                      onPress={() => {
                        setShowNodeModal(false);
                        router.push(`/roadmaps/${selectedNode.roadmap_link}`);
                      }}
                    >
                      <Ionicons name="map" size={24} color="#8b5cf6" />
                      <Text className="ml-3 text-purple-600 font-semibold">
                        Open Related Roadmap
                      </Text>
                    </TouchableOpacity>
                  )}

                  {/* Completion Toggle */}
                  <TouchableOpacity
                    onPress={() => toggleNodeCompletion(selectedNode.id)}
                    className={`p-4 rounded-lg flex-row items-center justify-center ${
                      selectedNode.is_completed ? 'bg-green-500' : 'bg-blue-500'
                    }`}
                  >
                    <Ionicons
                      name={selectedNode.is_completed ? 'checkmark-circle' : 'ellipse-outline'}
                      size={24}
                      color="#fff"
                    />
                    <Text className="ml-2 text-white font-semibold text-base">
                      {selectedNode.is_completed ? 'Completed' : 'Mark as Complete'}
                    </Text>
                  </TouchableOpacity>
                </View>
              )}
            </ScrollView>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}
