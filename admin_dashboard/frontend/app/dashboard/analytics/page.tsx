'use client'

import { useState, useEffect } from 'react'
import { Line, Bar, Pie, Doughnut } from 'react-chartjs-2'
import { analyticsApi } from '@/lib/api/client/config/interceptors/auth/token/analyticsApi'
import DatePicker from 'react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import { saveAs } from 'file-saver'

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

export default function EnhancedAnalytics() {
  const [loading, setLoading] = useState(true)
  const [dashboardData, setDashboardData] = useState<any>(null)
  const [startDate, setStartDate] = useState(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000))
  const [endDate, setEndDate] = useState(new Date())

  useEffect(() => {
    fetchAnalytics()
  }, [startDate, endDate])

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      const response = await analyticsApi.getDashboard()
      setDashboardData(response.data)
    } catch (error: any) {
      console.error('Failed to fetch analytics', error)
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async (format: 'csv' | 'pdf') => {
    try {
      // Export functionality - would need backend endpoint
      console.log(`Exporting as ${format}`)
      alert(`Export to ${format} - Backend endpoint needed`)
    } catch (error: any) {
      console.error('Failed to export', error)
    }
  }

  if (loading) {
    return <div className="p-6 text-center">Loading analytics...</div>
  }

  const userEngagementData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'Active Users',
        data: [150, 200, 180, 220, 250, 300, 280],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
      },
    ],
  }

  const jobApplicationsData = {
    labels: ['Jobs', 'Internships', 'Scholarships'],
    datasets: [
      {
        data: [dashboardData?.jobs_count || 0, dashboardData?.internships_count || 0, dashboardData?.scholarships_count || 0],
        backgroundColor: ['#3b82f6', '#8b5cf6', '#10b981'],
      },
    ],
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Enhanced Analytics</h1>

      {/* Date Range Selector */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="flex items-center gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Start Date</label>
            <DatePicker
              selected={startDate}
              onChange={(date) => date && setStartDate(date)}
              className="px-4 py-2 border rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">End Date</label>
            <DatePicker
              selected={endDate}
              onChange={(date) => date && setEndDate(date)}
              className="px-4 py-2 border rounded-lg"
            />
          </div>
          <div className="flex gap-2 mt-6">
            <button
              onClick={() => handleExport('csv')}
              className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
            >
              Export CSV
            </button>
            <button
              onClick={() => handleExport('pdf')}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
            >
              Export PDF
            </button>
          </div>
        </div>
      </div>

      {/* Real-time Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm mb-2">Total Users</h3>
          <p className="text-3xl font-bold">{dashboardData?.total_users || 0}</p>
          <p className="text-sm text-green-600 mt-1">↑ 12% this month</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm mb-2">Total Jobs</h3>
          <p className="text-3xl font-bold">{dashboardData?.jobs_count || 0}</p>
          <p className="text-sm text-green-600 mt-1">↑ 8% this week</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm mb-2">Active Applications</h3>
          <p className="text-3xl font-bold">{dashboardData?.applications_count || 0}</p>
          <p className="text-sm text-red-600 mt-1">↓ 5% today</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm mb-2">Gemini API Calls</h3>
          <p className="text-3xl font-bold">{dashboardData?.gemini_calls || 0}</p>
          <p className="text-sm text-green-600 mt-1">↑ 20% this week</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">User Engagement (Last 7 Days)</h3>
          <Line data={userEngagementData} />
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Content Distribution</h3>
          <Doughnut data={jobApplicationsData} />
        </div>
      </div>

      {/* Conversion Funnel */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-bold mb-4">Conversion Funnel</h3>
        <div className="space-y-3">
          <div className="flex items-center gap-4">
            <div className="w-full bg-gray-200 rounded-full h-8">
              <div className="bg-blue-600 h-8 rounded-full flex items-center justify-center text-white text-sm" style={{ width: '100%' }}>
                Visitors: 10,000
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-full bg-gray-200 rounded-full h-8">
              <div className="bg-blue-600 h-8 rounded-full flex items-center justify-center text-white text-sm" style={{ width: '70%' }}>
                Registrations: 7,000
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-full bg-gray-200 rounded-full h-8">
              <div className="bg-blue-600 h-8 rounded-full flex items-center justify-center text-white text-sm" style={{ width: '40%' }}>
                Applications: 4,000
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="w-full bg-gray-200 rounded-full h-8">
              <div className="bg-blue-600 h-8 rounded-full flex items-center justify-center text-white text-sm" style={{ width: '15%' }}>
                Hired: 1,500
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
