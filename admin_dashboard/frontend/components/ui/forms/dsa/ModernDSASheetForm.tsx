'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Layers, CheckCircle, Clock } from 'lucide-react'

interface DSASheet { _id?: string; name: string; description: string; difficulty: string; estimated_time: string; is_active: boolean }
interface Props { initialData?: DSASheet; isEditing?: boolean }

export default function ModernDSASheetForm({ initialData, isEditing = false }: Props) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<Partial<DSASheet>>({
    name: initialData?.name || '', description: initialData?.description || '', difficulty: initialData?.difficulty || 'Beginner',
    estimated_time: initialData?.estimated_time || '', is_active: initialData?.is_active ?? true,
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.name) { alert('Fill required fields'); return }
    setLoading(true)
    try {
      const url = isEditing && initialData?._id ? `/api/admin/dsa/sheets/${initialData._id}` : '/api/admin/dsa/sheets'
      const res = await fetch(url, { method: isEditing ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formData) })
      if (!res.ok) throw new Error('Failed')
      alert('✅ Saved!')
      router.push('/dashboard/dsa/sheets/list')
    } catch (error: any) { alert('❌ Failed') } finally { setLoading(false) }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg border p-8 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Sheet Name *</label>
            <input type="text" required value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-violet-500" placeholder="e.g., Striver's SDE Sheet" /></div>
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Difficulty *</label>
            <select required value={formData.difficulty} onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-violet-500">
              <option value="Beginner">Beginner</option><option value="Intermediate">Intermediate</option><option value="Advanced">Advanced</option></select></div>
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Estimated Time</label>
            <input type="text" value={formData.estimated_time} onChange={(e) => setFormData({ ...formData, estimated_time: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-violet-500" placeholder="e.g., 30 days" /></div>
        </div>
        <div><label className="block text-sm font-semibold text-slate-700 mb-2">Description *</label>
          <textarea required value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} rows={5}
            className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-violet-500 resize-none" /></div>
        <div className="flex items-center"><input type="checkbox" id="is_active" checked={formData.is_active}
          onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })} className="w-4 h-4 text-violet-600 rounded" />
          <label htmlFor="is_active" className="ml-2 text-sm font-medium">Active</label></div>
      </div>
      <div className="flex justify-end space-x-4">
        <button type="button" onClick={() => router.back()} className="px-6 py-3 border text-slate-700 rounded-lg hover:bg-slate-50">Cancel</button>
        <button type="submit" disabled={loading} className="px-8 py-3 bg-gradient-to-r from-violet-600 to-purple-600 text-white rounded-lg shadow-lg disabled:opacity-50 flex items-center">
          {loading ? <><div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>Saving...</> : <><CheckCircle className="w-5 h-5 mr-2" />{isEditing ? 'Update' : 'Create'}</>}
        </button>
      </div>
    </form>
  )
}
