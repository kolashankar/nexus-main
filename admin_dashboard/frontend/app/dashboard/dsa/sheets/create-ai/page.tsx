'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { dsaApi } from '@/lib/api/client/config/interceptors/auth/token/dsaApi'
import toast from 'react-hot-toast'

export default function CreateDSASheetAI() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    level: 'beginner',
    focus_topics: '',
    author: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const payload = {
        ...formData,
        focus_topics: formData.focus_topics.split(',').map(t => t.trim()).filter(t => t),
      }
      await dsaApi.sheets.generateAI(payload)
      toast.success('Sheet generated successfully with AI!')
      router.push('/dashboard/dsa/sheets/list')
    } catch (error: any) {
      console.error('Error generating sheet:', error)
      toast.error(error.response?.data?.detail || 'Failed to generate sheet')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">🤖 Generate DSA Sheet with AI</h1>
        <p className="text-gray-600">Let AI create a comprehensive problem sheet for you</p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-purple-900 mb-2">✨ AI-Powered Generation</h3>
          <p className="text-sm text-purple-800">
            Our AI will automatically create a comprehensive DSA sheet with 20-30 carefully selected problems,
            organized by topic and difficulty level, complete with descriptions and problem recommendations.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Sheet Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Sheet Name *
            </label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g., Complete SDE Preparation, Dynamic Programming Mastery"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500"
            />
          </div>

          {/* Level */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty Level *
            </label>
            <select
              required
              value={formData.level}
              onChange={(e) => setFormData({ ...formData, level: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500"
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          {/* Focus Topics */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Focus Topics (comma separated)
            </label>
            <input
              type="text"
              value={formData.focus_topics}
              onChange={(e) => setFormData({ ...formData, focus_topics: e.target.value })}
              placeholder="e.g., arrays, strings, trees, graphs, dynamic-programming"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500"
            />
            <p className="text-xs text-gray-500 mt-1">Leave blank for AI to choose optimal topics</p>
          </div>

          {/* Author */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Author Name *
            </label>
            <input
              type="text"
              required
              value={formData.author}
              onChange={(e) => setFormData({ ...formData, author: e.target.value })}
              placeholder="Your name or organization"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500"
            />
          </div>

          {/* Submit Buttons */}
          <div className="flex gap-4 pt-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition disabled:bg-gray-400 font-semibold"
            >
              {loading ? '🤖 Generating with AI...' : '✨ Generate Sheet with AI'}
            </button>
            <button
              type="button"
              onClick={() => router.back()}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition font-semibold"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
