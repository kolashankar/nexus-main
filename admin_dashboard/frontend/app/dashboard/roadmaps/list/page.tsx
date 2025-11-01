'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { roadmapsApi, type Roadmap } from '@/lib/api/client/config/interceptors/auth/token/roadmapsApi'
import DashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/DashboardLayout'

export default function RoadmapsListPage() {
  const [roadmaps, setRoadmaps] = useState<Roadmap[]>([])
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [level, setLevel] = useState('')

  const fetchRoadmaps = async () => {
    try {
      setLoading(true)
      const response = await roadmapsApi.getAll({
        search: search || undefined,
        category: category || undefined,
        level: level || undefined,
      })
      setRoadmaps(response.roadmaps)
      setTotal(response.total)
    } catch (error) {
      console.error('Error fetching roadmaps:', error)
      alert('Failed to fetch roadmaps')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchRoadmaps()
  }, [search, category, level])

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this roadmap?')) return

    try {
      await roadmapsApi.delete(id)
      alert('Roadmap deleted successfully')
      fetchRoadmaps()
    } catch (error) {
      console.error('Error deleting roadmap:', error)
      alert('Failed to delete roadmap')
    }
  }

  const handleTogglePublish = async (roadmap: Roadmap) => {
    try {
      await roadmapsApi.togglePublish(roadmap._id!)
      fetchRoadmaps()
    } catch (error) {
      console.error('Error updating roadmap:', error)
      alert('Failed to update roadmap')
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Roadmaps Management</h1>
            <p className="text-gray-600 mt-1">Total: {total} roadmaps</p>
          </div>
          <div className="flex space-x-3">
            <Link
              href="/dashboard/roadmaps/create"
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
            >
              + Create Roadmap
            </Link>
            <Link
              href="/dashboard/roadmaps/create-ai"
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition"
            >
              ✨ Generate with AI
            </Link>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input
              type="text"
              placeholder="Search roadmaps..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Categories</option>
              <option value="Web Development">Web Development</option>
              <option value="Mobile Development">Mobile Development</option>
              <option value="Data Science">Data Science</option>
              <option value="Machine Learning">Machine Learning</option>
              <option value="DevOps">DevOps</option>
              <option value="Blockchain">Blockchain</option>
              <option value="Cybersecurity">Cybersecurity</option>
              <option value="Cloud Computing">Cloud Computing</option>
            </select>
            <select
              value={level}
              onChange={(e) => setLevel(e.target.value)}
              className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Levels</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
              <option value="Expert">Expert</option>
            </select>
          </div>
        </div>

        {/* Roadmaps List */}
        {loading ? (
          <div className="text-center py-8">Loading...</div>
        ) : roadmaps.length === 0 ? (
          <div className="bg-white p-8 rounded-lg shadow text-center">
            <p className="text-gray-500">No roadmaps found</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {roadmaps.map((roadmap) => (
              <div key={roadmap._id} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-semibold text-gray-900">{roadmap.title}</h3>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        roadmap.level === 'Beginner' ? 'bg-green-100 text-green-800' :
                        roadmap.level === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                        roadmap.level === 'Advanced' ? 'bg-orange-100 text-orange-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {roadmap.level}
                      </span>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        roadmap.is_published ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {roadmap.is_published ? 'Published' : 'Draft'}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-3">{roadmap.description}</p>
                    <div className="flex flex-wrap gap-2 mb-3">
                      <span className="text-sm text-gray-500">📁 {roadmap.category}</span>
                      <span className="text-sm text-gray-500">⏱️ {roadmap.estimated_duration}</span>
                      <span className="text-sm text-gray-500">🎯 {roadmap.nodes.length} nodes</span>
                      <span className="text-sm text-gray-500">👁️ {roadmap.views_count || 0} views</span>
                    </div>
                    {roadmap.tags && roadmap.tags.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {roadmap.tags.map((tag, idx) => (
                          <span key={idx} className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded">
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                  <div className="flex flex-col gap-2 ml-4">
                    <Link
                      href={`/dashboard/roadmaps/edit/${roadmap._id}`}
                      className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition text-center"
                    >
                      Edit
                    </Link>
                    <button
                      onClick={() => handleTogglePublish(roadmap)}
                      className={`px-4 py-2 rounded transition text-white ${
                        roadmap.is_published ? 'bg-gray-500 hover:bg-gray-600' : 'bg-green-500 hover:bg-green-600'
                      }`}
                    >
                      {roadmap.is_published ? 'Unpublish' : 'Publish'}
                    </button>
                    <button
                      onClick={() => handleDelete(roadmap._id!)}
                      className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
