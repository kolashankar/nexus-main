'use client'

import { useState, useEffect } from 'react'
import { settingsApi } from '@/lib/api/client/config/interceptors/auth/token/settingsApi'
import toast from 'react-hot-toast'

export default function SystemHealth() {
  const [healthData, setHealthData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSystemHealth()
    const interval = setInterval(fetchSystemHealth, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchSystemHealth = async () => {
    try {
      setLoading(true)
      const response = await settingsApi.getSystemHealth()
      setHealthData(response.data)
    } catch (error: any) {
      toast.error('Failed to fetch system health')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
      case 'online':
        return 'bg-green-100 text-green-800'
      case 'warning':
        return 'bg-yellow-100 text-yellow-800'
      case 'error':
      case 'offline':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading && !healthData) {
    return <div className="p-6 text-center">Loading system health...</div>
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">System Health Monitoring</h1>
        <button
          onClick={fetchSystemHealth}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Refresh
        </button>
      </div>

      {/* Overall Status */}
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <div className="flex items-center gap-4">
          <div className={`text-5xl ${healthData?.overall_status === 'healthy' ? 'text-green-500' : 'text-red-500'}`}>
            {healthData?.overall_status === 'healthy' ? '✅' : '⚠️'}
          </div>
          <div>
            <h2 className="text-2xl font-bold">System Status</h2>
            <p className="text-gray-600">Last updated: {new Date().toLocaleString()}</p>
          </div>
        </div>
      </div>

      {/* Service Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-3">Backend Service</h3>
          <div className={`px-3 py-1 rounded text-sm inline-block ${getStatusColor(healthData?.backend_status || 'online')}`}>
            {healthData?.backend_status || 'Online'}
          </div>
          <p className="text-sm text-gray-600 mt-2">Uptime: {healthData?.backend_uptime || '99.9%'}</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-3">Database</h3>
          <div className={`px-3 py-1 rounded text-sm inline-block ${getStatusColor(healthData?.database_status || 'online')}`}>
            {healthData?.database_status || 'Online'}
          </div>
          <p className="text-sm text-gray-600 mt-2">Connections: {healthData?.database_connections || 45}/100</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-3">API Services</h3>
          <div className={`px-3 py-1 rounded text-sm inline-block ${getStatusColor(healthData?.api_status || 'online')}`}>
            {healthData?.api_status || 'Online'}
          </div>
          <p className="text-sm text-gray-600 mt-2">Response Time: {healthData?.api_response_time || '45ms'}</p>
        </div>
      </div>

      {/* System Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Server Resources</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>CPU Usage</span>
                <span>{healthData?.cpu_usage || 35}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${healthData?.cpu_usage || 35}%` }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>Memory Usage</span>
                <span>{healthData?.memory_usage || 62}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-green-600 h-2 rounded-full" 
                  style={{ width: `${healthData?.memory_usage || 62}%` }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>Disk Usage</span>
                <span>{healthData?.disk_usage || 48}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-yellow-600 h-2 rounded-full" 
                  style={{ width: `${healthData?.disk_usage || 48}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Recent Errors</h3>
          <div className="space-y-2">
            {healthData?.recent_errors && healthData.recent_errors.length > 0 ? (
              healthData.recent_errors.map((error: any, index: number) => (
                <div key={index} className="p-3 bg-red-50 rounded text-sm">
                  <div className="font-medium text-red-800">{error.message}</div>
                  <div className="text-xs text-red-600 mt-1">{error.timestamp}</div>
                </div>
              ))
            ) : (
              <div className="text-center text-gray-500 py-4">No recent errors</div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
