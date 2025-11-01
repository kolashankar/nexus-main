'use client'

import { useEffect, useState } from 'react'
import { careerToolsApi, type CareerToolTemplate } from '@/lib/api/client/config/interceptors/auth/token/careerToolsApi'
import DashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/DashboardLayout'

export default function CareerToolTemplatesPage() {
  const [templates, setTemplates] = useState<CareerToolTemplate[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingTemplate, setEditingTemplate] = useState<CareerToolTemplate | null>(null)
  const [formData, setFormData] = useState({
    tool_type: 'resume_review' as 'resume_review' | 'cover_letter' | 'ats_hack' | 'cold_email',
    name: '',
    description: '',
    prompt_template: '',
    is_active: true,
  })

  useEffect(() => {
    fetchTemplates()
  }, [])

  const fetchTemplates = async () => {
    try {
      setLoading(true)
      const response = await careerToolsApi.getTemplates()
      setTemplates(response.templates)
    } catch (error) {
      console.error('Error fetching templates:', error)
      alert('Failed to fetch templates')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      if (editingTemplate) {
        await careerToolsApi.updateTemplate(editingTemplate._id!, formData)
        alert('Template updated successfully!')
      } else {
        await careerToolsApi.createTemplate(formData)
        alert('Template created successfully!')
      }
      
      setShowForm(false)
      setEditingTemplate(null)
      resetForm()
      fetchTemplates()
    } catch (error: any) {
      console.error('Error saving template:', error)
      alert(error.response?.data?.detail || 'Failed to save template')
    }
  }

  const handleEdit = (template: CareerToolTemplate) => {
    setEditingTemplate(template)
    setFormData({
      tool_type: template.tool_type,
      name: template.name,
      description: template.description,
      prompt_template: template.prompt_template,
      is_active: template.is_active,
    })
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this template?')) return

    try {
      await careerToolsApi.deleteTemplate(id)
      alert('Template deleted successfully')
      fetchTemplates()
    } catch (error) {
      console.error('Error deleting template:', error)
      alert('Failed to delete template')
    }
  }

  const resetForm = () => {
    setFormData({
      tool_type: 'resume_review',
      name: '',
      description: '',
      prompt_template: '',
      is_active: true,
    })
  }

  const getToolTypeLabel = (type: string) => {
    const labels: { [key: string]: string } = {
      resume_review: 'Resume Review',
      cover_letter: 'Cover Letter',
      ats_hack: 'ATS Hack',
      cold_email: 'Cold Email',
    }
    return labels[type] || type
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Career Tools Templates</h1>
            <p className="text-gray-600 mt-1">Manage AI prompt templates for career tools</p>
          </div>
          <button
            onClick={() => {
              setShowForm(true)
              setEditingTemplate(null)
              resetForm()
            }}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
          >
            + Create Template
          </button>
        </div>

        {showForm && (
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">
              {editingTemplate ? 'Edit Template' : 'Create New Template'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tool Type *
                </label>
                <select
                  required
                  value={formData.tool_type}
                  onChange={(e) => setFormData({ ...formData, tool_type: e.target.value as any })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="resume_review">Resume Review</option>
                  <option value="cover_letter">Cover Letter Generator</option>
                  <option value="ats_hack">ATS Hack</option>
                  <option value="cold_email">Cold Email Generator</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Template Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="e.g., Default Resume Review Template"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description *
                </label>
                <textarea
                  required
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Brief description of the template"
                  rows={2}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Prompt Template *
                </label>
                <textarea
                  required
                  value={formData.prompt_template}
                  onChange={(e) => setFormData({ ...formData, prompt_template: e.target.value })}
                  placeholder="Enter the AI prompt template. Use {variable} for placeholders."
                  rows={6}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                />
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="is_active"
                  checked={formData.is_active}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                />
                <label htmlFor="is_active" className="ml-2 text-sm text-gray-700">
                  Active
                </label>
              </div>

              <div className="flex gap-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition"
                >
                  {editingTemplate ? 'Update Template' : 'Create Template'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false)
                    setEditingTemplate(null)
                    resetForm()
                  }}
                  className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {loading ? (
          <div className="text-center py-8">Loading...</div>
        ) : templates.length === 0 ? (
          <div className="bg-white p-8 rounded-lg shadow text-center">
            <p className="text-gray-500">No templates found. Create your first template!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {templates.map((template) => (
              <div key={template._id} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-semibold text-gray-900">{template.name}</h3>
                      <span className="px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800">
                        {getToolTypeLabel(template.tool_type)}
                      </span>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        template.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {template.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-3">{template.description}</p>
                    <div className="bg-gray-50 p-3 rounded">
                      <p className="text-xs text-gray-500 mb-1">Prompt Template:</p>
                      <p className="text-sm font-mono text-gray-700 line-clamp-2">{template.prompt_template}</p>
                    </div>
                  </div>
                  <div className="flex flex-col gap-2 ml-4">
                    <button
                      onClick={() => handleEdit(template)}
                      className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(template._id!)}
                      className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
