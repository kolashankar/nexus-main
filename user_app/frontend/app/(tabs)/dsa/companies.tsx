import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import api from '../../../lib/api';
import SearchBar from '../../../components/common/SearchBar';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';

interface Company {
  _id: string;
  name: string;
  logo: string;
  industry: string;
  problem_count: number;
  job_count: number;
}

export default function CompaniesScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();

  const { data, isLoading, isError, refetch, isFetching } = useQuery({
    queryKey: ['dsa-companies', searchQuery],
    queryFn: async () => {
      const params: any = {};
      if (searchQuery) params.search = searchQuery;
      
      const response = await api.get('/admin/dsa/companies', { params });
      return response.data.companies || [];
    },
  });

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <LoadingSpinner message="Loading companies..." />
      </SafeAreaView>
    );
  }

  if (isError) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <EmptyState
          icon="alert-circle-outline"
          title="Error Loading Companies"
          message="Failed to load companies. Please try again."
        />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-dark-400">
      {/* Header */}
      <View className="flex-row items-center px-6 py-4">
        <TouchableOpacity onPress={() => router.back()} className="mr-4">
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text className="text-white text-xl font-bold">Companies</Text>
      </View>

      <SearchBar
        value={searchQuery}
        onChangeText={setSearchQuery}
        placeholder="Search companies..."
      />

      <ScrollView
        className="flex-1 px-4"
        refreshControl={
          <RefreshControl
            refreshing={isFetching}
            onRefresh={refetch}
            tintColor="#3b82f6"
          />
        }
      >
        {data && data.length === 0 ? (
          <EmptyState
            icon="business-outline"
            title="No Companies Found"
            message="No companies available. Check back later!"
          />
        ) : (
          data?.map((company: Company) => (
            <TouchableOpacity
              key={company._id}
              className="bg-dark-200 rounded-lg p-4 mb-3 flex-row items-center"
              onPress={() => router.push(`/dsa/company-${company._id}`)}
            >
              <View className="bg-white w-12 h-12 rounded-lg items-center justify-center mr-4">
                <Text className="text-2xl">{company.logo}</Text>
              </View>
              <View className="flex-1">
                <Text className="text-white text-lg font-bold" numberOfLines={1}>
                  {company.name}
                </Text>
                <Text className="text-gray-400 text-sm mt-1">{company.industry}</Text>
                <View className="flex-row items-center mt-2">
                  <View className="flex-row items-center mr-4">
                    <Ionicons name="code-outline" size={14} color="#9ca3af" />
                    <Text className="text-gray-400 text-xs ml-1">
                      {company.problem_count} problems
                    </Text>
                  </View>
                  <View className="flex-row items-center">
                    <Ionicons name="briefcase-outline" size={14} color="#9ca3af" />
                    <Text className="text-gray-400 text-xs ml-1">
                      {company.job_count} jobs
                    </Text>
                  </View>
                </View>
              </View>
              <Ionicons name="chevron-forward" size={24} color="#9ca3af" />
            </TouchableOpacity>
          ))
        )}
      </ScrollView>
    </SafeAreaView>
  );
}