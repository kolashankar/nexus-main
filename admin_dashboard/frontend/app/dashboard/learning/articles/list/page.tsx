'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { articlesApi, Article } from '@/lib/api/client/config/interceptors/auth/token/articlesApi'
import toast from 'react-hot-toast'

export default function ArticlesList() {
  const [articles, setArticles] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  useEffect(() => {
    fetchArticles()
  }, [searchTerm, categoryFilter, statusFilter])

  const fetchArticles = async () => {
    try {
      setLoading(true)
      const params: any = {}
      if (searchTerm) params.search = searchTerm
      if (categoryFilter) params.category = categoryFilter
      if (statusFilter !== 'all') params.is_published = statusFilter === 'published'
      
      const response = await articlesApi.getAll(params)
      setArticles(response.data.articles || [])
    } catch (error: any) {
      toast.error('Failed to fetch articles')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this article?')) return
    
    try {
      await articlesApi.delete(id)
      toast.success('Article deleted successfully')
      fetchArticles()
    } catch (error: any) {
      toast.error('Failed to delete article')
      console.error(error)
    }
  }

  const handleTogglePublish = async (id: string) => {
    try {
      await articlesApi.togglePublish(id)
      toast.success('Article status updated')
      fetchArticles()
    } catch (error: any) {
      toast.error('Failed to update article')
      console.error(error)
    }
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Articles</h1>
        <div className="flex gap-2">
          <Link
            href="/dashboard/learning/articles/create"
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Create Article
          </Link>
          <Link
            href="/dashboard/learning/articles/create-ai"
            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700"
          >
            Generate with AI
          </Link>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <input
            type="text"
            placeholder="Search articles..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 border rounded-lg"
          />
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="">All Categories</option>
            <option value="Career Guidance">Career Guidance</option>
            <option value="Interview Tips">Interview Tips</option>
            <option value="Technology">Technology</option>
            <option value="Skill Development">Skill Development</option>
          </select>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="all">All Status</option>
            <option value="published">Published</option>
            <option value="draft">Draft</option>
          </select>
        </div>
      </div>

      {/* Articles List */}
      {loading ? (
        <div className="text-center py-12">Loading...</div>
      ) : articles.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No articles found</div>
      ) : (
        <div className="grid gap-4">
          {articles.map((article) => (
            <div key={article._id} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-xl font-bold mb-2">{article.title}</h3>
                  <p className="text-gray-600 mb-3">{article.excerpt}</p>
                  <div className="flex gap-4 text-sm text-gray-500">
                    <span>Author: {article.author}</span>
                    <span>Category: {article.category}</span>
                    <span>Read Time: {article.read_time || 0} min</span>
                    <span>Views: {article.views_count || 0}</span>
                    <span className={`px-2 py-1 rounded ${article.is_published ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                      {article.is_published ? 'Published' : 'Draft'}
                    </span>
                  </div>
                  <div className="flex gap-2 mt-2">
                    {article.tags.map((tag) => (
                      <span key={tag} className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="flex flex-col gap-2 ml-4">
                  <Link
                    href={`/dashboard/learning/articles/${article._id}`}
                    className="text-blue-600 hover:underline text-sm"
                  >
                    Preview
                  </Link>
                  <Link
                    href={`/dashboard/learning/articles/edit/${article._id}`}
                    className="text-green-600 hover:underline text-sm"
                  >
                    Edit
                  </Link>
                  <button
                    onClick={() => handleTogglePublish(article._id!)}
                    className="text-orange-600 hover:underline text-sm"
                  >
                    {article.is_published ? 'Unpublish' : 'Publish'}
                  </button>
                  <button
                    onClick={() => handleDelete(article._id!)}
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
