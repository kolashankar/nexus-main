'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

interface SubMenuItem {
  name: string
  path: string
}

interface MenuItem {
  name: string
  path?: string
  icon: string
  disabled?: boolean
  subItems?: SubMenuItem[]
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname()
  const [expandedItems, setExpandedItems] = useState<string[]>([])

  const toggleExpand = (itemName: string) => {
    setExpandedItems(prev => 
      prev.includes(itemName) 
        ? prev.filter(name => name !== itemName)
        : [...prev, itemName]
    )
  }

  const menuItems: MenuItem[] = [
    { name: 'Dashboard', path: '/dashboard', icon: '🏠' },
    { name: 'Analytics', path: '/dashboard/analytics', icon: '📊' },
    { name: 'Jobs', path: '/dashboard/jobs/list', icon: '💼' },
    { name: 'Internships', path: '/dashboard/internships/list', icon: '🎓' },
    { name: 'Scholarships', path: '/dashboard/scholarships/list', icon: '🏆' },
    { name: 'Learning', path: '/dashboard/learning/articles/list', icon: '📚' },
    { 
      name: 'DSA Corner', 
      icon: '💻',
      subItems: [
        { name: 'Dashboard', path: '/dashboard/dsa/dashboard' },
        { name: 'Questions', path: '/dashboard/dsa/questions/list' },
        { name: 'Topics', path: '/dashboard/dsa/topics/list' },
        { name: 'Sheets', path: '/dashboard/dsa/sheets/list' },
        { name: 'Companies', path: '/dashboard/dsa/companies/list' },
      ]
    },
    { 
      name: 'Roadmaps', 
      icon: '🗺️',
      subItems: [
        { name: 'All Roadmaps', path: '/dashboard/roadmaps/list' },
        { name: 'Create Roadmap', path: '/dashboard/roadmaps/create' },
        { name: 'Create with AI', path: '/dashboard/roadmaps/create-ai' },
      ]
    },
    { name: 'Career Tools', path: '/dashboard/career-tools/templates', icon: '🛠️' },
    { name: 'Notifications', path: '/dashboard/notifications/list', icon: '🔔' },
    { name: 'Content Approval', path: '/dashboard/content-approval', icon: '✅' },
    { name: 'Users', path: '/dashboard/users/list', icon: '👥' },
    { name: 'Admins', path: '/dashboard/admins/list', icon: '👨‍💼' },
    { name: 'Bulk Operations', path: '/dashboard/bulk-operations', icon: '📦' },
    { name: 'Settings', path: '/dashboard/settings', icon: '⚙️' },
  ]

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 z-50 h-screen w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out
          lg:translate-x-0 lg:static lg:z-auto
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b">
            <h2 className="text-xl font-bold text-gray-800">CareerGuide</h2>
            <button
              onClick={onClose}
              className="lg:hidden text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto p-4">
            <ul className="space-y-2">
              {menuItems.map((item, index) => {
                const isExpanded = expandedItems.includes(item.name)
                const hasSubItems = item.subItems && item.subItems.length > 0
                const isActive = pathname === item.path || (hasSubItems && item.subItems.some(sub => pathname === sub.path))
                const isDisabled = item.disabled
                
                return (
                  <li key={item.name + index}>
                    {isDisabled ? (
                      <div
                        className={`
                          flex items-center px-4 py-3 rounded-lg opacity-50 cursor-not-allowed
                          text-gray-400
                        `}
                      >
                        <span className="text-2xl mr-3">{item.icon}</span>
                        <span className="font-medium">{item.name}</span>
                        <span className="ml-auto text-xs">(Coming Soon)</span>
                      </div>
                    ) : hasSubItems ? (
                      <>
                        <button
                          onClick={() => toggleExpand(item.name)}
                          className={`
                            w-full flex items-center px-4 py-3 rounded-lg transition-colors
                            ${isActive
                              ? 'bg-blue-500 text-white'
                              : 'text-gray-700 hover:bg-gray-100'
                            }
                          `}
                        >
                          <span className="text-2xl mr-3">{item.icon}</span>
                          <span className="font-medium">{item.name}</span>
                          <span className="ml-auto">
                            {isExpanded ? (
                              <ChevronDown className="w-4 h-4" />
                            ) : (
                              <ChevronRight className="w-4 h-4" />
                            )}
                          </span>
                        </button>
                        {isExpanded && (
                          <ul className="ml-8 mt-2 space-y-1">
                            {item.subItems.map((subItem) => {
                              const isSubActive = pathname === subItem.path
                              return (
                                <li key={subItem.path}>
                                  <Link
                                    href={subItem.path}
                                    className={`
                                      flex items-center px-4 py-2 rounded-lg transition-colors text-sm
                                      ${isSubActive
                                        ? 'bg-blue-100 text-blue-600 font-medium'
                                        : 'text-gray-600 hover:bg-gray-50'
                                      }
                                    `}
                                    onClick={() => onClose()}
                                  >
                                    {subItem.name}
                                  </Link>
                                </li>
                              )
                            })}
                          </ul>
                        )}
                      </>
                    ) : (
                      <Link
                        href={item.path!}
                        className={`
                          flex items-center px-4 py-3 rounded-lg transition-colors
                          ${isActive
                            ? 'bg-blue-500 text-white'
                            : 'text-gray-700 hover:bg-gray-100'
                          }
                        `}
                        onClick={() => onClose()}
                      >
                        <span className="text-2xl mr-3">{item.icon}</span>
                        <span className="font-medium">{item.name}</span>
                      </Link>
                    )}
                  </li>
                )
              })}
            </ul>
          </nav>

          {/* Footer */}
          <div className="p-4 border-t">
            <div className="text-sm text-gray-500">
              Admin Dashboard v1.0
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
