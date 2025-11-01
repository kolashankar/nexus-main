'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Map, CheckCircle, X, Plus } from 'lucide-react'

interface Roadmap { _id?: string; title: string; description: string; category: string; difficulty_level: string; estimated_duration: string; prerequisites: string[]; is_active: boolean }
interface Props { initialData?: Roadmap; isEditing?: boolean }

export default function ModernRoadmapForm({ initialData, isEditing = false }: Props) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<Partial<Roadmap>>({
    title: initialData?.title || '', description: initialData?.description || '', category: initialData?.category || 'Frontend',
    difficulty_level: initialData?.difficulty_level || 'Beginner', estimated_duration: initialData?.estimated_duration || '',
    prerequisites: initialData?.prerequisites || [], is_active: initialData?.is_active ?? true,
  })
  const [prereqInput, setPrereqInput] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.title) { alert('Fill required'); return }
    setLoading(true)
    try {
      const url = isEditing && initialData?._id ? `/api/admin/roadmaps/${initialData._id}` : '/api/admin/roadmaps'
      const res = await fetch(url, { method: isEditing ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formData) })
      if (!res.ok) throw new Error('Failed')
      alert('✅ Saved!')
      router.push('/dashboard/roadmaps/list')
    } catch (error: any) { alert('❌ Failed') } finally { setLoading(false) }
  }

  const addPrereq = () => {
    if (prereqInput.trim()) {
      setFormData({ ...formData, prerequisites: [...(formData.prerequisites || []), prereqInput.trim()] })
      setPrereqInput('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg border p-8 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Roadmap Title *</label>
            <input type="text" required value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500" placeholder="e.g., Full Stack Development" /></div>
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Category *</label>
            <select required value={formData.category} onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500">
              <option value="Frontend">Frontend</option><option value="Backend">Backend</option><option value="Full Stack">Full Stack</option><option value="DevOps">DevOps</option><option value="Mobile">Mobile</option><option value="Data Science">Data Science</option></select></div>
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Difficulty Level *</label>
            <select required value={formData.difficulty_level} onChange={(e) => setFormData({ ...formData, difficulty_level: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500">
              <option value="Beginner">Beginner</option><option value="Intermediate">Intermediate</option><option value="Advanced">Advanced</option></select></div>
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Estimated Duration</label>
            <input type="text" value={formData.estimated_duration} onChange={(e) => setFormData({ ...formData, estimated_duration: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500" placeholder="e.g., 6 months" /></div>
        </div>
        <div><label className="block text-sm font-semibold text-slate-700 mb-2">Description *</label>
          <textarea required value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} rows={5}
            className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 resize-none" /></div>
        <div><label className="block text-sm font-semibold text-slate-700 mb-3">Prerequisites</label>
          <div className="flex gap-2 mb-3">
            <input type="text" value={prereqInput} onChange={(e) => setPrereqInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addPrereq())}
              className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500" placeholder="e.g., Basic HTML/CSS" />
            <button type="button" onClick={addPrereq} className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center">
              <Plus className="w-4 h-4 mr-1" /> Add
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {formData.prerequisites?.map((prereq, idx) => (
              <span key={idx} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
                {prereq}
                <button type="button" onClick={() => setFormData({ ...formData, prerequisites: formData.prerequisites?.filter((_, i) => i !== idx) })} className="ml-2 text-indigo-600 hover:text-indigo-800"><X className="w-3 h-3" /></button>
              </span>
            ))}
          </div>
        </div>
        <div className="flex items-center"><input type="checkbox" id="is_active" checked={formData.is_active}
          onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })} className="w-4 h-4 text-indigo-600 rounded" />
          <label htmlFor="is_active" className="ml-2 text-sm font-medium">Active</label></div>
      </div>
      <div className="flex justify-end space-x-4">
        <button type="button" onClick={() => router.back()} className="px-6 py-3 border text-slate-700 rounded-lg hover:bg-slate-50">Cancel</button>
        <button type="submit" disabled={loading} className="px-8 py-3 bg-gradient-to-r from-indigo-600 to-blue-600 text-white rounded-lg shadow-lg disabled:opacity-50 flex items-center">
          {loading ? <><div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>Saving...</> : <><CheckCircle className="w-5 h-5 mr-2" />{isEditing ? 'Update' : 'Create'}</>}
        </button>
      </div>
    </form>
  )
}
