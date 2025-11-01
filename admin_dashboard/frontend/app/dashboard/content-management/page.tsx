'use client'

import Link from 'next/link'

export default function ContentManagement() {
  const modules = [
    { name: 'Media Library', path: '/dashboard/content-management/media', icon: '🖼️', description: 'Manage images, videos, and files' },
    { name: 'File Manager', path: '/dashboard/content-management/files', icon: '📁', description: 'Organize and manage uploaded files' },
    { name: 'Tags Management', path: '/dashboard/content-management/tags', icon: '🏷️', description: 'Create and manage content tags' },
    { name: 'Categories Management', path: '/dashboard/content-management/categories', icon: '📋', description: 'Organize content by categories' },
    { name: 'SEO Settings', path: '/dashboard/content-management/seo', icon: '🔍', description: 'Manage SEO for content' },
  ]

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Content Management</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {modules.map((module) => (
          <Link
            key={module.path}
            href={module.path}
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition"
          >
            <div className="text-5xl mb-4">{module.icon}</div>
            <h3 className="text-xl font-bold mb-2">{module.name}</h3>
            <p className="text-gray-600 text-sm">{module.description}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
