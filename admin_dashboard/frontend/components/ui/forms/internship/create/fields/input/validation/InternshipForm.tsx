'use client'

import { useState } from 'react'
import { internshipsApi, type Internship } from '@/lib/api/client/config/interceptors/auth/token/internshipsApi'
import { useRouter } from 'next/navigation'

interface InternshipFormProps {
  initialData?: Internship
  isEditing?: boolean
}

export default function InternshipForm({ initialData, isEditing = false }: InternshipFormProps) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<Partial<Internship>>({
    title: initialData?.title || '',
    company: initialData?.company || '',
    description: initialData?.description || '',
    location: initialData?.location || '',
    duration: initialData?.duration || '3 months',
    internship_type: initialData?.internship_type || 'full-time',
    category: initialData?.category || 'technology',
    stipend_amount: initialData?.stipend_amount || 0,
    currency: initialData?.currency || 'USD',
    skills_required: initialData?.skills_required || [],
    qualifications: initialData?.qualifications || [],
    learning_outcomes: initialData?.learning_outcomes || [],
    benefits: initialData?.benefits || [],
    apply_link: initialData?.apply_link || '',
    is_active: initialData?.is_active ?? true,
  })

  const [skillInput, setSkillInput] = useState('')
  const [qualInput, setQualInput] = useState('')
  const [outcomeInput, setOutcomeInput] = useState('')
  const [benefitInput, setBenefitInput] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (isEditing && initialData?._id) {
        await internshipsApi.update(initialData._id, formData)
        alert('Internship updated successfully!')
      } else {
        await internshipsApi.create(formData as Omit<Internship, '_id' | 'created_at' | 'updated_at'>)
        alert('Internship created successfully!')
      }
      router.push('/dashboard/internships/list')
    } catch (error: any) {
      console.error('Error saving internship:', error)
      alert(`Failed to save internship: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const addItem = (field: 'skills_required' | 'qualifications' | 'learning_outcomes' | 'benefits', value: string, setter: (value: string) => void) => {
    if (value.trim()) {
      setFormData({
        ...formData,
        [field]: [...(formData[field] || []), value.trim()],
      })
      setter('')
    }
  }

  const removeItem = (field: 'skills_required' | 'qualifications' | 'learning_outcomes' | 'benefits', index: number) => {
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
          <label className="block text-sm font-medium text-gray-700 mb-2">Internship Title *</label>
          <input
            type="text"
            required
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., Software Engineering Intern"
          />
        </div>

        {/* Company */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Company *</label>
          <input
            type="text"
            required
            value={formData.company}
            onChange={(e) => setFormData({ ...formData, company: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., Google"
          />
        </div>

        {/* Location */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Location *</label>
          <input
            type="text"
            required
            value={formData.location}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., Mountain View, CA"
          />
        </div>

        {/* Duration */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Duration *</label>
          <select
            required
            value={formData.duration}
            onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="2 months">2 Months</option>
            <option value="3 months">3 Months</option>
            <option value="6 months">6 Months</option>
            <option value="12 months">12 Months</option>
          </select>
        </div>

        {/* Internship Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Internship Type *</label>
          <select
            required
            value={formData.internship_type}
            onChange={(e) => setFormData({ ...formData, internship_type: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="full-time">Full-time</option>
            <option value="part-time">Part-time</option>
            <option value="remote">Remote</option>
            <option value="on-site">On-site</option>
          </select>
        </div>

        {/* Category */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Category *</label>
          <select
            required
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="technology">Technology</option>
            <option value="marketing">Marketing</option>
            <option value="finance">Finance</option>
            <option value="design">Design</option>
            <option value="engineering">Engineering</option>
          </select>
        </div>

        {/* Stipend */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Stipend Amount</label>
          <input
            type="number"
            value={formData.stipend_amount}
            onChange={(e) => setFormData({ ...formData, stipend_amount: parseFloat(e.target.value) })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="1000"
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
            placeholder="https://company.com/apply"
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
          placeholder="Detailed internship description..."
        />
      </div>

      {/* Skills */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Skills Required</label>
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={skillInput}
            onChange={(e) => setSkillInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('skills_required', skillInput, setSkillInput))}
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Add a skill and press Enter"
          />
          <button
            type="button"
            onClick={() => addItem('skills_required', skillInput, setSkillInput)}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Add
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {formData.skills_required?.map((skill, index) => (
            <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm flex items-center">
              {skill}
              <button
                type="button"
                onClick={() => removeItem('skills_required', index)}
                className="ml-2 text-blue-600 hover:text-blue-800"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      </div>

      {/* Qualifications */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Qualifications</label>
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={qualInput}
            onChange={(e) => setQualInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('qualifications', qualInput, setQualInput))}
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Add a qualification and press Enter"
          />
          <button
            type="button"
            onClick={() => addItem('qualifications', qualInput, setQualInput)}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Add
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {formData.qualifications?.map((qual, index) => (
            <span key={index} className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm flex items-center">
              {qual}
              <button
                type="button"
                onClick={() => removeItem('qualifications', index)}
                className="ml-2 text-green-600 hover:text-green-800"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      </div>

      {/* Learning Outcomes */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Learning Outcomes</label>
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={outcomeInput}
            onChange={(e) => setOutcomeInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('learning_outcomes', outcomeInput, setOutcomeInput))}
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Add a learning outcome and press Enter"
          />
          <button
            type="button"
            onClick={() => addItem('learning_outcomes', outcomeInput, setOutcomeInput)}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Add
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {formData.learning_outcomes?.map((outcome, index) => (
            <span key={index} className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm flex items-center">
              {outcome}
              <button
                type="button"
                onClick={() => removeItem('learning_outcomes', index)}
                className="ml-2 text-purple-600 hover:text-purple-800"
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
            <span key={index} className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm flex items-center">
              {benefit}
              <button
                type="button"
                onClick={() => removeItem('benefits', index)}
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
          {loading ? 'Saving...' : isEditing ? 'Update Internship' : 'Create Internship'}
        </button>
      </div>
    </form>
  )
}
