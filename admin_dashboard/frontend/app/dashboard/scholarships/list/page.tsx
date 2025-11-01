'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import { Plus, Search, Edit, Trash2, Award } from 'lucide-react'

interface Scholarship {
  _id: string
  title: string
  organization: string
  amount: number
  currency: string
  deadline: string
  is_active: boolean
}

export default function ScholarshipsListPage() {
  const [scholarships, setScholarships] = useState<Scholarship[]>([])
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')

  const fetchScholarships = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (search) params.append('search', search)
      
      const response = await fetch(`/api/admin/scholarships?${params}`)
      const data = await response.json()
      setScholarships(data.scholarships || data.items || [])
      setTotal(data.total || 0)
    } catch (error) {
      console.error('Error fetching scholarships:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchScholarships()
  }, [search])

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this scholarship?')) return

    try {
      await fetch(`/api/admin/scholarships/${id}`, { method: 'DELETE' })
      alert('Scholarship deleted successfully')
      fetchScholarships()
    } catch (error) {
      console.error('Error deleting scholarship:', error)
      alert('Failed to delete scholarship')
    }
  }

  const handleToggleActive = async (scholarship: Scholarship) => {
    try {
      await fetch(`/api/admin/scholarships/${scholarship._id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...scholarship, is_active: !scholarship.is_active }),
      })
      fetchScholarships()
    } catch (error) {
      console.error('Error updating scholarship:', error)
      alert('Failed to update scholarship')
    }
  }

  return (
    <ModernDashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-gradient-to-br from-orange-500 to-amber-600 rounded-xl shadow-lg">
              <Award className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900">Scholarships Management</h1>
              <p className="text-slate-600 mt-1">Total: {total} scholarships</p>
            </div>
          </div>
          <Link href="/dashboard/scholarships/create">
            <button className="px-6 py-3 bg-gradient-to-r from-orange-600 to-amber-600 text-white rounded-lg hover:from-orange-700 hover:to-amber-700 shadow-lg shadow-orange-500/50 transition-all font-medium flex items-center">
              <Plus className="w-5 h-5 mr-2" />
              Create Scholarship
            </button>
          </Link>
        </div>

        <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search scholarships..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-11 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
            />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden">
          {loading ? (
            <div className="p-12 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto"></div>
              <p className="mt-4 text-slate-600">Loading scholarships...</p>
            </div>
          ) : scholarships.length === 0 ? (
            <div className="p-12 text-center">
              <Award className="w-16 h-16 text-slate-300 mx-auto mb-4" />
              <p className="text-slate-500 text-lg">No scholarships found</p>
              <Link href="/dashboard/scholarships/create">
                <button className="mt-4 px-6 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-all">
                  Create Your First Scholarship
                </button>
              </Link>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Title</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Organization</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Amount</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Deadline</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-4 text-right text-xs font-semibold text-slate-700 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-slate-200">
                  {scholarships.map((scholarship) => (
                    <tr key={scholarship._id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4">
                        <div className="text-sm font-semibold text-slate-900">{scholarship.title}</div>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-900">{scholarship.organization}</td>
                      <td className="px-6 py-4 text-sm text-slate-900">
                        {scholarship.currency} {scholarship.amount}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {scholarship.deadline ? new Date(scholarship.deadline).toLocaleDateString() : 'N/A'}
                      </td>
                      <td className="px-6 py-4">
                        <button
                          onClick={() => handleToggleActive(scholarship)}
                          className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full transition-all ${
                            scholarship.is_active
                              ? 'bg-green-100 text-green-800 hover:bg-green-200'
                              : 'bg-red-100 text-red-800 hover:bg-red-200'
                          }`}
                        >
                          {scholarship.is_active ? 'Active' : 'Inactive'}
                        </button>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex justify-end space-x-2">
                          <Link href={`/dashboard/scholarships/edit/${scholarship._id}`}>
                            <button className="p-2 text-orange-600 hover:bg-orange-50 rounded-lg transition-colors">
                              <Edit className="w-4 h-4" />
                            </button>
                          </Link>
                          <button
                            onClick={() => handleDelete(scholarship._id)}
                            className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </ModernDashboardLayout>
  )
}
