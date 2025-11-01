'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { settingsApi } from '@/lib/api/client/config/interceptors/auth/token/settingsApi'
import toast from 'react-hot-toast'

export default function GeneralSettings() {
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [formData, setFormData] = useState({
    site_name: '',
    site_description: '',
    contact_email: '',
    support_email: '',
    maintenance_mode: false,
  })

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      setLoading(true)
      const response = await settingsApi.getGeneral()
      setFormData(response.data)
    } catch (error: any) {
      console.error('Failed to fetch settings', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      setSaving(true)
      await settingsApi.updateGeneral(formData)
      toast.success('Settings updated successfully')
    } catch (error: any) {
      toast.error('Failed to update settings')
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return <div className="p-6 text-center">Loading settings...</div>
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Settings & Configuration</h1>

      {/* Quick Links */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Link href="/dashboard/settings/email" className="bg-white p-4 rounded-lg shadow hover:shadow-lg text-center">
          <div className="text-3xl mb-2">📧</div>
          <div className="font-medium">Email Config</div>
        </Link>
        <Link href="/dashboard/settings/api-keys" className="bg-white p-4 rounded-lg shadow hover:shadow-lg text-center">
          <div className="text-3xl mb-2">🔑</div>
          <div className="font-medium">API Keys</div>
        </Link>
        <Link href="/dashboard/settings/theme" className="bg-white p-4 rounded-lg shadow hover:shadow-lg text-center">
          <div className="text-3xl mb-2">🎨</div>
          <div className="font-medium">Theme</div>
        </Link>
        <Link href="/dashboard/settings/backup" className="bg-white p-4 rounded-lg shadow hover:shadow-lg text-center">
          <div className="text-3xl mb-2">💾</div>
          <div className="font-medium">Backup</div>
        </Link>
      </div>

      {/* General Settings Form */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">General Settings</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Site Name *</label>
            <input
              type="text"
              required
              value={formData.site_name}
              onChange={(e) => setFormData({ ...formData, site_name: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Site Description</label>
            <textarea
              value={formData.site_description}
              onChange={(e) => setFormData({ ...formData, site_description: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg"
              rows={3}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Contact Email</label>
              <input
                type="email"
                value={formData.contact_email}
                onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Support Email</label>
              <input
                type="email"
                value={formData.support_email}
                onChange={(e) => setFormData({ ...formData, support_email: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg"
              />
            </div>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              checked={formData.maintenance_mode}
              onChange={(e) => setFormData({ ...formData, maintenance_mode: e.target.checked })}
              className="mr-2"
            />
            <label className="text-sm font-medium">Enable Maintenance Mode</label>
          </div>

          <button
            type="submit"
            disabled={saving}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </form>
      </div>
    </div>
  )
}
