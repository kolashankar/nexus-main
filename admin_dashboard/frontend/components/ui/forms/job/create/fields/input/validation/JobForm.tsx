'use client'

import { useState } from 'react'
import { jobsApi, type Job } from '@/lib/api/client/config/interceptors/auth/token/jobsApi'
import { useRouter } from 'next/navigation'

interface JobFormProps {
  initialData?: Job
  isEditing?: boolean
}

export default function JobForm({ initialData, isEditing = false }: JobFormProps) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<Partial<Job>>({
    title: initialData?.title || '',
    company: initialData?.company || '',
    description: initialData?.description || '',
    location: initialData?.location || '',
    job_type: initialData?.job_type || 'full-time',
    category: initialData?.category || 'technology',
    salary_min: initialData?.salary_min || 0,
    salary_max: initialData?.salary_max || 0,
    currency: initialData?.currency || 'USD',
    experience_level: initialData?.experience_level || 'mid',
    skills_required: initialData?.skills_required || [],
    qualifications: initialData?.qualifications || [],
    responsibilities: initialData?.responsibilities || [],
    benefits: initialData?.benefits || [],
    apply_link: initialData?.apply_link || '',
    is_active: initialData?.is_active ?? true,
  })

  const [skillInput, setSkillInput] = useState('')
  const [qualInput, setQualInput] = useState('')
  const [respInput, setRespInput] = useState('')
  const [benefitInput, setBenefitInput] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (isEditing && initialData?._id) {
        await jobsApi.update(initialData._id, formData)
        alert('Job updated successfully!')
      } else {
        await jobsApi.create(formData as Omit<Job, '_id' | 'created_at' | 'updated_at'>)
        alert('Job created successfully!')
      }
      router.push('/dashboard/jobs/list')
    } catch (error: any) {
      console.error('Error saving job:', error)
      alert(`Failed to save job: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const addItem = (field: 'skills_required' | 'qualifications' | 'responsibilities' | 'benefits', value: string, setter: (value: string) => void) => {
    if (value.trim()) {
      setFormData({
        ...formData,
        [field]: [...(formData[field] || []), value.trim()],
      })
      setter('')
    }
  }

  const removeItem = (field: 'skills_required' | 'qualifications' | 'responsibilities' | 'benefits', index: number) => {
    setFormData({
      ...formData,
      [field]: formData[field]?.filter((_, i) => i !== index),
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Job Title */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Job Title *</label>
          <input
            type="text"
            required
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., Senior Software Engineer"
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
            placeholder="e.g., San Francisco, CA"
          />
        </div>

        {/* Job Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Job Type *</label>
          <select
            required
            value={formData.job_type}
            onChange={(e) => setFormData({ ...formData, job_type: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="full-time">Full-time</option>
            <option value="part-time">Part-time</option>
            <option value="contract">Contract</option>
            <option value="remote">Remote</option>
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
            <option value="sales">Sales</option>
            <option value="design">Design</option>
          </select>
        </div>

        {/* Experience Level */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Experience Level *</label>
          <select
            required
            value={formData.experience_level}
            onChange={(e) => setFormData({ ...formData, experience_level: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="entry">Entry Level</option>
            <option value="mid">Mid Level</option>
            <option value="senior">Senior Level</option>
          </select>
        </div>

        {/* Salary Range */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Salary Min</label>
          <input
            type="number"
            value={formData.salary_min}
            onChange={(e) => setFormData({ ...formData, salary_min: parseFloat(e.target.value) })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="50000"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Salary Max</label>
          <input
            type="number"
            value={formData.salary_max}
            onChange={(e) => setFormData({ ...formData, salary_max: parseFloat(e.target.value) })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="100000"
          />
        </div>

        {/* Apply Link */}
        <div className="md:col-span-2">
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
          placeholder="Detailed job description..."
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

      {/* Responsibilities */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Responsibilities</label>
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={respInput}
            onChange={(e) => setRespInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('responsibilities', respInput, setRespInput))}
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Add a responsibility and press Enter"
          />
          <button
            type="button"
            onClick={() => addItem('responsibilities', respInput, setRespInput)}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Add
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {formData.responsibilities?.map((resp, index) => (
            <span key={index} className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm flex items-center">
              {resp}
              <button
                type="button"
                onClick={() => removeItem('responsibilities', index)}
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
          {loading ? 'Saving...' : isEditing ? 'Update Job' : 'Create Job'}
        </button>
      </div>
    </form>
  )
}
