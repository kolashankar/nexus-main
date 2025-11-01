'use client'

import { useEffect, useState } from 'react'
import { careerToolsApi, type CareerToolStats } from '@/lib/api/client/config/interceptors/auth/token/careerToolsApi'
import DashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/DashboardLayout'
import Link from 'next/link'

export default function CareerToolsStatsPage() {
  const [stats, setStats] = useState<CareerToolStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setLoading(true)
      const response = await careerToolsApi.getStats()
      setStats(response.stats)
    } catch (error) {
      console.error('Error fetching stats:', error)
      alert('Failed to fetch statistics')
    } finally {
      setLoading(false)
    }
  }

  const getToolLabel = (type: string) => {
    const labels: { [key: string]: string } = {
      resume_review: 'Resume Review',
      cover_letter: 'Cover Letter',
      ats_hack: 'ATS Hack',
      cold_email: 'Cold Email',
    }
    return labels[type] || type
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Career Tools Statistics</h1>
            <p className="text-gray-600 mt-1">Usage analytics and insights</p>
          </div>
          <Link
            href="/dashboard/career-tools/templates"
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
          >
            Manage Templates
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-8">Loading...</div>
        ) : stats ? (
          <>
            {/* Total Usage Card */}
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
              <h2 className="text-xl font-semibold mb-2">Total Usage</h2>
              <p className="text-5xl font-bold">{stats.total_usage}</p>
              <p className="text-blue-100 mt-2">All-time career tool interactions</p>
            </div>

            {/* Usage by Tool */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Usage by Tool</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-blue-50 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-3xl">📝</span>
                    <span className="text-2xl font-bold text-blue-600">{stats.usage_by_tool.resume_review}</span>
                  </div>
                  <p className="text-gray-700 font-medium">Resume Review</p>
                </div>

                <div className="bg-green-50 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-3xl">✉️</span>
                    <span className="text-2xl font-bold text-green-600">{stats.usage_by_tool.cover_letter}</span>
                  </div>
                  <p className="text-gray-700 font-medium">Cover Letter</p>
                </div>

                <div className="bg-purple-50 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-3xl">🎯</span>
                    <span className="text-2xl font-bold text-purple-600">{stats.usage_by_tool.ats_hack}</span>
                  </div>
                  <p className="text-gray-700 font-medium">ATS Hack</p>
                </div>

                <div className="bg-orange-50 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-3xl">📧</span>
                    <span className="text-2xl font-bold text-orange-600">{stats.usage_by_tool.cold_email}</span>
                  </div>
                  <p className="text-gray-700 font-medium">Cold Email</p>
                </div>
              </div>
            </div>

            {/* Recent Usage */}
            {stats.recent_usage && stats.recent_usage.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Usage</h2>
                <div className="space-y-3">
                  {stats.recent_usage.map((usage, idx) => (
                    <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <p className="font-semibold text-gray-900">{getToolLabel(usage.tool_type)}</p>
                        <p className="text-sm text-gray-500">User: {usage.user_id}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-500">
                          {new Date(usage.created_at!).toLocaleDateString()}
                        </p>
                        <p className="text-xs text-gray-400">
                          {new Date(usage.created_at!).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="bg-white p-8 rounded-lg shadow text-center">
            <p className="text-gray-500">No statistics available</p>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
