'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import dynamic from 'next/dynamic'
import { dsaApi } from '@/lib/api/client/config/interceptors/auth/token/dsaApi'
import toast from 'react-hot-toast'

const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false })

export default function CreateQuestion() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    difficulty: 'Medium',
    topics: '',
    companies: '',
    solution_approach: '',
    hints: '',
    time_complexity: '',
    space_complexity: '',
  })

  const [codeSolutions, setCodeSolutions] = useState([
    { language: 'Python', code: '# Your Python solution here' },
    { language: 'JavaScript', code: '// Your JavaScript solution here' },
  ])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const payload = {
        ...formData,
        topics: formData.topics.split(',').map(t => t.trim()).filter(t => t),
        companies: formData.companies.split(',').map(c => c.trim()).filter(c => c),
        hints: formData.hints.split('\n').filter(h => h.trim()),
        code_solutions: codeSolutions,
        complexity_analysis: {
          time: formData.time_complexity,
          space: formData.space_complexity,
        },
      }
      
      await dsaApi.questions.create(payload)
      toast.success('Question created successfully')
      router.push('/dashboard/dsa/questions/list')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create question')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const addCodeSolution = () => {
    setCodeSolutions([...codeSolutions, { language: 'C++', code: '// Your C++ solution here' }])
  }

  const updateCodeSolution = (index: number, field: 'language' | 'code', value: string) => {
    const updated = [...codeSolutions]
    updated[index][field] = value
    setCodeSolutions(updated)
  }

  const removeCodeSolution = (index: number) => {
    setCodeSolutions(codeSolutions.filter((_, i) => i !== index))
  }

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Create DSA Question</h1>

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow space-y-6">
        <div>
          <label className="block text-sm font-medium mb-2">Title *</label>
          <input
            type="text"
            required
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Description *</label>
          <textarea
            required
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg"
            rows={5}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
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
            <label className="block text-sm font-medium mb-2">Topics (comma separated)</label>
            <input
              type="text"
              value={formData.topics}
              onChange={(e) => setFormData({ ...formData, topics: e.target.value })}
              placeholder="e.g. Arrays, Sorting"
              className="w-full px-4 py-2 border rounded-lg"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Companies (comma separated)</label>
            <input
              type="text"
              value={formData.companies}
              onChange={(e) => setFormData({ ...formData, companies: e.target.value })}
              placeholder="e.g. Google, Amazon"
              className="w-full px-4 py-2 border rounded-lg"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Solution Approach</label>
          <textarea
            value={formData.solution_approach}
            onChange={(e) => setFormData({ ...formData, solution_approach: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg"
            rows={4}
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Hints (one per line)</label>
          <textarea
            value={formData.hints}
            onChange={(e) => setFormData({ ...formData, hints: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg"
            rows={3}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Time Complexity</label>
            <input
              type="text"
              value={formData.time_complexity}
              onChange={(e) => setFormData({ ...formData, time_complexity: e.target.value })}
              placeholder="e.g. O(n log n)"
              className="w-full px-4 py-2 border rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Space Complexity</label>
            <input
              type="text"
              value={formData.space_complexity}
              onChange={(e) => setFormData({ ...formData, space_complexity: e.target.value })}
              placeholder="e.g. O(n)"
              className="w-full px-4 py-2 border rounded-lg"
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between items-center mb-4">
            <label className="block text-sm font-medium">Code Solutions *</label>
            <button
              type="button"
              onClick={addCodeSolution}
              className="text-blue-600 hover:underline text-sm"
            >
              + Add Solution
            </button>
          </div>
          
          {codeSolutions.map((solution, index) => (
            <div key={index} className="mb-4 p-4 border rounded-lg">
              <div className="flex justify-between items-center mb-2">
                <input
                  type="text"
                  value={solution.language}
                  onChange={(e) => updateCodeSolution(index, 'language', e.target.value)}
                  className="px-3 py-1 border rounded"
                />
                {codeSolutions.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeCodeSolution(index)}
                    className="text-red-600 hover:underline text-sm"
                  >
                    Remove
                  </button>
                )}
              </div>
              <MonacoEditor
                height="200px"
                language={solution.language.toLowerCase()}
                value={solution.code}
                onChange={(value) => updateCodeSolution(index, 'code', value || '')}
                theme="vs-dark"
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                }}
              />
            </div>
          ))}
        </div>

        <div className="flex gap-4 pt-4">
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Creating...' : 'Create Question'}
          </button>
          <button
            type="button"
            onClick={() => router.back()}
            className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}
