'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { roadmapsApi } from '@/lib/api/client/config/interceptors/auth/token/roadmapsApi'
import DashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/DashboardLayout'

export default function RoadmapCreateAIPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    category: '',
    level: 'Beginner',
    focus_areas: [''],
    estimated_duration: '3 months',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const dataToSubmit = {
        title: formData.title,
        category: formData.category,
        subcategory: formData.category, // Using category as subcategory for simplicity
        difficulty_level: formData.level.toLowerCase(),
        estimated_duration: formData.estimated_duration,
        focus_areas: formData.focus_areas.filter(area => area.trim() !== ''),
      }

      const response = await roadmapsApi.generateAI(dataToSubmit)
      alert('Roadmap with flowchart generated successfully with AI! 🎉')
      
      // Redirect to edit page if we have the ID, otherwise to list
      if (response.data._id) {
        router.push(`/dashboard/roadmaps/edit/${response.data._id}`)
      } else {
        router.push('/dashboard/roadmaps/list')
      }
    } catch (error: any) {
      console.error('Error generating roadmap:', error)
      alert(error.response?.data?.detail || 'Failed to generate roadmap with AI')
    } finally {
      setLoading(false)
    }
  }

  const addFocusArea = () => {
    setFormData({ ...formData, focus_areas: [...formData.focus_areas, ''] })
  }

  const removeFocusArea = (index: number) => {
    const newFocusAreas = formData.focus_areas.filter((_, i) => i !== index)
    setFormData({ ...formData, focus_areas: newFocusAreas })
  }

  const updateFocusArea = (index: number, value: string) => {
    const newFocusAreas = [...formData.focus_areas]
    newFocusAreas[index] = value
    setFormData({ ...formData, focus_areas: newFocusAreas })
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Generate Roadmap with AI</h1>
          <p className="text-gray-600 mt-1">Let AI create a comprehensive learning roadmap</p>
        </div>

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
              placeholder="e.g., Full Stack Web Development Roadmap"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

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
              <option value="">Select Category</option>
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

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Estimated Duration
            </label>
            <input
              type="text"
              value={formData.estimated_duration}
              onChange={(e) => setFormData({ ...formData, estimated_duration: e.target.value })}
              placeholder="e.g., 3 months, 6 months"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Focus Areas (Optional)
            </label>
            {formData.focus_areas.map((area, index) => (
              <div key={index} className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={area}
                  onChange={(e) => updateFocusArea(index, e.target.value)}
                  placeholder="e.g., React, Node.js, Database Design"
                  className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <button
                  type="button"
                  onClick={() => removeFocusArea(index)}
                  className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
                >
                  Remove
                </button>
              </div>
            ))}
            <button
              type="button"
              onClick={addFocusArea}
              className="mt-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              + Add Focus Area
            </button>
          </div>

          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-blue-800">
              ✨ AI will generate a comprehensive roadmap with 15-25 interconnected nodes including topics, resources, and learning paths. 
              The flowchart will automatically include node connections, positions, and different node types (content, roadmap links, article links).
            </p>
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition disabled:bg-gray-400"
            >
              {loading ? 'Generating with AI...' : '✨ Generate Roadmap'}
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
      </div>
    </DashboardLayout>
  )
}
