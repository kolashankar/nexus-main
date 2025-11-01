'use client'

import { useState, useEffect } from 'react'
import { contentManagementApi } from '@/lib/api/client/config/interceptors/auth/token/contentManagementApi'
import toast from 'react-hot-toast'

export default function TagsManagement() {
  const [tags, setTags] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [newTag, setNewTag] = useState('')

  useEffect(() => {
    fetchTags()
  }, [])

  const fetchTags = async () => {
    try {
      setLoading(true)
      const response = await contentManagementApi.tags.getAll()
      setTags(response.data.tags || [])
    } catch (error: any) {
      toast.error('Failed to fetch tags')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newTag.trim()) return

    try {
      await contentManagementApi.tags.create(newTag.trim())
      toast.success('Tag created successfully')
      setNewTag('')
      fetchTags()
    } catch (error: any) {
      toast.error('Failed to create tag')
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure?')) return
    try {
      await contentManagementApi.tags.delete(id)
      toast.success('Tag deleted')
      fetchTags()
    } catch (error: any) {
      toast.error('Failed to delete tag')
    }
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Tags Management</h1>

      {/* Create Tag Form */}
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <form onSubmit={handleCreate} className="flex gap-4">
          <input
            type="text"
            value={newTag}
            onChange={(e) => setNewTag(e.target.value)}
            placeholder="Enter tag name..."
            className="flex-1 px-4 py-2 border rounded-lg"
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Add Tag
          </button>
        </form>
      </div>

      {/* Tags List */}
      {loading ? (
        <div className="text-center py-12">Loading...</div>
      ) : tags.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No tags found</div>
      ) : (
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex flex-wrap gap-3">
            {tags.map((tag) => (
              <div
                key={tag._id}
                className="flex items-center gap-2 bg-blue-100 text-blue-800 px-4 py-2 rounded-full"
              >
                <span className="font-medium">{tag.name}</span>
                <span className="text-xs text-blue-600">({tag.count || 0})</span>
                <button
                  onClick={() => handleDelete(tag._id)}
                  className="text-red-600 hover:text-red-800 ml-2"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
