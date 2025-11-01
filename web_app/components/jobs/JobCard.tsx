'use client';

import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Job } from '@/types';
import { useBookmarkStore } from '@/store/bookmarkStore';
import { MapPin, Briefcase, Clock, DollarSign, Bookmark } from 'lucide-react';
import { formatDate, formatSalary } from '@/lib/utils';
import { toast } from 'react-hot-toast';

interface JobCardProps {
  job: Job;
}

export function JobCard({ job }: JobCardProps) {
  const { isJobBookmarked, toggleJobBookmark } = useBookmarkStore();
  const isBookmarked = isJobBookmarked(job.id);

  const handleBookmark = (e: React.MouseEvent) => {
    e.preventDefault();
    toggleJobBookmark(job.id);
    toast.success(isBookmarked ? 'Removed from bookmarks' : 'Added to bookmarks');
  };

  return (
    <Link href={`/jobs/${job.id}`}>
      <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer group">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-start space-x-3 flex-1">
              {job.company_logo ? (
                <img
                  src={job.company_logo}
                  alt={job.company}
                  className="w-12 h-12 rounded-lg object-cover"
                />
              ) : (
                <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center">
                  <Briefcase className="w-6 h-6 text-blue-600" />
                </div>
              )}
              <div className="flex-1 min-w-0">
                <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2">
                  {job.title}
                </h3>
                <p className="text-sm text-gray-600">{job.company}</p>
              </div>
            </div>
            <button
              onClick={handleBookmark}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <Bookmark
                className={`w-5 h-5 ${
                  isBookmarked ? 'fill-blue-600 text-blue-600' : 'text-gray-400'
                }`}
              />
            </button>
          </div>

          {/* Details */}
          <div className="space-y-2 mb-4">
            <div className="flex items-center text-sm text-gray-600">
              <MapPin className="w-4 h-4 mr-2" />
              {job.location}
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <Briefcase className="w-4 h-4 mr-2" />
              {job.job_type} • {job.experience_level}
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <DollarSign className="w-4 h-4 mr-2" />
              {formatSalary(job.salary_min, job.salary_max, job.salary_currency)}
            </div>
            <div className="flex items-center text-sm text-gray-500">
              <Clock className="w-4 h-4 mr-2" />
              Posted {formatDate(job.posted_at)}
            </div>
          </div>

          {/* Category Badge */}
          <div className="mb-4">
            <span className="inline-block px-3 py-1 text-xs font-medium bg-blue-50 text-blue-700 rounded-full">
              {job.category}
            </span>
          </div>

          {/* Skills */}
          {job.skills && job.skills.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {job.skills.slice(0, 4).map((skill, index) => (
                <span
                  key={index}
                  className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"
                >
                  {skill}
                </span>
              ))}
              {job.skills.length > 4 && (
                <span className="px-2 py-1 text-xs text-gray-500">
                  +{job.skills.length - 4} more
                </span>
              )}
            </div>
          )}

          {/* Footer */}
          <div className="pt-4 border-t">
            <Button variant="outline" className="w-full group-hover:bg-blue-50 group-hover:text-blue-600 group-hover:border-blue-600">
              View Details
            </Button>
          </div>
        </div>
      </Card>
    </Link>
  );
}
