'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { articlesApi } from '@/lib/api/client/config/interceptors/auth/token/articlesApi'
import toast from 'react-hot-toast'

export default function CreateArticleAI() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    topic: '',
    category: '',
    author: '',
    tone: 'professional',
    length: 'medium',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await articlesApi.generateAI(formData)
      toast.success('Article generated successfully')
      
      // Redirect to edit page with generated article
      if (response.data._id) {
        router.push(`/dashboard/learning/articles/edit/${response.data._id}`)
      } else {
        router.push('/dashboard/learning/articles/list')
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to generate article')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Generate Article with AI</h1>

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Topic *</label>
            <input
              type="text"
              required
              value={formData.topic}
              onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
              placeholder="e.g. How to ace technical interviews"
              className="w-full px-4 py-2 border rounded-lg"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Category *</label>
            <select
              required
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="">Select Category</option>
              <option value="Career Guidance">Career Guidance</option>
              <option value="Interview Tips">Interview Tips</option>
              <option value="Technology">Technology</option>
              <option value="Skill Development">Skill Development</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Author *</label>
            <input
              type="text"
              required
              value={formData.author}
              onChange={(e) => setFormData({ ...formData, author: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Tone</label>
            <select
              value={formData.tone}
              onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="professional">Professional</option>
              <option value="casual">Casual</option>
              <option value="formal">Formal</option>
              <option value="friendly">Friendly</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Length</label>
            <select
              value={formData.length}
              onChange={(e) => setFormData({ ...formData, length: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="short">Short (500-800 words)</option>
              <option value="medium">Medium (1000-1500 words)</option>
              <option value="long">Long (2000-3000 words)</option>
            </select>
          </div>

          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>AI Generation:</strong> The AI will create a comprehensive article based on your inputs, including proper formatting, headings, and structure.
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
