'use client'

import Link from 'next/link'

export default function AdvancedFeatures() {
  const features = [
    { name: 'Email Templates', path: '/dashboard/advanced/email-templates', icon: '📧', description: 'Manage email templates' },
    { name: 'SMS Templates', path: '/dashboard/advanced/sms-templates', icon: '📱', description: 'Manage SMS templates' },
    { name: 'Automation Rules', path: '/dashboard/advanced/automation', icon: '⚙️', description: 'Set up automation workflows' },
    { name: 'Scheduled Tasks', path: '/dashboard/advanced/scheduled-tasks', icon: '⏰', description: 'Manage scheduled tasks' },
    { name: 'System Health', path: '/dashboard/advanced/system-health', icon: '📊', description: 'Monitor system health' },
    { name: 'Database Backup', path: '/dashboard/advanced/database-backup', icon: '💾', description: 'Backup and restore database' },
    { name: 'Audit Trails', path: '/dashboard/advanced/audit-trails', icon: '📝', description: 'View audit logs' },
  ]

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Advanced Features</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((feature) => (
          <Link
            key={feature.path}
            href={feature.path}
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition"
          >
            <div className="text-5xl mb-4">{feature.icon}</div>
            <h3 className="text-xl font-bold mb-2">{feature.name}</h3>
            <p className="text-gray-600 text-sm">{feature.description}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
