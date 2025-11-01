'use client';

import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { DSACompany } from '@/types';
import { Briefcase, Code, Building } from 'lucide-react';

interface CompanyCardProps {
  company: DSACompany;
}

export function CompanyCard({ company }: CompanyCardProps) {
  return (
    <Link href={`/dsa/companies/${company.id}`}>
      <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer group">
        <div className="p-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center space-x-3">
              {company.logo ? (
                <img
                  src={company.logo}
                  alt={company.name}
                  className="w-12 h-12 rounded-lg object-cover"
                />
              ) : (
                <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center">
                  <Building className="w-6 h-6 text-blue-600" />
                </div>
              )}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                  {company.name}
                </h3>
                <p className="text-sm text-gray-500">{company.industry}</p>
              </div>
            </div>
          </div>
          
          <div className="space-y-3">
            <div className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded-lg">
              <div className="flex items-center text-sm text-gray-600">
                <Code className="w-4 h-4 mr-2" />
                Problems
              </div>
              <span className="font-semibold text-gray-900">{company.problem_count}</span>
            </div>
            
            <div className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded-lg">
              <div className="flex items-center text-sm text-gray-600">
                <Briefcase className="w-4 h-4 mr-2" />
                Job Openings
              </div>
              <span className="font-semibold text-gray-900">{company.job_count}</span>
            </div>
          </div>
        </div>
      </Card>
    </Link>
  );
}