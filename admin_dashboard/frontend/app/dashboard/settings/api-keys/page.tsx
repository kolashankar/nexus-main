'use client'

import { useState, useEffect } from 'react'
import { settingsApi } from '@/lib/api/client/config/interceptors/auth/token/settingsApi'
import toast from 'react-hot-toast'

export default function APIKeysManagement() {
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [showKeys, setShowKeys] = useState<{[key: string]: boolean}>({})
  const [formData, setFormData] = useState({
    gemini_api_key: '',
    openai_api_key: '',
    stripe_api_key: '',
    sendgrid_api_key: '',
  })

  useEffect(() => {
    fetchAPIKeys()
  }, [])

  const fetchAPIKeys = async () => {
    try {
      setLoading(true)
      const response = await settingsApi.getApiKeys()
      setFormData(response.data)
    } catch (error: any) {
      console.error('Failed to fetch API keys', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      setSaving(true)
      await settingsApi.updateApiKeys(formData)
      toast.success('API Keys updated successfully')
    } catch (error: any) {
      toast.error('Failed to update API keys')
    } finally {
      setSaving(false)
    }
  }

  const toggleShowKey = (key: string) => {
    setShowKeys(prev => ({ ...prev, [key]: !prev[key] }))
  }

  const maskKey = (key: string, showKey: boolean) => {
    if (!key) return ''
    if (showKey) return key
    return key.substring(0, 8) + '*'.repeat(Math.max(key.length - 8, 10))
  }

  if (loading) {
    return <div className="p-6 text-center">Loading...</div>
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">API Keys Management</h1>

      <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg mb-6">
        <p className="text-sm text-yellow-800">
          <strong>Security Warning:</strong> Keep your API keys secure. Never share them publicly or commit them to version control.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow space-y-6">
        <div>
          <label className="block text-sm font-medium mb-2">Gemini API Key</label>
          <div className="flex gap-2">
            <input
              type={showKeys['gemini'] ? 'text' : 'password'}
              value={formData.gemini_api_key}
              onChange={(e) => setFormData({ ...formData, gemini_api_key: e.target.value })}
              placeholder="AIza..." 
              className="flex-1 px-4 py-2 border rounded-lg"
            />
            <button
              type="button"
              onClick={() => toggleShowKey('gemini')}
              className="px-4 py-2 border rounded-lg hover:bg-gray-50"
            >
              {showKeys['gemini'] ? '👁️' : '🚫'}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">Used for AI content generation</p>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">OpenAI API Key</label>
          <div className="flex gap-2">
            <input
              type={showKeys['openai'] ? 'text' : 'password'}
              value={formData.openai_api_key}
              onChange={(e) => setFormData({ ...formData, openai_api_key: e.target.value })}
              placeholder="sk-..."
              className="flex-1 px-4 py-2 border rounded-lg"
            />
            <button
              type="button"
              onClick={() => toggleShowKey('openai')}
              className="px-4 py-2 border rounded-lg hover:bg-gray-50"
            >
              {showKeys['openai'] ? '👁️' : '🚫'}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">Alternative AI provider</p>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Stripe API Key</label>
          <div className="flex gap-2">
            <input
              type={showKeys['stripe'] ? 'text' : 'password'}
              value={formData.stripe_api_key}
              onChange={(e) => setFormData({ ...formData, stripe_api_key: e.target.value })}
              placeholder="sk_..."
              className="flex-1 px-4 py-2 border rounded-lg"
            />
            <button
              type="button"
              onClick={() => toggleShowKey('stripe')}
              className="px-4 py-2 border rounded-lg hover:bg-gray-50"
            >
              {showKeys['stripe'] ? '👁️' : '🚫'}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">For payment processing</p>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">SendGrid API Key</label>
          <div className="flex gap-2">
            <input
              type={showKeys['sendgrid'] ? 'text' : 'password'}
              value={formData.sendgrid_api_key}
              onChange={(e) => setFormData({ ...formData, sendgrid_api_key: e.target.value })}
              placeholder="SG..."
              className="flex-1 px-4 py-2 border rounded-lg"
            />
            <button
              type="button"
              onClick={() => toggleShowKey('sendgrid')}
              className="px-4 py-2 border rounded-lg hover:bg-gray-50"
            >
              {showKeys['sendgrid'] ? '👁️' : '🚫'}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">For email delivery</p>
        </div>

        <button
          type="submit"
          disabled={saving}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? 'Saving...' : 'Save API Keys'}
        </button>
      </form>
    </div>
  )
}
