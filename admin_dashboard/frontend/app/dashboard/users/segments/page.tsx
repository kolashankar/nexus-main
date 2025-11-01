'use client'

import { useState, useEffect } from 'react'
import { usersApi } from '@/lib/api/client/config/interceptors/auth/token/usersApi'
import toast from 'react-hot-toast'
import { Pie } from 'react-chartjs-2'

export default function UserSegments() {
  const [segments, setSegments] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSegments()
  }, [])

  const fetchSegments = async () => {
    try {
      setLoading(true)
      const response = await usersApi.getSegments()
      setSegments(response.data)
    } catch (error: any) {
      toast.error('Failed to fetch segments')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="p-6 text-center">Loading segments...</div>
  }

  const chartData = {
    labels: Object.keys(segments || {}),
    datasets: [
      {
        data: Object.values(segments || {}),
        backgroundColor: ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'],
      },
    ],
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">User Segmentation</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">User Distribution</h3>
          <Pie data={chartData} />
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Segment Details</h3>
          <div className="space-y-3">
            {Object.entries(segments || {}).map(([key, value]: [string, any]) => (
              <div key={key} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="font-medium">{key}</span>
                <span className="text-2xl font-bold text-blue-600">{value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
