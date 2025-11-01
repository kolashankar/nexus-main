'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { GraduationCap, DollarSign, MapPin, Clock, Users, Award, CheckCircle, X, Plus } from 'lucide-react'

interface Internship {
  _id?: string
  title: string
  company: string
  description: string
  location: string
  duration: string
  stipend: number
  currency: string
  category: string
  skills_required: string[]
  qualifications: string[]
  responsibilities: string[]
  benefits: string[]
  apply_link: string
  is_active: boolean
}

interface InternshipFormProps {
  initialData?: Internship
  isEditing?: boolean
}

export default function ModernInternshipForm({ initialData, isEditing = false }: InternshipFormProps) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('basic')
  const [formData, setFormData] = useState<Partial<Internship>>({
    title: initialData?.title || '',
    company: initialData?.company || '',
    description: initialData?.description || '',
    location: initialData?.location || '',
    duration: initialData?.duration || '',
    stipend: initialData?.stipend || 0,
    currency: initialData?.currency || 'INR',
    category: initialData?.category || 'Technology',
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
    
    if (!formData.title || !formData.company || !formData.description) {
      alert('Please fill in all required fields')
      return
    }

    setLoading(true)

    try {
      const url = isEditing && initialData?._id 
        ? `/api/admin/internships/${initialData._id}`
        : '/api/admin/internships'
      
      const response = await fetch(url, {
        method: isEditing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (!response.ok) throw new Error('Failed to save internship')

      alert(`✅ Internship ${isEditing ? 'updated' : 'created'} successfully!`)
      router.push('/dashboard/internships/list')
    } catch (error: any) {
      console.error('Error saving internship:', error)
      alert(`❌ Failed to save internship: ${error.message}`)
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

  const tabs = [
    { id: 'basic', name: 'Basic Info', icon: GraduationCap },
    { id: 'details', name: 'Internship Details', icon: Clock },
    { id: 'requirements', name: 'Requirements', icon: CheckCircle },
  ]

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden">
        <div className="border-b border-slate-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-purple-600 text-purple-600'
                      : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.name}</span>
                </button>
              )
            })}
          </nav>
        </div>

        <div className="p-8">
          {activeTab === 'basic' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Internship Title *</label>
                  <input
                    type="text"
                    required
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    placeholder="e.g., Software Engineering Intern"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Company *</label>
                  <input
                    type="text"
                    required
                    value={formData.company}
                    onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    placeholder="e.g., Microsoft"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Location *</label>
                  <div className="relative">
                    <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                      type="text"
                      required
                      value={formData.location}
                      onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                      className="w-full pl-11 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                      placeholder="e.g., Mumbai, India"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Duration *</label>
                  <input
                    type="text"
                    required
                    value={formData.duration}
                    onChange={(e) => setFormData({ ...formData, duration: e.target.value })}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                    placeholder="e.g., 3 months, 6 months"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Category *</label>
                  <select
                    required
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  >
                    <option value="Technology">Technology</option>
                    <option value="Marketing">Marketing</option>
                    <option value="Sales">Sales</option>
                    <option value="Design">Design</option>
                    <option value="Finance">Finance</option>
                    <option value="Healthcare">Healthcare</option>
                    <option value="Education">Education</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Description *</label>
                <textarea
                  required
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={6}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none"
                  placeholder="Describe the internship role..."
                />
              </div>
            </div>
          )}

          {activeTab === 'details' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Currency</label>
                  <select
                    value={formData.currency}
                    onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  >
                    <option value="INR">INR (₹)</option>
                    <option value="USD">USD ($)</option>
                    <option value="EUR">EUR (€)</option>
                    <option value="GBP">GBP (£)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Stipend (per month)</label>
                  <div className="relative">
                    <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                      type="number"
                      value={formData.stipend}
                      onChange={(e) => setFormData({ ...formData, stipend: parseInt(e.target.value) || 0 })}
                      className="w-full pl-11 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                      placeholder="15000"
                    />
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Application Link</label>
                <input
                  type="url"
                  value={formData.apply_link}
                  onChange={(e) => setFormData({ ...formData, apply_link: e.target.value })}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  placeholder="https://company.com/apply"
                />
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="is_active"
                  checked={formData.is_active}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  className="w-4 h-4 text-purple-600 border-slate-300 rounded focus:ring-purple-500"
                />
                <label htmlFor="is_active" className="ml-2 text-sm font-medium text-slate-700">
                  Active (visible to users)
                </label>
              </div>
            </div>
          )}

          {activeTab === 'requirements' && (
            <div className="space-y-8">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-3">Required Skills</label>
                <div className="flex gap-2 mb-3">
                  <input
                    type="text"
                    value={skillInput}
                    onChange={(e) => setSkillInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('skills_required', skillInput, setSkillInput))}
                    className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="e.g., Python, JavaScript"
                  />
                  <button
                    type="button"
                    onClick={() => addItem('skills_required', skillInput, setSkillInput)}
                    className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {formData.skills_required?.map((skill, index) => (
                    <span key={index} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
                      {skill}
                      <button type="button" onClick={() => removeItem('skills_required', index)} className="ml-2 text-purple-600 hover:text-purple-800">
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-3">Qualifications</label>
                <div className="flex gap-2 mb-3">
                  <input
                    type="text"
                    value={qualInput}
                    onChange={(e) => setQualInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('qualifications', qualInput, setQualInput))}
                    className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="e.g., Currently pursuing B.Tech"
                  />
                  <button
                    type="button"
                    onClick={() => addItem('qualifications', qualInput, setQualInput)}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Add
                  </button>
                </div>
                <div className="space-y-2">
                  {formData.qualifications?.map((qual, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded-lg">
                      <span className="text-sm text-green-900">{qual}</span>
                      <button type="button" onClick={() => removeItem('qualifications', index)} className="text-green-600 hover:text-green-800">
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-3">Responsibilities</label>
                <div className="flex gap-2 mb-3">
                  <input
                    type="text"
                    value={respInput}
                    onChange={(e) => setRespInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('responsibilities', respInput, setRespInput))}
                    className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="e.g., Assist in software development"
                  />
                  <button
                    type="button"
                    onClick={() => addItem('responsibilities', respInput, setRespInput)}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors flex items-center"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Add
                  </button>
                </div>
                <div className="space-y-2">
                  {formData.responsibilities?.map((resp, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-indigo-50 border border-indigo-200 rounded-lg">
                      <span className="text-sm text-indigo-900">{resp}</span>
                      <button type="button" onClick={() => removeItem('responsibilities', index)} className="text-indigo-600 hover:text-indigo-800">
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-3">Benefits</label>
                <div className="flex gap-2 mb-3">
                  <input
                    type="text"
                    value={benefitInput}
                    onChange={(e) => setBenefitInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addItem('benefits', benefitInput, setBenefitInput))}
                    className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="e.g., Certificate, Flexible hours"
                  />
                  <button
                    type="button"
                    onClick={() => addItem('benefits', benefitInput, setBenefitInput)}
                    className="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors flex items-center"
                  >
                    <Plus className="w-4 h-4 mr-1" />
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {formData.benefits?.map((benefit, index) => (
                    <span key={index} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-orange-100 text-orange-800">
                      {benefit}
                      <button type="button" onClick={() => removeItem('benefits', index)} className="ml-2 text-orange-600 hover:text-orange-800">
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}
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
          className="px-8 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 shadow-lg shadow-purple-500/50 transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Saving...
            </>
          ) : (
            <>
              <CheckCircle className="w-5 h-5 mr-2" />
              {isEditing ? 'Update Internship' : 'Create Internship'}
            </>
          )}
        </button>
      </div>
    </form>
  )
}
