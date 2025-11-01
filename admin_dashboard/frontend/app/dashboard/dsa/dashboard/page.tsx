'use client'

import { useState, useEffect } from 'react'
import { dsaApi } from '@/lib/api/client/config/interceptors/auth/token/dsaApi'
import { Line, Bar, Pie } from 'react-chartjs-2'
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

export default function DSADashboard() {
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      setLoading(true)
      const [topicsStats, questionsStatsDiff, questionsStatsTopic, sheetsStats, companiesStats] = await Promise.all([
        dsaApi.topics.getStats(),
        dsaApi.questions.getStatsByDifficulty(),
        dsaApi.questions.getStatsByTopic(),
        dsaApi.sheets.getStats(),
        dsaApi.companies.getStats(),
      ])

      setStats({
        topics: topicsStats.data,
        questionsDifficulty: questionsStatsDiff.data,
        questionsTopic: questionsStatsTopic.data,
        sheets: sheetsStats.data,
        companies: companiesStats.data,
      })
    } catch (error: any) {
      console.error('Failed to fetch stats', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="p-6 text-center">Loading dashboard...</div>
  }

  const difficultyData = {
    labels: Object.keys(stats.questionsDifficulty || {}),
    datasets: [
      {
        label: 'Questions by Difficulty',
        data: Object.values(stats.questionsDifficulty || {}),
        backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
      },
    ],
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">DSA Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm mb-2">Total Topics</h3>
          <p className="text-3xl font-bold">{stats.topics?.total || 0}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm mb-2">Total Questions</h3>
          <p className="text-3xl font-bold">{String(Object.values(stats.questionsDifficulty || {}).reduce((a: any, b: any) => a + b, 0))}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm mb-2">Total Sheets</h3>
          <p className="text-3xl font-bold">{stats.sheets?.total || 0}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm mb-2">Total Companies</h3>
          <p className="text-3xl font-bold">{stats.companies?.total || 0}</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Questions by Difficulty</h3>
          <Pie data={difficultyData} />
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Quick Links</h3>
          <div className="space-y-3">
            <a href="/dashboard/dsa/topics/list" className="block p-3 bg-blue-50 rounded hover:bg-blue-100">
              📚 Manage Topics
            </a>
            <a href="/dashboard/dsa/questions/list" className="block p-3 bg-green-50 rounded hover:bg-green-100">
              ❓ Manage Questions
            </a>
            <a href="/dashboard/dsa/sheets/list" className="block p-3 bg-purple-50 rounded hover:bg-purple-100">
              📋 Manage Sheets
            </a>
            <a href="/dashboard/dsa/companies/list" className="block p-3 bg-orange-50 rounded hover:bg-orange-100">
              🏢 Manage Companies
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
