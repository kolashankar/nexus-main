'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import { Plus, Search, Edit, Trash2, GraduationCap, Sparkles } from 'lucide-react'

interface Internship {
  _id: string
  title: string
  company: string
  location: string
  duration: string
  stipend: number
  currency: string
  category: string
  is_active: boolean
}

export default function InternshipsListPage() {
  const [internships, setInternships] = useState<Internship[]>([])
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')

  const fetchInternships = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (search) params.append('search', search)
      if (category) params.append('category', category)
      
      const response = await fetch(`/api/admin/internships?${params}`)
      const data = await response.json()
      setInternships(data.internships || data.items || [])
      setTotal(data.total || 0)
    } catch (error) {
      console.error('Error fetching internships:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchInternships()
  }, [search, category])

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this internship?')) return

    try {
      await fetch(`/api/admin/internships/${id}`, { method: 'DELETE' })
      alert('Internship deleted successfully')
      fetchInternships()
    } catch (error) {
      console.error('Error deleting internship:', error)
      alert('Failed to delete internship')
    }
  }

  const handleToggleActive = async (internship: Internship) => {
    try {
      await fetch(`/api/admin/internships/${internship._id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...internship, is_active: !internship.is_active }),
      })
      fetchInternships()
    } catch (error) {
      console.error('Error updating internship:', error)
      alert('Failed to update internship')
    }
  }

  return (
    <ModernDashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl shadow-lg">
              <GraduationCap className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900">Internships Management</h1>
              <p className="text-slate-600 mt-1">Total: {total} internships</p>
            </div>
          </div>
          <div className="flex space-x-3">
            <Link href="/dashboard/internships/create">
              <button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 shadow-lg shadow-purple-500/50 transition-all font-medium flex items-center">
                <Plus className="w-5 h-5 mr-2" />
                Create Internship
              </button>
            </Link>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="text"
                placeholder="Search internships..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-11 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              />
            </div>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
            >
              <option value="">All Categories</option>
              <option value="Technology">Technology</option>
              <option value="Marketing">Marketing</option>
              <option value="Finance">Finance</option>
              <option value="Design">Design</option>
            </select>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden">
          {loading ? (
            <div className="p-12 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
              <p className="mt-4 text-slate-600">Loading internships...</p>
            </div>
          ) : internships.length === 0 ? (
            <div className="p-12 text-center">
              <GraduationCap className="w-16 h-16 text-slate-300 mx-auto mb-4" />
              <p className="text-slate-500 text-lg">No internships found</p>
              <Link href="/dashboard/internships/create">
                <button className="mt-4 px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-all">
                  Create Your First Internship
                </button>
              </Link>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Title</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Company</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Location</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Duration</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Stipend</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-4 text-right text-xs font-semibold text-slate-700 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-slate-200">
                  {internships.map((internship) => (
                    <tr key={internship._id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4">
                        <div className="text-sm font-semibold text-slate-900">{internship.title}</div>
                        <div className="text-xs text-slate-500">{internship.category}</div>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-900">{internship.company}</td>
                      <td className="px-6 py-4 text-sm text-slate-600">{internship.location}</td>
                      <td className="px-6 py-4 text-sm text-slate-600">{internship.duration}</td>
                      <td className="px-6 py-4 text-sm text-slate-900">
                        {internship.currency} {internship.stipend}
                      </td>
                      <td className="px-6 py-4">
                        <button
                          onClick={() => handleToggleActive(internship)}
                          className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full transition-all ${
                            internship.is_active
                              ? 'bg-green-100 text-green-800 hover:bg-green-200'
                              : 'bg-red-100 text-red-800 hover:bg-red-200'
                          }`}
                        >
                          {internship.is_active ? 'Active' : 'Inactive'}
                        </button>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex justify-end space-x-2">
                          <Link href={`/dashboard/internships/edit/${internship._id}`}>
                            <button className="p-2 text-purple-600 hover:bg-purple-50 rounded-lg transition-colors">
                              <Edit className="w-4 h-4" />
                            </button>
                          </Link>
                          <button
                            onClick={() => handleDelete(internship._id)}
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
