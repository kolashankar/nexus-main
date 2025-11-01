'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'
import { ChevronDown, ChevronRight, X } from 'lucide-react'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

interface MenuItem {
  name: string
  icon: string
  children?: {
    name: string
    href: string
  }[]
}

export function MobileSidebar({ isOpen, onClose }: SidebarProps) {
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
    {
      name: 'Jobs',
      icon: '💼',
      children: [
        { name: 'Browse Jobs', href: '/jobs' },
        { name: 'Freshers Jobs', href: '/jobs?type=freshers' },
        { name: 'Internships', href: '/jobs?type=internships' },
      ]
    },
    {
      name: 'DSA Corner',
      icon: '💻',
      children: [
        { name: 'Dashboard', href: '/dsa' },
        { name: 'Questions', href: '/dsa/questions' },
        { name: 'Topics', href: '/dsa/topics' },
        { name: 'Companies', href: '/dsa/companies' },
        { name: 'Sheets', href: '/dsa/sheets' },
      ]
    },
    {
      name: 'Learning',
      icon: '📚',
      children: [
        { name: 'Articles', href: '/learning' },
        { name: 'Browse by Topic', href: '/learning?view=topics' },
      ]
    },
    {
      name: 'Career Tools',
      icon: '🛠️',
      children: [
        { name: 'Resume Review', href: '/career-tools/resume-review' },
        { name: 'Cover Letter', href: '/career-tools/cover-letter' },
        { name: 'ATS Hack', href: '/career-tools/ats-hack' },
        { name: 'Cold Email', href: '/career-tools/cold-email' },
      ]
    },
    {
      name: 'Roadmaps',
      icon: '🗺️',
      children: [
        { name: 'Browse Roadmaps', href: '/roadmaps' },
        { name: 'Trending', href: '/roadmaps?sort=trending' },
      ]
    },
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
          fixed top-0 left-0 z-50 h-screen w-80 bg-white shadow-lg transform transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b">
            <h2 className="text-xl font-bold text-blue-600">CareerGuide</h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 p-2"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto p-4">
            <ul className="space-y-2">
              {menuItems.map((item) => {
                const isExpanded = expandedItems.includes(item.name)
                
                return (
                  <li key={item.name}>
                    <button
                      onClick={() => toggleExpand(item.name)}
                      className="w-full flex items-center justify-between px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
                    >
                      <div className="flex items-center">
                        <span className="text-2xl mr-3">{item.icon}</span>
                        <span className="font-medium">{item.name}</span>
                      </div>
                      {isExpanded ? (
                        <ChevronDown className="w-5 h-5" />
                      ) : (
                        <ChevronRight className="w-5 h-5" />
                      )}
                    </button>
                    
                    {/* Dropdown Items */}
                    {isExpanded && item.children && (
                      <ul className="mt-2 ml-6 space-y-1">
                        {item.children.map((child) => {
                          const isActive = pathname === child.href
                          return (
                            <li key={child.href}>
                              <Link
                                href={child.href}
                                onClick={onClose}
                                className={`
                                  block px-4 py-2 rounded-lg text-sm transition-colors
                                  ${isActive
                                    ? 'bg-blue-50 text-blue-600 font-medium'
                                    : 'text-gray-600 hover:bg-gray-50'
                                  }
                                `}
                              >
                                {child.name}
                              </Link>
                            </li>
                          )
                        })}
                      </ul>
                    )}
                  </li>
                )
              })}
            </ul>
          </nav>

          {/* Footer */}
          <div className="p-4 border-t">
            <div className="text-sm text-gray-500">
              © 2024 CareerGuide. All rights reserved.
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
