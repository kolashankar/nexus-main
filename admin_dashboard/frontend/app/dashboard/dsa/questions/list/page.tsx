'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { dsaApi } from '@/lib/api/client/config/interceptors/auth/token/dsaApi'
import toast from 'react-hot-toast'

export default function DSAQuestionsList() {
  const [questions, setQuestions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [difficultyFilter, setDifficultyFilter] = useState('')

  useEffect(() => {
    fetchQuestions()
  }, [searchTerm, difficultyFilter])

  const fetchQuestions = async () => {
    try {
      setLoading(true)
      const params: any = {}
      if (searchTerm) params.search = searchTerm
      if (difficultyFilter) params.difficulty = difficultyFilter
      
      const response = await dsaApi.questions.getAll(params)
      setQuestions(response.data.questions || [])
    } catch (error: any) {
      toast.error('Failed to fetch questions')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this question?')) return
    
    try {
      await dsaApi.questions.delete(id)
      toast.success('Question deleted successfully')
      fetchQuestions()
    } catch (error: any) {
      toast.error('Failed to delete question')
      console.error(error)
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'hard': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">DSA Questions</h1>
        <div className="flex gap-2">
          <Link
            href="/dashboard/dsa/questions/create"
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Create Question
          </Link>
          <Link
            href="/dashboard/dsa/questions/create-ai"
            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700"
          >
            Generate with AI
          </Link>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Search questions..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 border rounded-lg"
          />
          <select
            value={difficultyFilter}
            onChange={(e) => setDifficultyFilter(e.target.value)}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">Loading...</div>
      ) : questions.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No questions found</div>
      ) : (
        <div className="grid gap-4">
          {questions.map((question) => (
            <div key={question._id} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-bold">{question.title}</h3>
                    <span className={`px-2 py-1 rounded text-xs ${getDifficultyColor(question.difficulty)}`}>
                      {question.difficulty}
                    </span>
                  </div>
                  <p className="text-gray-600 mb-3 line-clamp-2">{question.description}</p>
                  <div className="flex gap-4 text-sm text-gray-500">
                    <span>Topics: {question.topics?.length || 0}</span>
                    <span>Companies: {question.companies?.length || 0}</span>
                    <span>Solutions: {question.code_solutions?.length || 0}</span>
                  </div>
                </div>
                <div className="flex flex-col gap-2 ml-4">
                  <Link
                    href={`/dashboard/dsa/questions/edit/${question._id}`}
                    className="text-blue-600 hover:underline text-sm"
                  >
                    Edit
                  </Link>
                  <button
                    onClick={() => handleDelete(question._id)}
                    className="text-red-600 hover:underline text-sm"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
