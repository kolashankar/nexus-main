'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { dsaApi } from '@/lib/api/client/config/interceptors/auth/token/dsaApi'
import toast from 'react-hot-toast'

export default function CreateQuestionAI() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    topic: '',
    difficulty: 'Medium',
    companies: '',
    focus_area: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await dsaApi.questions.generateAI(formData)
      toast.success('Question generated successfully')
      
      if (response.data._id) {
        router.push(`/dashboard/dsa/questions/edit/${response.data._id}`)
      } else {
        router.push('/dashboard/dsa/questions/list')
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to generate question')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Generate DSA Question with AI</h1>

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Topic *</label>
            <input
              type="text"
              required
              value={formData.topic}
              onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
              placeholder="e.g. Binary Search, Dynamic Programming"
              className="w-full px-4 py-2 border rounded-lg"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Difficulty *</label>
            <select
              required
              value={formData.difficulty}
              onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Companies (comma separated)</label>
            <input
              type="text"
              value={formData.companies}
              onChange={(e) => setFormData({ ...formData, companies: e.target.value })}
              placeholder="e.g. Google, Amazon, Microsoft"
              className="w-full px-4 py-2 border rounded-lg"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Focus Area (optional)</label>
            <textarea
              value={formData.focus_area}
              onChange={(e) => setFormData({ ...formData, focus_area: e.target.value })}
              placeholder="e.g. Focus on edge cases, optimization techniques"
              className="w-full px-4 py-2 border rounded-lg"
              rows={3}
            />
          </div>

          <div className="bg-purple-50 p-4 rounded-lg">
            <p className="text-sm text-purple-800">
              <strong>AI Generation:</strong> The AI will create a comprehensive DSA question including problem statement, solution approach, code in multiple languages, hints, and complexity analysis.
            </p>
          </div>

          <div className="flex gap-4 pt-4">
            <button
              type="submit"
              disabled={loading}
              className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 disabled:opacity-50 flex items-center gap-2"
            >
              {loading ? (
                <>
                  <span className="animate-spin">⚙️</span>
                  Generating...
                </>
              ) : (
                <>✨ Generate with AI</>
              )}
            </button>
            <button
              type="button"
              onClick={() => router.back()}
              className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400"
            >
              Cancel
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}
