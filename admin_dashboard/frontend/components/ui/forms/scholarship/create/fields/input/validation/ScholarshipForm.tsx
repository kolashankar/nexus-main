'use client'

import { useState } from 'react'
import { scholarshipsApi, type Scholarship } from '@/lib/api/client/config/interceptors/auth/token/scholarshipsApi'
import { useRouter } from 'next/navigation'

interface ScholarshipFormProps {
  initialData?: Scholarship
  isEditing?: boolean
}

export default function ScholarshipForm({ initialData, isEditing = false }: ScholarshipFormProps) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<Partial<Scholarship>>({
    title: initialData?.title || '',
    provider: initialData?.provider || '',
    description: initialData?.description || '',
    country: initialData?.country || '',
    scholarship_type: initialData?.scholarship_type || 'merit-based',
    education_level: initialData?.education_level || 'undergraduate',
    amount: initialData?.amount || 0,
    currency: initialData?.currency || 'USD',
    deadline: initialData?.deadline || '',
    field_of_study: initialData?.field_of_study || [],
    eligibility_criteria: initialData?.eligibility_criteria || [],
    benefits: initialData?.benefits || [],
    application_process: initialData?.application_process || [],
    apply_link: initialData?.apply_link || '',
    is_active: initialData?.is_active ?? true,
  })

  const [fieldInput, setFieldInput] = useState('')
  const [eligibilityInput, setEligibilityInput] = useState('')
  const [benefitInput, setBenefitInput] = useState('')
  const [processInput, setProcessInput] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (isEditing && initialData?._id) {
        await scholarshipsApi.update(initialData._id, formData)
        alert('Scholarship updated successfully!')
      } else {
        await scholarshipsApi.create(formData as Omit<Scholarship, '_id' | 'created_at' | 'updated_at'>)
        alert('Scholarship created successfully!')
      }
      router.push('/dashboard/scholarships/list')
    } catch (error: any) {
      console.error('Error saving scholarship:', error)
      alert(`Failed to save scholarship: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const addItem = (field: 'field_of_study' | 'eligibility_criteria' | 'benefits' | 'application_process', value: string, setter: (value: string) => void) => {
    if (value.trim()) {
      setFormData({
        ...formData,
        [field]: [...(formData[field] || []), value.trim()],
      })
      setter('')
    }
  }

  const removeItem = (field: 'field_of_study' | 'eligibility_criteria' | 'benefits' | 'application_process', index: number) => {
    setFormData({
      ...formData,
      [field]: formData[field]?.filter((_, i) => i !== index),
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Title */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Scholarship Title *</label>
          <input
            type="text"
            required
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., Fulbright Scholarship Program"
          />
        </div>

        {/* Provider */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Provider *</label>
          <input
            type="text"
            required
            value={formData.provider}
            onChange={(e) => setFormData({ ...formData, provider: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., U.S. Department of State"
          />
        </div>

        {/* Country */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Country *</label>
          <input
            type="text"
            required
            value={formData.country}
            onChange={(e) => setFormData({ ...formData, country: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., United States"
          />
        </div>

        {/* Scholarship Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Scholarship Type *</label>
          <select
            required
            value={formData.scholarship_type}
            onChange={(e) => setFormData({ ...formData, scholarship_type: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="merit-based">Merit-based</option>
            <option value="need-based">Need-based</option>
            <option value="full-funding">Full Funding</option>
            <option value="partial-funding">Partial Funding</option>
          </select>
        </div>

        {/* Education Level */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Education Level *</label>
          <select
            required
            value={formData.education_level}
            onChange={(e) => setFormData({ ...formData, education_level: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="undergraduate">Undergraduate</option>
            <option value="postgraduate">Postgraduate</option>
            <option value="doctorate">Doctorate</option>
          </select>
        </div>

        {/* Amount */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Scholarship Amount</label>
          <input
            type="number"
            value={formData.amount}
            onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="10000"
          />
        </div>

        {/* Deadline */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Application Deadline</label>
          <input
            type="date"
            value={formData.deadline}
            onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Apply Link */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Apply Link</label>
          <input
            type="url"
            value={formData.apply_link}
            onChange={(e) => setFormData({ ...formData, apply_link: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="https://scholarship.org/apply"
          />
        </div>
      </div>

      {/* Description */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Description *</label>
        <textarea
          required
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          rows={6}
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          placeholder="Detailed scholarship description..."
        />
      </div>

      {/* Field of Study */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Field of Study</label>
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={fieldInput}
            onChange={(e) => setFieldInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('field_of_study', fieldInput, setFieldInput))}
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Add a field of study and press Enter"
          />
          <button
            type="button"
            onClick={() => addItem('field_of_study', fieldInput, setFieldInput)}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Add
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {formData.field_of_study?.map((field, index) => (
            <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm flex items-center">
              {field}
              <button
                type="button"
                onClick={() => removeItem('field_of_study', index)}
                className="ml-2 text-blue-600 hover:text-blue-800"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      </div>

      {/* Eligibility Criteria */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Eligibility Criteria</label>
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={eligibilityInput}
            onChange={(e) => setEligibilityInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('eligibility_criteria', eligibilityInput, setEligibilityInput))}
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Add an eligibility criterion and press Enter"
          />
          <button
            type="button"
            onClick={() => addItem('eligibility_criteria', eligibilityInput, setEligibilityInput)}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Add
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {formData.eligibility_criteria?.map((criteria, index) => (
            <span key={index} className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm flex items-center">
              {criteria}
              <button
                type="button"
                onClick={() => removeItem('eligibility_criteria', index)}
                className="ml-2 text-green-600 hover:text-green-800"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      </div>

      {/* Benefits */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Benefits</label>
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={benefitInput}
            onChange={(e) => setBenefitInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('benefits', benefitInput, setBenefitInput))}
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Add a benefit and press Enter"
          />
          <button
            type="button"
            onClick={() => addItem('benefits', benefitInput, setBenefitInput)}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Add
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {formData.benefits?.map((benefit, index) => (
            <span key={index} className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm flex items-center">
              {benefit}
              <button
                type="button"
                onClick={() => removeItem('benefits', index)}
                className="ml-2 text-purple-600 hover:text-purple-800"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      </div>

      {/* Application Process */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Application Process</label>
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={processInput}
            onChange={(e) => setProcessInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('application_process', processInput, setProcessInput))}
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Add an application step and press Enter"
          />
          <button
            type="button"
            onClick={() => addItem('application_process', processInput, setProcessInput)}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Add
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {formData.application_process?.map((step, index) => (
            <span key={index} className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm flex items-center">
              {step}
              <button
                type="button"
                onClick={() => removeItem('application_process', index)}
                className="ml-2 text-yellow-600 hover:text-yellow-800"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      </div>

      {/* Status */}
      <div className="flex items-center">
        <input
          type="checkbox"
          checked={formData.is_active}
          onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
          className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
        />
        <label className="ml-2 text-sm font-medium text-gray-700">Active (visible to users)</label>
      </div>

      {/* Submit Buttons */}
      <div className="flex justify-end space-x-4">
        <button
          type="button"
          onClick={() => router.back()}
          className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Saving...' : isEditing ? 'Update Scholarship' : 'Create Scholarship'}
        </button>
      </div>
    </form>
  )
}
