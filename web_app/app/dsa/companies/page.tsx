'use client';

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { CompanyCard } from '@/components/dsa/CompanyCard';
import { SearchBar } from '@/components/common/SearchBar';
import { Skeleton } from '@/components/ui/Skeleton';
import { Button } from '@/components/ui/Button';
import { Building } from 'lucide-react';
import { DSACompany } from '@/types';

export default function DSACompaniesPage() {
  const [searchQuery, setSearchQuery] = useState('');

  const { data, isLoading, error } = useQuery({
    queryKey: ['dsa-companies', searchQuery],
    queryFn: async () => {
      const params: any = {
        search: searchQuery || undefined,
      };
      const response = await apiClient.getDSACompanies(params);
      return response;
    },
  });

  const companies: DSACompany[] = data?.data || [];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center mb-4">
            <Building className="w-6 h-6 text-orange-600 mr-2" />
            <h1 className="text-2xl font-bold text-gray-900">DSA Companies</h1>
          </div>
          <p className="text-gray-600">Practice problems asked by top tech companies</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <SearchBar
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="Search companies..."
          />
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
              <Skeleton key={i} className="h-48" />
            ))}
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <p className="text-red-600 mb-4">Failed to load companies</p>
            <Button onClick={() => window.location.reload()}>Try Again</Button>
          </div>
        ) : companies.length === 0 ? (
          <div className="text-center py-12">
            <Building className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No companies found</h3>
            <p className="text-gray-600">Try adjusting your search</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {companies.map((company) => (
              <CompanyCard key={company.id} company={company} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}