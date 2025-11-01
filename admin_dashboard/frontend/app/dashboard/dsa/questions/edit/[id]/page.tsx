'use client'

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { dsaApi } from '@/lib/api/client/config/interceptors/auth/token/dsaApi'
import toast from 'react-hot-toast'
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false })

export default function EditDSAQuestion() {
  const router = useRouter()
  const params = useParams()
  const questionId = params.id as string
  const [loading, setLoading] = useState(false)
  const [fetching, setFetching] = useState(true)
  const [topics, setTopics] = useState<any[]>([])
  const [companies, setCompanies] = useState<any[]>([])
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    difficulty: 'Medium',
    topics: [] as string[],
    companies: [] as string[],
    examples: [{ input: '', output: '', explanation: '' }],
    constraints: '',
    hints: [''],
    solution_approach: '',
    code_solutions: [{ language: 'Python', code: '' }],
    time_complexity: '',
    space_complexity: '',
  })

  useEffect(() => {
    fetchQuestion()
    fetchTopics()
    fetchCompanies()
  }, [questionId])

  const fetchQuestion = async () => {
    try {
      setFetching(true)
      const response = await dsaApi.questions.getById(questionId)
      const q = response.data.question
      setFormData({
        title: q.title || '',
        description: q.description || '',
        difficulty: q.difficulty || 'Medium',
        topics: q.topics || [],
        companies: q.companies || [],
        examples: q.examples?.length > 0 ? q.examples : [{ input: '', output: '', explanation: '' }],
        constraints: q.constraints || '',
        hints: q.hints?.length > 0 ? q.hints : [''],
        solution_approach: q.solution_approach || '',
        code_solutions: q.code_solutions?.length > 0 ? q.code_solutions : [{ language: 'Python', code: '' }],
        time_complexity: q.time_complexity || '',
        space_complexity: q.space_complexity || '',
      })
    } catch (error: any) {
      console.error('Error fetching question:', error)
      toast.error('Failed to load question data')
    } finally {
      setFetching(false)
    }
  }

  const fetchTopics = async () => {
    try {
      const response = await dsaApi.topics.getAll()
      setTopics(response.data.topics || [])
    } catch (error: any) {
      console.error('Error fetching topics:', error)
    }
  }

  const fetchCompanies = async () => {
    try {
      const response = await dsaApi.companies.getAll()
      setCompanies(response.data.companies || [])
    } catch (error: any) {
      console.error('Error fetching companies:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await dsaApi.questions.update(questionId, formData)
      toast.success('Question updated successfully!')
      router.push('/dashboard/dsa/questions/list')
    } catch (error: any) {
      console.error('Error updating question:', error)
      toast.error(error.response?.data?.detail || 'Failed to update question')
    } finally {
      setLoading(false)
    }
  }

  if (fetching) {
    return (
      <div className="p-6">
        <div className="text-center py-12">Loading question data...</div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Edit DSA Question</h1>
        <p className="text-gray-600">Update question details</p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Question Title *</label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Description *</label>
            <textarea
              required
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={6}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Difficulty */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Difficulty *</label>
            <select
              required
              value={formData.difficulty}
              onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          {/* Topics */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Topics</label>
            <div className="border rounded-lg p-4 max-h-48 overflow-y-auto space-y-2">
              {topics.map((topic) => (
                <label key={topic._id} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.topics.includes(topic._id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setFormData({ ...formData, topics: [...formData.topics, topic._id] })
                      } else {
                        setFormData({ ...formData, topics: formData.topics.filter(t => t !== topic._id) })
                      }
                    }}
                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span className="ml-2">{topic.name}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Companies */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Companies</label>
            <div className="border rounded-lg p-4 max-h-48 overflow-y-auto space-y-2">
              {companies.map((company) => (
                <label key={company._id} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.companies.includes(company._id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setFormData({ ...formData, companies: [...formData.companies, company._id] })
                      } else {
                        setFormData({ ...formData, companies: formData.companies.filter(c => c !== company._id) })
                      }
                    }}
                    className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span className="ml-2">{company.name}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Code Solutions */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Code Solutions</label>
            {formData.code_solutions.map((solution, index) => (
              <div key={index} className="mb-4 border rounded-lg p-4">
                <div className="flex gap-4 mb-2">
                  <select
                    value={solution.language}
                    onChange={(e) => {
                      const newSolutions = [...formData.code_solutions]
                      newSolutions[index].language = e.target.value
                      setFormData({ ...formData, code_solutions: newSolutions })
                    }}
                    className="px-4 py-2 border rounded-lg"
                  >
                    <option value="Python">Python</option>
                    <option value="JavaScript">JavaScript</option>
                    <option value="Java">Java</option>
                    <option value="C++">C++</option>
                  </select>
                  {formData.code_solutions.length > 1 && (
                    <button
                      type="button"
                      onClick={() => {
                        setFormData({
                          ...formData,
                          code_solutions: formData.code_solutions.filter((_, i) => i !== index)
                        })
                      }}
                      className="px-4 py-2 bg-red-500 text-white rounded-lg"
                    >
                      Remove
                    </button>
                  )}
                </div>
                <MonacoEditor
                  height="300px"
                  language={solution.language.toLowerCase()}
                  value={solution.code}
                  onChange={(value) => {
                    const newSolutions = [...formData.code_solutions]
                    newSolutions[index].code = value || ''
                    setFormData({ ...formData, code_solutions: newSolutions })
                  }}
                  theme="vs-dark"
                  options={{
                    minimap: { enabled: false },
                    fontSize: 14,
                  }}
                />
              </div>
            ))}
            <button
              type="button"
              onClick={() => {
                setFormData({
                  ...formData,
                  code_solutions: [...formData.code_solutions, { language: 'Python', code: '' }]
                })
              }}
              className="mt-2 px-4 py-2 bg-green-500 text-white rounded-lg"
            >
              Add Solution
            </button>
          </div>

          {/* Submit Buttons */}
          <div className="flex gap-4 pt-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400 font-semibold"
            >
              {loading ? 'Updating...' : 'Update Question'}
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
