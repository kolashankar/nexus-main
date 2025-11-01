'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { BookOpen, CheckCircle, X, Plus, Image as ImageIcon } from 'lucide-react'

interface Article { _id?: string; title: string; content: string; excerpt: string; featured_image: string; category: string; tags: string[]; author: string; reading_time: number; is_published: boolean }
interface Props { initialData?: Article; isEditing?: boolean }

export default function ModernArticleForm({ initialData, isEditing = false }: Props) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<Partial<Article>>({
    title: initialData?.title || '', content: initialData?.content || '', excerpt: initialData?.excerpt || '',
    featured_image: initialData?.featured_image || '', category: initialData?.category || 'Tutorial',
    tags: initialData?.tags || [], author: initialData?.author || '', reading_time: initialData?.reading_time || 5,
    is_published: initialData?.is_published ?? true,
  })
  const [tagInput, setTagInput] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.title || !formData.content) { alert('Fill required'); return }
    setLoading(true)
    try {
      const url = isEditing && initialData?._id ? `/api/admin/learning/articles/${initialData._id}` : '/api/admin/learning/articles'
      const res = await fetch(url, { method: isEditing ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formData) })
      if (!res.ok) throw new Error('Failed')
      alert('✅ Saved!')
      router.push('/dashboard/learning/articles/list')
    } catch (error: any) { alert('❌ Failed') } finally { setLoading(false) }
  }

  const addTag = () => {
    if (tagInput.trim()) {
      setFormData({ ...formData, tags: [...(formData.tags || []), tagInput.trim()] })
      setTagInput('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg border p-8 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="md:col-span-2"><label className="block text-sm font-semibold text-slate-700 mb-2">Article Title *</label>
            <input type="text" required value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-rose-500" placeholder="e.g., Getting Started with React" /></div>
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Category *</label>
            <select required value={formData.category} onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-rose-500">
              <option value="Tutorial">Tutorial</option><option value="Guide">Guide</option><option value="News">News</option><option value="Tips">Tips</option></select></div>
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Author</label>
            <input type="text" value={formData.author} onChange={(e) => setFormData({ ...formData, author: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-rose-500" placeholder="Your Name" /></div>
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Reading Time (minutes)</label>
            <input type="number" value={formData.reading_time} onChange={(e) => setFormData({ ...formData, reading_time: parseInt(e.target.value) || 0 })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-rose-500" placeholder="5" /></div>
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Featured Image URL</label>
            <input type="url" value={formData.featured_image} onChange={(e) => setFormData({ ...formData, featured_image: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-rose-500" placeholder="https://..." /></div>
        </div>
        <div><label className="block text-sm font-semibold text-slate-700 mb-2">Excerpt</label>
          <textarea value={formData.excerpt} onChange={(e) => setFormData({ ...formData, excerpt: e.target.value })} rows={2}
            className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-rose-500 resize-none" placeholder="Short summary..." /></div>
        <div><label className="block text-sm font-semibold text-slate-700 mb-2">Content *</label>
          <textarea required value={formData.content} onChange={(e) => setFormData({ ...formData, content: e.target.value })} rows={12}
            className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-rose-500 resize-none" placeholder="Write your article content..." /></div>
        <div><label className="block text-sm font-semibold text-slate-700 mb-3">Tags</label>
          <div className="flex gap-2 mb-3">
            <input type="text" value={tagInput} onChange={(e) => setTagInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
              className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-rose-500" placeholder="e.g., React, JavaScript" />
            <button type="button" onClick={addTag} className="px-4 py-2 bg-rose-600 text-white rounded-lg hover:bg-rose-700 flex items-center">
              <Plus className="w-4 h-4 mr-1" /> Add
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {formData.tags?.map((tag, idx) => (
              <span key={idx} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-rose-100 text-rose-800">
                {tag}
                <button type="button" onClick={() => setFormData({ ...formData, tags: formData.tags?.filter((_, i) => i !== idx) })} className="ml-2 text-rose-600 hover:text-rose-800"><X className="w-3 h-3" /></button>
              </span>
            ))}
          </div>
        </div>
        <div className="flex items-center"><input type="checkbox" id="is_published" checked={formData.is_published}
          onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })} className="w-4 h-4 text-rose-600 rounded" />
          <label htmlFor="is_published" className="ml-2 text-sm font-medium">Published</label></div>
      </div>
      <div className="flex justify-end space-x-4">
        <button type="button" onClick={() => router.back()} className="px-6 py-3 border text-slate-700 rounded-lg hover:bg-slate-50">Cancel</button>
        <button type="submit" disabled={loading} className="px-8 py-3 bg-gradient-to-r from-rose-600 to-pink-600 text-white rounded-lg shadow-lg disabled:opacity-50 flex items-center">
          {loading ? <><div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>Saving...</> : <><CheckCircle className="w-5 h-5 mr-2" />{isEditing ? 'Update' : 'Create'}</>}
        </button>
      </div>
    </form>
  )
}
