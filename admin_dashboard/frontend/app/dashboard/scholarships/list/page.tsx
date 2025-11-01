'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { scholarshipsApi, type Scholarship } from '@/lib/api/client/config/interceptors/auth/token/scholarshipsApi'
import DashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/DashboardLayout'

export default function ScholarshipsListPage() {
  const [scholarships, setScholarships] = useState<Scholarship[]>([])
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')
  const [scholarshipType, setScholarshipType] = useState('')
  const [educationLevel, setEducationLevel] = useState('')
  const [country, setCountry] = useState('')

  const fetchScholarships = async () => {
    try {
      setLoading(true)
      const response = await scholarshipsApi.getAll({
        search: search || undefined,
        scholarship_type: scholarshipType || undefined,
        education_level: educationLevel || undefined,
        country: country || undefined,
      })
      setScholarships(response.scholarships)
      setTotal(response.total)
    } catch (error) {
      console.error('Error fetching scholarships:', error)
      alert('Failed to fetch scholarships')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchScholarships()
  }, [search, scholarshipType, educationLevel, country])

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this scholarship?')) return

    try {
      await scholarshipsApi.delete(id)
      alert('Scholarship deleted successfully')
      fetchScholarships()
    } catch (error) {
      console.error('Error deleting scholarship:', error)
      alert('Failed to delete scholarship')
    }
  }

  const handleToggleActive = async (scholarship: Scholarship) => {
    try {
      await scholarshipsApi.update(scholarship._id!, { is_active: !scholarship.is_active })
      fetchScholarships()
    } catch (error) {
      console.error('Error updating scholarship:', error)
      alert('Failed to update scholarship')
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Scholarships Management</h1>
            <p className="text-gray-600 mt-1">Total: {total} scholarships</p>
          </div>
          <div className="flex space-x-3">
            <Link
              href="/dashboard/scholarships/create"
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
            >
              + Create Scholarship
            </Link>
            <Link
              href="/dashboard/scholarships/create-ai"
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition"
            >
              ✨ Generate with AI
            </Link>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <input
              type="text"
              placeholder="Search scholarships..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <select
              value={scholarshipType}
              onChange={(e) => setScholarshipType(e.target.value)}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Types</option>
              <option value="merit-based">Merit-based</option>
              <option value="need-based">Need-based</option>
              <option value="full-funding">Full Funding</option>
              <option value="partial-funding">Partial Funding</option>
            </select>
            <select
              value={educationLevel}
              onChange={(e) => setEducationLevel(e.target.value)}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Levels</option>
              <option value="undergraduate">Undergraduate</option>
              <option value="postgraduate">Postgraduate</option>
              <option value="doctorate">Doctorate</option>
            </select>
            <input
              type="text"
              placeholder="Country..."
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Scholarships Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          {loading ? (
            <div className="p-8 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading scholarships...</p>
            </div>
          ) : scholarships.length === 0 ? (
            <div className="p-8 text-center">
              <p className="text-gray-500">No scholarships found</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Title
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Provider
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Country
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Level
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {scholarships.map((scholarship) => (
                    <tr key={scholarship._id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{scholarship.title}</div>
                        <div className="text-sm text-gray-500">{scholarship.scholarship_type}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{scholarship.provider}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{scholarship.country}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">
                          {scholarship.education_level}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button
                          onClick={() => handleToggleActive(scholarship)}
                          className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            scholarship.is_active
                              ? 'bg-green-100 text-green-800'
                              : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {scholarship.is_active ? 'Active' : 'Inactive'}
                        </button>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                        <Link
                          href={`/dashboard/scholarships/edit/${scholarship._id}`}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          Edit
                        </Link>
                        <button
                          onClick={() => handleDelete(scholarship._id!)}
                          className="text-red-600 hover:text-red-900"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  )
}
