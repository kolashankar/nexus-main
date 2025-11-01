'use client';

import React, { useState } from 'react';
import { X, Filter } from 'lucide-react';
import { Button } from '@/components/ui/Button';

interface FilterOption {
  label: string;
  value: string;
}

interface JobFiltersProps {
  jobTypes?: FilterOption[];
  experienceLevels?: FilterOption[];
  onApplyFilters: (filters: any) => void;
  onReset: () => void;
}

export function JobFilters({ jobTypes = [], experienceLevels = [], onApplyFilters, onReset }: JobFiltersProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedJobTypes, setSelectedJobTypes] = useState<string[]>([]);
  const [selectedExperienceLevels, setSelectedExperienceLevels] = useState<string[]>([]);
  const [salaryRange, setSalaryRange] = useState({ min: 0, max: 500000 });

  const handleApply = () => {
    onApplyFilters({
      jobTypes: selectedJobTypes,
      experienceLevels: selectedExperienceLevels,
      salaryRange,
    });
    setIsOpen(false);
  };

  const handleReset = () => {
    setSelectedJobTypes([]);
    setSelectedExperienceLevels([]);
    setSalaryRange({ min: 0, max: 500000 });
    onReset();
  };

  return (
    <>
      {/* Mobile Filter Button */}
      <Button
        onClick={() => setIsOpen(true)}
        variant="outline"
        className="lg:hidden"
      >
        <Filter className="w-4 h-4 mr-2" />
        Filters
      </Button>

      {/* Desktop Sidebar */}
      <div className="hidden lg:block w-64 bg-white border border-gray-200 rounded-lg p-6 h-fit sticky top-20">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
          <button onClick={handleReset} className="text-sm text-blue-600 hover:text-blue-700">
            Reset
          </button>
        </div>

        {/* Job Type */}
        {jobTypes.length > 0 && (
          <div className="mb-6">
            <h4 className="text-sm font-medium text-gray-900 mb-3">Job Type</h4>
            <div className="space-y-2">
              {jobTypes.map((type) => (
                <label key={type.value} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedJobTypes.includes(type.value)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedJobTypes([...selectedJobTypes, type.value]);
                      } else {
                        setSelectedJobTypes(selectedJobTypes.filter((t) => t !== type.value));
                      }
                    }}
                    className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{type.label}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Experience Level */}
        {experienceLevels.length > 0 && (
          <div className="mb-6">
            <h4 className="text-sm font-medium text-gray-900 mb-3">Experience Level</h4>
            <div className="space-y-2">
              {experienceLevels.map((level) => (
                <label key={level.value} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedExperienceLevels.includes(level.value)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedExperienceLevels([...selectedExperienceLevels, level.value]);
                      } else {
                        setSelectedExperienceLevels(selectedExperienceLevels.filter((l) => l !== level.value));
                      }
                    }}
                    className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{level.label}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        <Button onClick={handleApply} className="w-full">
          Apply Filters
        </Button>
      </div>

      {/* Mobile Filter Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div className="fixed inset-0 bg-black bg-opacity-50" onClick={() => setIsOpen(false)} />
          <div className="fixed inset-y-0 right-0 w-full max-w-sm bg-white shadow-xl overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
                <button onClick={() => setIsOpen(false)}>
                  <X className="w-6 h-6 text-gray-400" />
                </button>
              </div>

              {/* Same filter content as desktop */}
              {jobTypes.length > 0 && (
                <div className="mb-6">
                  <h4 className="text-sm font-medium text-gray-900 mb-3">Job Type</h4>
                  <div className="space-y-2">
                    {jobTypes.map((type) => (
                      <label key={type.value} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={selectedJobTypes.includes(type.value)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setSelectedJobTypes([...selectedJobTypes, type.value]);
                            } else {
                              setSelectedJobTypes(selectedJobTypes.filter((t) => t !== type.value));
                            }
                          }}
                          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">{type.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
              )}

              {experienceLevels.length > 0 && (
                <div className="mb-6">
                  <h4 className="text-sm font-medium text-gray-900 mb-3">Experience Level</h4>
                  <div className="space-y-2">
                    {experienceLevels.map((level) => (
                      <label key={level.value} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={selectedExperienceLevels.includes(level.value)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setSelectedExperienceLevels([...selectedExperienceLevels, level.value]);
                            } else {
                              setSelectedExperienceLevels(selectedExperienceLevels.filter((l) => l !== level.value));
                            }
                          }}
                          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">{level.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
              )}

              <div className="space-y-3">
                <Button onClick={handleApply} className="w-full">
                  Apply Filters
                </Button>
                <Button onClick={handleReset} variant="outline" className="w-full">
                  Reset Filters
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
