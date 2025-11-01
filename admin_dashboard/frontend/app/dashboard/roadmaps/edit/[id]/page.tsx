'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { roadmapsApi, type Roadmap, type RoadmapNode } from '@/lib/api/client/config/interceptors/auth/token/roadmapsApi'
import DashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/DashboardLayout'
import dynamic from 'next/dynamic'

const FlowchartEditor = dynamic(() => import('@/components/roadmaps/FlowchartEditor'), { ssr: false })

export default function RoadmapEditPage() {
  const router = useRouter()
  const params = useParams()
  const id = params.id as string
  
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null)
  const [nodes, setNodes] = useState<RoadmapNode[]>([])
  const [tab, setTab] = useState<'info' | 'flowchart'>('info')
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    level: 'Beginner',
    author: '',
    tags: [''],
    estimated_duration: '',
    is_published: false,
  })

  useEffect(() => {
    fetchRoadmap()
  }, [id])

  const fetchRoadmap = async () => {
    try {
      const response = await roadmapsApi.getById(id)
      setRoadmap(response.roadmap)
      setNodes(response.roadmap.nodes || [])
      setFormData({
        title: response.roadmap.title,
        description: response.roadmap.description,
        category: response.roadmap.category,
        level: response.roadmap.level,
        author: response.roadmap.author,
        tags: response.roadmap.tags.length > 0 ? response.roadmap.tags : [''],
        estimated_duration: response.roadmap.estimated_duration,
        is_published: response.roadmap.is_published,
      })
    } catch (error) {
      console.error('Error fetching roadmap:', error)
      alert('Failed to fetch roadmap')
    } finally {
      setLoading(false)
    }
  }

  const handleFlowchartSave = (updatedNodes: RoadmapNode[]) => {
    setNodes(updatedNodes)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)

    try {
      const dataToSubmit = {
        ...formData,
        tags: formData.tags.filter(tag => tag.trim() !== ''),
        nodes: nodes,
      }

      await roadmapsApi.update(id, dataToSubmit)
      alert('Roadmap updated successfully!')
      router.push('/dashboard/roadmaps/list')
    } catch (error: any) {
      console.error('Error updating roadmap:', error)
      alert(error.response?.data?.detail || 'Failed to update roadmap')
    } finally {
      setSaving(false)
    }
  }

  const addTag = () => {
    setFormData({ ...formData, tags: [...formData.tags, ''] })
  }

  const removeTag = (index: number) => {
    const newTags = formData.tags.filter((_, i) => i !== index)
    setFormData({ ...formData, tags: newTags })
  }

  const updateTag = (index: number, value: string) => {
    const newTags = [...formData.tags]
    newTags[index] = value
    setFormData({ ...formData, tags: newTags })
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="text-center py-8">Loading...</div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="max-w-6xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Edit Roadmap</h1>
          <p className="text-gray-600 mt-1">Update roadmap details and manage flowchart</p>
        </div>

        {/* Tabs */}
        <div className="mb-6 border-b">
          <div className="flex gap-4">
            <button
              onClick={() => setTab('info')}
              className={`px-4 py-2 font-medium border-b-2 transition ${
                tab === 'info'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Basic Information
            </button>
            <button
              onClick={() => setTab('flowchart')}
              className={`px-4 py-2 font-medium border-b-2 transition ${
                tab === 'flowchart'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Flowchart Editor ({nodes.length} nodes)
            </button>
          </div>
        </div>

        {/* Basic Info Tab */}
        {tab === 'info' && (
          <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Roadmap Title *
              </label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description *
              </label>
              <textarea
                required
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows={4}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category *
                </label>
                <select
                  required
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Web Development">Web Development</option>
                  <option value="Mobile Development">Mobile Development</option>
                  <option value="Data Science">Data Science</option>
                  <option value="Machine Learning">Machine Learning</option>
                  <option value="DevOps">DevOps</option>
                  <option value="Blockchain">Blockchain</option>
                  <option value="Cybersecurity">Cybersecurity</option>
                  <option value="Cloud Computing">Cloud Computing</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Level *
                </label>
                <select
                  required
                  value={formData.level}
                  onChange={(e) => setFormData({ ...formData, level: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Beginner">Beginner</option>
                  <option value="Intermediate">Intermediate</option>
                  <option value="Advanced">Advanced</option>
                  <option value="Expert">Expert</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Author *
                </label>
                <input
                  type="text"
                  required
                  value={formData.author}
                  onChange={(e) => setFormData({ ...formData, author: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Estimated Duration *
                </label>
                <input
                  type="text"
                  required
                  value={formData.estimated_duration}
                  onChange={(e) => setFormData({ ...formData, estimated_duration: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tags
              </label>
              {formData.tags.map((tag, index) => (
                <div key={index} className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={tag}
                    onChange={(e) => updateTag(index, e.target.value)}
                    className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                  <button
                    type="button"
                    onClick={() => removeTag(index)}
                    className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
                  >
                    Remove
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={addTag}
                className="mt-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
              >
                + Add Tag
              </button>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="is_published"
                checked={formData.is_published}
                onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
                className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
              />
              <label htmlFor="is_published" className="ml-2 text-sm text-gray-700">
                Published
              </label>
            </div>

            <div className="flex gap-4">
              <button
                type="submit"
                disabled={saving}
                className="flex-1 bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition disabled:bg-gray-400"
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                type="button"
                onClick={() => router.push('/dashboard/roadmaps/list')}
                className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        {/* Flowchart Tab */}
        {tab === 'flowchart' && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="mb-4">
                <h2 className="text-xl font-bold text-gray-900 mb-2">Edit Roadmap Flowchart</h2>
                <p className="text-gray-600 text-sm">
                  Drag nodes to reposition, click to edit, connect them to update learning paths.
                  Don't forget to click "Save Changes" in the editor!
                </p>
              </div>
              
              <FlowchartEditor
                initialNodes={nodes}
                onSave={handleFlowchartSave}
              />

              <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm text-blue-800">
                  <strong>💡 Tips:</strong>
                  <ul className="list-disc list-inside mt-2 space-y-1">
                    <li>Nodes are automatically positioned based on AI generation or your manual placement</li>
                    <li>Edit nodes by clicking them and then clicking "Edit Node"</li>
                    <li>Connect nodes by dragging from one node's edge to another</li>
                    <li>Delete unwanted nodes by selecting and clicking "Delete Node"</li>
                    <li>Click "Save Changes" in the editor panel to update the flowchart</li>
                    <li>Finally, click "Save All Changes" below to persist everything to the database</li>
                  </ul>
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <button
                onClick={handleSubmit}
                disabled={saving}
                className="flex-1 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition disabled:bg-gray-400"
              >
                {saving ? 'Saving All Changes...' : '✓ Save All Changes'}
              </button>
              <button
                type="button"
                onClick={() => router.push('/dashboard/roadmaps/list')}
                className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
