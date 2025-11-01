'use client'

import { useState } from 'react'
import { bulkApi } from '@/lib/api/client/config/interceptors/auth/token/bulkApi'
import toast from 'react-hot-toast'

export default function BulkOperations() {
  const [activeTab, setActiveTab] = useState('jobs')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
    }
  }

  const handleImport = async () => {
    if (!selectedFile) {
      toast.error('Please select a file first')
      return
    }

    try {
      setLoading(true)
      if (activeTab === 'jobs') {
        await bulkApi.importJobs(selectedFile)
      } else {
        await bulkApi.importInternships(selectedFile)
      }
      toast.success('Import completed successfully')
      setSelectedFile(null)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Import failed')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async () => {
    try {
      setLoading(true)
      let response
      if (activeTab === 'jobs') {
        response = await bulkApi.exportJobs()
      } else {
        response = await bulkApi.exportInternships()
      }
      
      // Create download link
      const blob = new Blob([response.data], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${activeTab}_export_${Date.now()}.csv`
      a.click()
      toast.success('Export completed successfully')
    } catch (error: any) {
      toast.error('Export failed')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Bulk Operations</h1>

      {/* Tabs */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setActiveTab('jobs')}
          className={`px-6 py-2 rounded-lg font-medium ${
            activeTab === 'jobs'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Jobs
        </button>
        <button
          onClick={() => setActiveTab('internships')}
          className={`px-6 py-2 rounded-lg font-medium ${
            activeTab === 'internships'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Internships
        </button>
      </div>

      {/* Import/Export Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Import */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">⬇️ Import {activeTab}</h2>
          <p className="text-sm text-gray-600 mb-4">
            Upload a CSV file to bulk import {activeTab}. The CSV should have all required fields.
          </p>
          
          <div className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <input
                type="file"
                accept=".csv"
                onChange={handleFileSelect}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer text-blue-600 hover:underline"
              >
                {selectedFile ? selectedFile.name : 'Click to select CSV file'}
              </label>
            </div>

            <button
              onClick={handleImport}
              disabled={!selectedFile || loading}
              className="w-full bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Importing...' : `Import ${activeTab}`}
            </button>
          </div>
        </div>

        {/* Export */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">⬆️ Export {activeTab}</h2>
          <p className="text-sm text-gray-600 mb-4">
            Download all {activeTab} as a CSV file. You can edit and re-import the file.
          </p>
          
          <div className="space-y-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-800">
                The export will include all fields and can be used as a template for imports.
              </p>
            </div>

            <button
              onClick={handleExport}
              disabled={loading}
              className="w-full bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Exporting...' : `Export ${activeTab} to CSV`}
            </button>
          </div>
        </div>
      </div>

      {/* Bulk Actions */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Bulk Actions</h2>
        <p className="text-sm text-gray-600 mb-4">
          Perform actions on multiple {activeTab} at once. Select items from the list page to enable bulk actions.
        </p>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="p-4 border-2 border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 text-center">
            <div className="text-2xl mb-2">✅</div>
            <div className="text-sm font-medium">Activate Selected</div>
          </button>
          <button className="p-4 border-2 border-gray-300 rounded-lg hover:border-orange-500 hover:bg-orange-50 text-center">
            <div className="text-2xl mb-2">⏸️</div>
            <div className="text-sm font-medium">Deactivate Selected</div>
          </button>
          <button className="p-4 border-2 border-gray-300 rounded-lg hover:border-red-500 hover:bg-red-50 text-center">
            <div className="text-2xl mb-2">🗑️</div>
            <div className="text-sm font-medium">Delete Selected</div>
          </button>
          <button className="p-4 border-2 border-gray-300 rounded-lg hover:border-green-500 hover:bg-green-50 text-center">
            <div className="text-2xl mb-2">📝</div>
            <div className="text-sm font-medium">Edit Fields</div>
          </button>
        </div>
      </div>
    </div>
  )
}
