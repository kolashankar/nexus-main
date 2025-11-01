'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { ListTree, CheckCircle, X, Plus, Link as LinkIcon } from 'lucide-react'

interface DSATopic {
  _id?: string
  name: string
  description: string
  category: string
  difficulty_level: string
  resources: Array<{ title: string; url: string }>
  is_active: boolean
}

interface DSATopicFormProps {
  initialData?: DSATopic
  isEditing?: boolean
}

export default function ModernDSATopicForm({ initialData, isEditing = false }: DSATopicFormProps) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<Partial<DSATopic>>({
    name: initialData?.name || '',
    description: initialData?.description || '',
    category: initialData?.category || 'Arrays',
    difficulty_level: initialData?.difficulty_level || 'Beginner',
    resources: initialData?.resources || [],
    is_active: initialData?.is_active ?? true,
  })
  const [resourceInput, setResourceInput] = useState({ title: '', url: '' })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.name) {
      alert('Please fill in required fields')
      return
    }
    setLoading(true)
    try {
      const url = isEditing && initialData?._id ? `/api/admin/dsa/topics/${initialData._id}` : '/api/admin/dsa/topics'
      const res = await fetch(url, { method: isEditing ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formData) })
      if (!res.ok) throw new Error('Failed')
      alert('✅ Topic saved!')
      router.push('/dashboard/dsa/topics/list')
    } catch (error: any) {
      alert('❌ Failed: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const addResource = () => {
    if (resourceInput.title && resourceInput.url) {
      setFormData({ ...formData, resources: [...(formData.resources || []), resourceInput] })
      setResourceInput({ title: '', url: '' })
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-8 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Topic Name *</label>
            <input type="text" required value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-cyan-500" placeholder="e.g., Binary Search" />
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Category *</label>
            <select required value={formData.category} onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-cyan-500">
              <option value="Arrays">Arrays</option>
              <option value="Strings">Strings</option>
              <option value="Trees">Trees</option>
              <option value="Graphs">Graphs</option>
              <option value="Dynamic Programming">Dynamic Programming</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Difficulty Level *</label>
            <select required value={formData.difficulty_level} onChange={(e) => setFormData({ ...formData, difficulty_level: e.target.value })}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-cyan-500">
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
          </div>
        </div>
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-2">Description *</label>
          <textarea required value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} rows={5}
            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-cyan-500 resize-none" />
        </div>
        <div>
          <label className="block text-sm font-semibold text-slate-700 mb-3">Resources</label>
          <div className="space-y-2 mb-3">
            <input type="text" placeholder="Resource Title" value={resourceInput.title} onChange={(e) => setResourceInput({ ...resourceInput, title: e.target.value })}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-cyan-500" />
            <input type="url" placeholder="Resource URL" value={resourceInput.url} onChange={(e) => setResourceInput({ ...resourceInput, url: e.target.value })}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-cyan-500" />
            <button type="button" onClick={addResource} className="px-4 py-2 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 flex items-center">
              <Plus className="w-4 h-4 mr-1" /> Add Resource
            </button>
          </div>
          <div className="space-y-2">
            {formData.resources?.map((res, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-cyan-50 border border-cyan-200 rounded-lg">
                <div><strong>{res.title}</strong><br/><a href={res.url} target="_blank" className="text-sm text-cyan-600">{res.url}</a></div>
                <button type="button" onClick={() => setFormData({ ...formData, resources: formData.resources?.filter((_, i) => i !== idx) })} className="text-red-600"><X className="w-4 h-4" /></button>
              </div>
            ))}
          </div>
        </div>
        <div className="flex items-center">
          <input type="checkbox" id="is_active" checked={formData.is_active} onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
            className="w-4 h-4 text-cyan-600 border-slate-300 rounded" />
          <label htmlFor="is_active" className="ml-2 text-sm font-medium text-slate-700">Active</label>
        </div>
      </div>
      <div className="flex justify-end space-x-4">
        <button type="button" onClick={() => router.back()} className="px-6 py-3 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 font-medium">Cancel</button>
        <button type="submit" disabled={loading} className="px-8 py-3 bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-lg hover:from-cyan-700 hover:to-blue-700 shadow-lg shadow-cyan-500/50 font-medium disabled:opacity-50 flex items-center">
          {loading ? <><div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>Saving...</> : <><CheckCircle className="w-5 h-5 mr-2" />{isEditing ? 'Update' : 'Create'}</>}
        </button>
      </div>
    </form>
  )
}
