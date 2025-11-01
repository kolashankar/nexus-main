'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Award, DollarSign, Calendar, CheckCircle, X, Plus, Link as LinkIcon } from 'lucide-react'

interface Scholarship {
  _id?: string
  title: string
  organization: string
  description: string
  amount: number
  currency: string
  deadline: string
  eligibility_criteria: string[]
  application_link: string
  is_active: boolean
}

interface ScholarshipFormProps {
  initialData?: Scholarship
  isEditing?: boolean
}

export default function ModernScholarshipForm({ initialData, isEditing = false }: ScholarshipFormProps) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<Partial<Scholarship>>({
    title: initialData?.title || '',
    organization: initialData?.organization || '',
    description: initialData?.description || '',
    amount: initialData?.amount || 0,
    currency: initialData?.currency || 'INR',
    deadline: initialData?.deadline || '',
    eligibility_criteria: initialData?.eligibility_criteria || [],
    application_link: initialData?.application_link || '',
    is_active: initialData?.is_active ?? true,
  })

  const [criteriaInput, setCriteriaInput] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.title || !formData.organization || !formData.description) {
      alert('Please fill in all required fields')
      return
    }

    setLoading(true)

    try {
      const url = isEditing && initialData?._id 
        ? `/api/admin/scholarships/${initialData._id}`
        : '/api/admin/scholarships'
      
      const response = await fetch(url, {
        method: isEditing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (!response.ok) throw new Error('Failed to save scholarship')

      alert(`✅ Scholarship ${isEditing ? 'updated' : 'created'} successfully!`)
      router.push('/dashboard/scholarships/list')
    } catch (error: any) {
      console.error('Error saving scholarship:', error)
      alert(`❌ Failed to save scholarship: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const addCriteria = () => {
    if (criteriaInput.trim()) {
      setFormData({
        ...formData,
        eligibility_criteria: [...(formData.eligibility_criteria || []), criteriaInput.trim()],
      })
      setCriteriaInput('')
    }
  }

  const removeCriteria = (index: number) => {
    setFormData({
      ...formData,
      eligibility_criteria: formData.eligibility_criteria?.filter((_, i) => i !== index),
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-8">
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Scholarship Title *</label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                placeholder="e.g., Merit-Based Scholarship 2024"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Organization *</label>
              <input
                type="text"
                required
                value={formData.organization}
                onChange={(e) => setFormData({ ...formData, organization: e.target.value })}
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                placeholder="e.g., National Scholarship Foundation"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Currency</label>
              <select
                value={formData.currency}
                onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
              >
                <option value="INR">INR (₹)</option>
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Scholarship Amount</label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="number"
                  value={formData.amount}
                  onChange={(e) => setFormData({ ...formData, amount: parseInt(e.target.value) || 0 })}
                  className="w-full pl-11 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                  placeholder="50000"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Application Deadline</label>
              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="date"
                  value={formData.deadline}
                  onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
                  className="w-full pl-11 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Application Link</label>
              <div className="relative">
                <LinkIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="url"
                  value={formData.application_link}
                  onChange={(e) => setFormData({ ...formData, application_link: e.target.value })}
                  className="w-full pl-11 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                  placeholder="https://organization.com/apply"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Description *</label>
            <textarea
              required
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={6}
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all resize-none"
              placeholder="Describe the scholarship program..."
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-3">Eligibility Criteria</label>
            <div className="flex gap-2 mb-3">
              <input
                type="text"
                value={criteriaInput}
                onChange={(e) => setCriteriaInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCriteria())}
                className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="e.g., Minimum 80% marks in previous exam"
              />
              <button
                type="button"
                onClick={addCriteria}
                className="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors flex items-center"
              >
                <Plus className="w-4 h-4 mr-1" />
                Add
              </button>
            </div>
            <div className="space-y-2">
              {formData.eligibility_criteria?.map((criteria, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-orange-50 border border-orange-200 rounded-lg">
                  <span className="text-sm text-orange-900">{criteria}</span>
                  <button type="button" onClick={() => removeCriteria(index)} className="text-orange-600 hover:text-orange-800">
                    <X className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="is_active"
              checked={formData.is_active}
              onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
              className="w-4 h-4 text-orange-600 border-slate-300 rounded focus:ring-orange-500"
            />
            <label htmlFor="is_active" className="ml-2 text-sm font-medium text-slate-700">
              Active (visible to users)
            </label>
          </div>
        </div>
      </div>

      <div className="flex justify-end space-x-4">
        <button
          type="button"
          onClick={() => router.back()}
          className="px-6 py-3 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-all font-medium"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-8 py-3 bg-gradient-to-r from-orange-600 to-amber-600 text-white rounded-lg hover:from-orange-700 hover:to-amber-700 shadow-lg shadow-orange-500/50 transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Saving...
            </>
          ) : (
            <>
              <CheckCircle className="w-5 h-5 mr-2" />
              {isEditing ? 'Update Scholarship' : 'Create Scholarship'}
            </>
          )}
        </button>
      </div>
    </form>
  )
}
