'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { articlesApi, Article } from '@/lib/api/client/config/interceptors/auth/token/articlesApi'
import toast from 'react-hot-toast'

export default function ArticlePreview() {
  const params = useParams()
  const router = useRouter()
  const id = params.id as string
  const [article, setArticle] = useState<Article | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchArticle()
  }, [id])

  const fetchArticle = async () => {
    try {
      setLoading(true)
      const response = await articlesApi.getById(id)
      setArticle(response.data)
    } catch (error: any) {
      toast.error('Failed to fetch article')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="p-6 text-center">Loading article...</div>
  }

  if (!article) {
    return <div className="p-6 text-center">Article not found</div>
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <button
          onClick={() => router.back()}
          className="text-blue-600 hover:underline mb-4"
        >
          ← Back to Articles
        </button>
      </div>

      <article className="bg-white p-8 rounded-lg shadow">
        {article.cover_image && (
          <img
            src={article.cover_image}
            alt={article.title}
            className="w-full h-64 object-cover rounded-lg mb-6"
          />
        )}

        <div className="mb-6">
          <h1 className="text-4xl font-bold mb-4">{article.title}</h1>
          <div className="flex flex-wrap gap-4 text-sm text-gray-600">
            <span>👤 {article.author}</span>
            <span>📁 {article.category}</span>
            <span>⏱️ {article.read_time} min read</span>
            <span>👁️ {article.views_count || 0} views</span>
            <span className={`px-2 py-1 rounded ${
              article.is_published 
                ? 'bg-green-100 text-green-800' 
                : 'bg-gray-100 text-gray-800'
            }`}>
              {article.is_published ? 'Published' : 'Draft'}
            </span>
          </div>
        </div>

        <div className="mb-6">
          <p className="text-xl text-gray-700 italic">{article.excerpt}</p>
        </div>

        <div className="flex flex-wrap gap-2 mb-6">
          {article.tags.map((tag) => (
            <span key={tag} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
              #{tag}
            </span>
          ))}
        </div>

        <div 
          className="prose max-w-none"
          dangerouslySetInnerHTML={{ __html: article.content }}
        />
      </article>

      <div className="mt-6 flex gap-4">
        <button
          onClick={() => router.push(`/dashboard/learning/articles/edit/${id}`)}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
        >
          Edit Article
        </button>
        <button
          onClick={() => router.push('/dashboard/learning/articles/list')}
          className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400"
        >
          Back to List
        </button>
      </div>
    </div>
  )
}
