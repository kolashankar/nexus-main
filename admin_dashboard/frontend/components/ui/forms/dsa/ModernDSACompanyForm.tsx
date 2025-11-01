'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Building2, CheckCircle, X, Plus, Image as ImageIcon } from 'lucide-react'

interface DSACompany { _id?: string; name: string; logo_url: string; description: string; interview_process: string[]; is_active: boolean }
interface Props { initialData?: DSACompany; isEditing?: boolean }

export default function ModernDSACompanyForm({ initialData, isEditing = false }: Props) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<Partial<DSACompany>>({
    name: initialData?.name || '', logo_url: initialData?.logo_url || '', description: initialData?.description || '',
    interview_process: initialData?.interview_process || [], is_active: initialData?.is_active ?? true,
  })
  const [processInput, setProcessInput] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.name) { alert('Fill required'); return }
    setLoading(true)
    try {
      const url = isEditing && initialData?._id ? `/api/admin/dsa/companies/${initialData._id}` : '/api/admin/dsa/companies'
      const res = await fetch(url, { method: isEditing ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(formData) })
      if (!res.ok) throw new Error('Failed')
      alert('✅ Saved!')
      router.push('/dashboard/dsa/companies/list')
    } catch (error: any) { alert('❌ Failed') } finally { setLoading(false) }
  }

  const addProcess = () => {
    if (processInput.trim()) {
      setFormData({ ...formData, interview_process: [...(formData.interview_process || []), processInput.trim()] })
      setProcessInput('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg border p-8 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Company Name *</label>
            <input type="text" required value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-slate-500" placeholder="e.g., Google" /></div>
          <div><label className="block text-sm font-semibold text-slate-700 mb-2">Logo URL</label>
            <input type="url" value={formData.logo_url} onChange={(e) => setFormData({ ...formData, logo_url: e.target.value })}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-slate-500" placeholder="https://..." /></div>
        </div>
        <div><label className="block text-sm font-semibold text-slate-700 mb-2">Description *</label>
          <textarea required value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} rows={4}
            className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-slate-500 resize-none" /></div>
        <div><label className="block text-sm font-semibold text-slate-700 mb-3">Interview Process</label>
          <div className="flex gap-2 mb-3">
            <input type="text" value={processInput} onChange={(e) => setProcessInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addProcess())}
              className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-slate-500" placeholder="e.g., Online Assessment" />
            <button type="button" onClick={addProcess} className="px-4 py-2 bg-slate-600 text-white rounded-lg hover:bg-slate-700 flex items-center">
              <Plus className="w-4 h-4 mr-1" /> Add
            </button>
          </div>
          <div className="space-y-2">
            {formData.interview_process?.map((step, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-slate-50 border rounded-lg">
                <span className="text-sm">{step}</span>
                <button type="button" onClick={() => setFormData({ ...formData, interview_process: formData.interview_process?.filter((_, i) => i !== idx) })} className="text-red-600"><X className="w-4 h-4" /></button>
              </div>
            ))}
          </div>
        </div>
        <div className="flex items-center"><input type="checkbox" id="is_active" checked={formData.is_active}
          onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })} className="w-4 h-4 text-slate-600 rounded" />
          <label htmlFor="is_active" className="ml-2 text-sm font-medium">Active</label></div>
      </div>
      <div className="flex justify-end space-x-4">
        <button type="button" onClick={() => router.back()} className="px-6 py-3 border text-slate-700 rounded-lg hover:bg-slate-50">Cancel</button>
        <button type="submit" disabled={loading} className="px-8 py-3 bg-gradient-to-r from-slate-600 to-gray-600 text-white rounded-lg shadow-lg disabled:opacity-50 flex items-center">
          {loading ? <><div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>Saving...</> : <><CheckCircle className="w-5 h-5 mr-2" />{isEditing ? 'Update' : 'Create'}</>}
        </button>
      </div>
    </form>
  )
}
