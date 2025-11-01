'use client'

import { useState } from 'react'
import { reportsApi } from '@/lib/api/client/config/interceptors/auth/token/reportsApi'
import toast from 'react-hot-toast'
import Link from 'next/link'
import jsPDF from 'jspdf'

export default function Reports() {
  const [loading, setLoading] = useState(false)
  const [reportType, setReportType] = useState('users')
  const [dateRange, setDateRange] = useState('30')

  const generateReport = async () => {
    try {
      setLoading(true)
      const config = {
        type: reportType,
        date_range: parseInt(dateRange),
      }
      const response = await reportsApi.buildReport(config)
      toast.success('Report generated successfully')
      // Handle report data
    } catch (error: any) {
      toast.error('Failed to generate report')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const exportPDF = async () => {
    try {
      const reportData = { type: reportType, date_range: parseInt(dateRange) }
      const response = await reportsApi.exportPDF(reportData)
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `report_${Date.now()}.pdf`
      a.click()
      toast.success('PDF exported successfully')
    } catch (error: any) {
      toast.error('Failed to export PDF')
    }
  }

  const exportCSV = async () => {
    try {
      const reportData = { type: reportType, date_range: parseInt(dateRange) }
      const response = await reportsApi.exportCSV(reportData)
      const blob = new Blob([response.data], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `report_${Date.now()}.csv`
      a.click()
      toast.success('CSV exported successfully')
    } catch (error: any) {
      toast.error('Failed to export CSV')
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Reports</h1>

      {/* Quick Links */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Link
          href="/dashboard/reports/builder"
          className="bg-white p-6 rounded-lg shadow hover:shadow-lg text-center"
        >
          <div className="text-4xl mb-3">🔧</div>
          <h3 className="text-lg font-bold">Report Builder</h3>
          <p className="text-sm text-gray-600 mt-1">Create custom reports</p>
        </Link>
        <Link
          href="/dashboard/reports/scheduled"
          className="bg-white p-6 rounded-lg shadow hover:shadow-lg text-center"
        >
          <div className="text-4xl mb-3">⏰</div>
          <h3 className="text-lg font-bold">Scheduled Reports</h3>
          <p className="text-sm text-gray-600 mt-1">Automated reporting</p>
        </Link>
        <Link
          href="/dashboard/reports/email"
          className="bg-white p-6 rounded-lg shadow hover:shadow-lg text-center"
        >
          <div className="text-4xl mb-3">📧</div>
          <h3 className="text-lg font-bold">Email Reports</h3>
          <p className="text-sm text-gray-600 mt-1">Send reports via email</p>
        </Link>
      </div>

      {/* Quick Report Generator */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Quick Report Generator</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Report Type</label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="users">User Statistics</option>
              <option value="jobs">Jobs Report</option>
              <option value="internships">Internships Report</option>
              <option value="applications">Applications Report</option>
              <option value="revenue">Revenue Report</option>
              <option value="engagement">Engagement Metrics</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Date Range</label>
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="7">Last 7 Days</option>
              <option value="30">Last 30 Days</option>
              <option value="90">Last 90 Days</option>
              <option value="365">Last Year</option>
            </select>
          </div>

          <div className="flex gap-4">
            <button
              onClick={generateReport}
              disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Generating...' : 'Generate Report'}
            </button>
            <button
              onClick={exportPDF}
              className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700"
            >
              Export PDF
            </button>
            <button
              onClick={exportCSV}
              className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
            >
              Export CSV
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
