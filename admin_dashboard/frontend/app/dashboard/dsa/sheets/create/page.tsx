'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { dsaApi } from '@/lib/api/client/config/interceptors/auth/token/dsaApi'
import toast from 'react-hot-toast'

export default function CreateDSASheet() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [questions, setQuestions] = useState<any[]>([])
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    author: '',
    level: 'beginner',
    tags: '',
    questions: [] as string[],
    is_published: false,
  })

  useEffect(() => {
    fetchQuestions()
  }, [])

  const fetchQuestions = async () => {
    try {
      const response = await dsaApi.questions.getAll({})
      setQuestions(response.data.questions || [])
    } catch (error: any) {
      console.error('Error fetching questions:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const payload = {
        ...formData,
        tags: formData.tags.split(',').map(t => t.trim()).filter(t => t),
      }
      await dsaApi.sheets.create(payload)
      toast.success('Sheet created successfully!')
      router.push('/dashboard/dsa/sheets/list')
    } catch (error: any) {
      console.error('Error creating sheet:', error)
      toast.error(error.response?.data?.detail || 'Failed to create sheet')
    } finally {
      setLoading(false)
    }
  }

  const handleQuestionToggle = (questionId: string) => {
    setFormData((prev) => {
      const questions = prev.questions.includes(questionId)
        ? prev.questions.filter((id) => id !== questionId)
        : [...prev.questions, questionId]
      return { ...prev, questions }
    })
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Create DSA Sheet</h1>
        <p className="text-gray-600">Create a new curated problem sheet</p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
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
              placeholder="e.g., Striver's SDE Sheet, LeetCode Top 100"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description *
            </label>
            <textarea
              required
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Brief description of this sheet and its purpose"
              rows={4}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Author */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Author *
            </label>
            <input
              type="text"
              required
              value={formData.author}
              onChange={(e) => setFormData({ ...formData, author: e.target.value })}
              placeholder="Author name"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Level */}
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
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tags (comma separated)
            </label>
            <input
              type="text"
              value={formData.tags}
              onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
              placeholder="e.g., arrays, strings, dynamic-programming"
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Questions Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Questions ({formData.questions.length} selected)
            </label>
            <div className="border rounded-lg p-4 max-h-96 overflow-y-auto space-y-2">
              {questions.length === 0 ? (
                <p className="text-gray-500 text-center py-4">No questions available</p>
              ) : (
                questions.map((question) => (
                  <label key={question._id} className="flex items-center p-3 border rounded hover:bg-gray-50 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.questions.includes(question._id)}
                      onChange={() => handleQuestionToggle(question._id)}
                      className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                    />
                    <span className="ml-3 flex-1">
                      <span className="font-medium">{question.title}</span>
                      <span className={`ml-2 text-xs px-2 py-1 rounded ${question.difficulty === 'Easy' ? 'bg-green-100 text-green-800' : question.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'}`}>
                        {question.difficulty}
                      </span>
                    </span>
                  </label>
                ))
              )}
            </div>
          </div>

          {/* Published Status */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="is_published"
              checked={formData.is_published}
              onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
              className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
            />
            <label htmlFor="is_published" className="ml-2 text-sm font-medium text-gray-700">
              Publish immediately
            </label>
          </div>

          {/* Submit Buttons */}
          <div className="flex gap-4 pt-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400 font-semibold"
            >
              {loading ? 'Creating...' : 'Create Sheet'}
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
