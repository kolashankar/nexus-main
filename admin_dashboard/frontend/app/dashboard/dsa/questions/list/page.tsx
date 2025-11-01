'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import { Plus, Search, Edit, Trash2, Code2 } from 'lucide-react'

interface DSAQuestion {
  _id: string
  title: string
  difficulty: string
  topic: string
  companies: string[]
  is_active: boolean
}

export default function DSAQuestionsListPage() {
  const [questions, setQuestions] = useState<DSAQuestion[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [difficulty, setDifficulty] = useState('')

  const fetchQuestions = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (search) params.append('search', search)
      if (difficulty) params.append('difficulty', difficulty)
      const response = await fetch(`/api/admin/dsa/questions?${params}`)
      const data = await response.json()
      setQuestions(data.questions || data.items || [])
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchQuestions() }, [search, difficulty])

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this question?')) return
    try {
      await fetch(`/api/admin/dsa/questions/${id}`, { method: 'DELETE' })
      alert('Question deleted')
      fetchQuestions()
    } catch (error) {
      alert('Failed to delete')
    }
  }

  return (
    <ModernDashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg">
              <Code2 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900">DSA Questions</h1>
              <p className="text-slate-600 mt-1">Manage coding problems</p>
            </div>
          </div>
          <Link href="/dashboard/dsa/questions/create">
            <button className="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-700 hover:to-emerald-700 shadow-lg shadow-green-500/50 transition-all font-medium flex items-center">
              <Plus className="w-5 h-5 mr-2" /> Create Question
            </button>
          </Link>
        </div>

        <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input type="text" placeholder="Search questions..." value={search} onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-11 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all" />
            </div>
            <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}
              className="px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 transition-all">
              <option value="">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden">
          {loading ? (
            <div className="p-12 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
              <p className="mt-4 text-slate-600">Loading...</p>
            </div>
          ) : questions.length === 0 ? (
            <div className="p-12 text-center">
              <Code2 className="w-16 h-16 text-slate-300 mx-auto mb-4" />
              <p className="text-slate-500 text-lg">No questions found</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase">Title</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase">Difficulty</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase">Topic</th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase">Companies</th>
                    <th className="px-6 py-4 text-right text-xs font-semibold text-slate-700 uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200">
                  {questions.map((q) => (
                    <tr key={q._id} className="hover:bg-slate-50">
                      <td className="px-6 py-4 text-sm font-semibold text-slate-900">{q.title}</td>
                      <td className="px-6 py-4">
                        <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                          q.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
                          q.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>{q.difficulty}</span>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">{q.topic}</td>
                      <td className="px-6 py-4 text-sm text-slate-600">{q.companies?.slice(0, 2).join(', ')}</td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex justify-end space-x-2">
                          <Link href={`/dashboard/dsa/questions/edit/${q._id}`}>
                            <button className="p-2 text-green-600 hover:bg-green-50 rounded-lg">
                              <Edit className="w-4 h-4" />
                            </button>
                          </Link>
                          <button onClick={() => handleDelete(q._id)} className="p-2 text-red-600 hover:bg-red-50 rounded-lg">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </ModernDashboardLayout>
  )
}
