'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { dsaApi } from '@/lib/api/client/config/interceptors/auth/token/dsaApi'
import toast from 'react-hot-toast'

export default function DSATopicsList() {
  const [topics, setTopics] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTopics()
  }, [])

  const fetchTopics = async () => {
    try {
      setLoading(true)
      const response = await dsaApi.topics.getAll()
      setTopics(response.data.topics || [])
    } catch (error: any) {
      toast.error('Failed to fetch topics')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this topic?')) return
    
    try {
      await dsaApi.topics.delete(id)
      toast.success('Topic deleted successfully')
      fetchTopics()
    } catch (error: any) {
      toast.error('Failed to delete topic')
      console.error(error)
    }
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">DSA Topics</h1>
        <Link
          href="/dashboard/dsa/topics/create"
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Create Topic
        </Link>
      </div>

      {loading ? (
        <div className="text-center py-12">Loading...</div>
      ) : topics.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No topics found</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {topics.map((topic) => (
            <div key={topic._id} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="flex items-start justify-between mb-4">
                <div className="text-4xl">{topic.icon}</div>
                <span 
                  className="w-4 h-4 rounded-full"
                  style={{ backgroundColor: topic.color }}
                />
              </div>
              <h3 className="text-xl font-bold mb-2">{topic.name}</h3>
              <p className="text-gray-600 text-sm mb-4">{topic.description}</p>
              <div className="flex justify-between items-center text-sm">
                <span className="text-gray-500">Questions: {topic.question_count || 0}</span>
                <div className="flex gap-2">
                  <Link
                    href={`/dashboard/dsa/topics/edit/${topic._id}`}
                    className="text-blue-600 hover:underline"
                  >
                    Edit
                  </Link>
                  <button
                    onClick={() => handleDelete(topic._id)}
                    className="text-red-600 hover:underline"
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
