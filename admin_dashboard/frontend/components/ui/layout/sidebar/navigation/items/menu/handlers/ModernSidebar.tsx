'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useState } from 'react'
import { 
  ChevronDown, 
  ChevronRight, 
  LayoutDashboard, 
  BarChart3, 
  Briefcase, 
  GraduationCap, 
  Award, 
  BookOpen, 
  Code2, 
  Map, 
  Wrench, 
  Bell, 
  CheckCircle, 
  Users, 
  UserCog, 
  Package, 
  Settings, 
  LogOut,
  FileText,
  Building2,
  ListTree,
  Layers
} from 'lucide-react'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

interface SubMenuItem {
  name: string
  path: string
  icon?: any
}

interface MenuItem {
  name: string
  path?: string
  icon: any
  badge?: string
  subItems?: SubMenuItem[]
  category?: string
}

export default function ModernSidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname()
  const router = useRouter()
  const [expandedItems, setExpandedItems] = useState<string[]>(['DSA Corner', 'Roadmaps'])

  const toggleExpand = (itemName: string) => {
    setExpandedItems(prev => 
      prev.includes(itemName) 
        ? prev.filter(name => name !== itemName)
        : [...prev, itemName]
    )
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  const menuItems: MenuItem[] = [
    { 
      name: 'Dashboard', 
      path: '/dashboard', 
      icon: LayoutDashboard,
      category: 'Main'
    },
    { 
      name: 'Analytics', 
      path: '/dashboard/analytics', 
      icon: BarChart3,
      category: 'Main'
    },
    
    // Opportunities Section
    { 
      name: 'Jobs', 
      icon: Briefcase,
      category: 'Opportunities',
      subItems: [
        { name: 'All Jobs', path: '/dashboard/jobs/list', icon: Briefcase },
        { name: 'Create Job', path: '/dashboard/jobs/create', icon: FileText },
        { name: 'Create with AI', path: '/dashboard/jobs/create-ai', icon: Code2 },
      ]
    },
    { 
      name: 'Internships', 
      icon: GraduationCap,
      category: 'Opportunities',
      subItems: [
        { name: 'All Internships', path: '/dashboard/internships/list', icon: GraduationCap },
        { name: 'Create Internship', path: '/dashboard/internships/create', icon: FileText },
      ]
    },
    { 
      name: 'Scholarships', 
      icon: Award,
      category: 'Opportunities',
      subItems: [
        { name: 'All Scholarships', path: '/dashboard/scholarships/list', icon: Award },
        { name: 'Create Scholarship', path: '/dashboard/scholarships/create', icon: FileText },
      ]
    },
    
    // Content Section
    { 
      name: 'Learning', 
      icon: BookOpen,
      category: 'Content',
      subItems: [
        { name: 'All Articles', path: '/dashboard/learning/articles/list', icon: BookOpen },
        { name: 'Create Article', path: '/dashboard/learning/articles/create', icon: FileText },
        { name: 'Categories', path: '/dashboard/learning/categories', icon: Layers },
      ]
    },
    { 
      name: 'DSA Corner', 
      icon: Code2,
      category: 'Content',
      subItems: [
        { name: 'Dashboard', path: '/dashboard/dsa/dashboard', icon: LayoutDashboard },
        { name: 'Questions', path: '/dashboard/dsa/questions/list', icon: Code2 },
        { name: 'Create Question', path: '/dashboard/dsa/questions/create', icon: FileText },
        { name: 'Topics', path: '/dashboard/dsa/topics/list', icon: ListTree },
        { name: 'Sheets', path: '/dashboard/dsa/sheets/list', icon: Layers },
        { name: 'Companies', path: '/dashboard/dsa/companies/list', icon: Building2 },
      ]
    },
    { 
      name: 'Roadmaps', 
      icon: Map,
      category: 'Content',
      subItems: [
        { name: 'All Roadmaps', path: '/dashboard/roadmaps/list', icon: Map },
        { name: 'Create Roadmap', path: '/dashboard/roadmaps/create', icon: FileText },
        { name: 'Create with AI', path: '/dashboard/roadmaps/create-ai', icon: Code2 },
      ]
    },
    
    // Tools & Management
    { 
      name: 'Career Tools', 
      path: '/dashboard/career-tools/templates', 
      icon: Wrench,
      category: 'Tools'
    },
    { 
      name: 'Notifications', 
      path: '/dashboard/notifications/list', 
      icon: Bell,
      badge: '3',
      category: 'Tools'
    },
    { 
      name: 'Content Approval', 
      path: '/dashboard/content-approval', 
      icon: CheckCircle,
      category: 'Tools'
    },
    { 
      name: 'Bulk Operations', 
      path: '/dashboard/bulk-operations', 
      icon: Package,
      category: 'Tools'
    },
    
    // Administration
    { 
      name: 'Users', 
      path: '/dashboard/users/list', 
      icon: Users,
      category: 'Administration'
    },
    { 
      name: 'Admins', 
      path: '/dashboard/admins/list', 
      icon: UserCog,
      category: 'Administration'
    },
    { 
      name: 'Settings', 
      path: '/dashboard/settings', 
      icon: Settings,
      category: 'Administration'
    },
  ]

  // Group items by category
  const groupedItems = menuItems.reduce((acc, item) => {
    const category = item.category || 'Other'
    if (!acc[category]) {
      acc[category] = []
    }
    acc[category].push(item)
    return acc
  }, {} as Record<string, MenuItem[]>)

  const categoryOrder = ['Main', 'Opportunities', 'Content', 'Tools', 'Administration']

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
          fixed top-0 left-0 z-50 h-screen w-72 bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 shadow-2xl transform transition-transform duration-300 ease-in-out
          lg:translate-x-0 lg:static lg:z-auto
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-slate-700">
            <div>
              <h2 className="text-2xl font-bold text-white">CareerGuide</h2>
              <p className="text-xs text-slate-400 mt-1">Admin Dashboard</p>
            </div>
            <button
              onClick={onClose}
              className="lg:hidden text-slate-400 hover:text-white transition-colors"
            >
              ✕
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-slate-800">
            {categoryOrder.map((category) => {
              const items = groupedItems[category]
              if (!items || items.length === 0) return null

              return (
                <div key={category} className="mb-6">
                  <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 px-3">
                    {category}
                  </h3>
                  <ul className="space-y-1">
                    {items.map((item) => {
                      const isExpanded = expandedItems.includes(item.name)
                      const hasSubItems = item.subItems && item.subItems.length > 0
                      const isActive = pathname === item.path || (hasSubItems && item.subItems.some(sub => pathname === sub.path))
                      const Icon = item.icon
                      
                      return (
                        <li key={item.name}>
                          {hasSubItems ? (
                            <>
                              <button
                                onClick={() => toggleExpand(item.name)}
                                className={`
                                  w-full flex items-center px-3 py-2.5 rounded-lg transition-all duration-200
                                  ${isActive
                                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/50'
                                    : 'text-slate-300 hover:bg-slate-700/50 hover:text-white'
                                  }
                                `}
                              >
                                <Icon className="w-5 h-5 mr-3" />
                                <span className="font-medium text-sm flex-1 text-left">{item.name}</span>
                                {item.badge && (
                                  <span className="px-2 py-0.5 text-xs font-bold bg-red-500 text-white rounded-full mr-2">
                                    {item.badge}
                                  </span>
                                )}
                                {isExpanded ? (
                                  <ChevronDown className="w-4 h-4" />
                                ) : (
                                  <ChevronRight className="w-4 h-4" />
                                )}
                              </button>
                              {isExpanded && (
                                <ul className="ml-6 mt-1 space-y-1 border-l-2 border-slate-700 pl-3">
                                  {item.subItems.map((subItem) => {
                                    const isSubActive = pathname === subItem.path
                                    const SubIcon = subItem.icon
                                    return (
                                      <li key={subItem.path}>
                                        <Link
                                          href={subItem.path}
                                          className={`
                                            flex items-center px-3 py-2 rounded-lg transition-all duration-200 text-sm
                                            ${isSubActive
                                              ? 'bg-blue-500/20 text-blue-400 font-medium border-l-2 border-blue-400 -ml-[14px] pl-[14px]'
                                              : 'text-slate-400 hover:bg-slate-700/30 hover:text-slate-200'
                                            }
                                          `}
                                          onClick={() => onClose()}
                                        >
                                          {SubIcon && <SubIcon className="w-4 h-4 mr-2" />}
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
                                flex items-center px-3 py-2.5 rounded-lg transition-all duration-200
                                ${isActive
                                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/50'
                                  : 'text-slate-300 hover:bg-slate-700/50 hover:text-white'
                                }
                              `}
                              onClick={() => onClose()}
                            >
                              <Icon className="w-5 h-5 mr-3" />
                              <span className="font-medium text-sm flex-1">{item.name}</span>
                              {item.badge && (
                                <span className="px-2 py-0.5 text-xs font-bold bg-red-500 text-white rounded-full">
                                  {item.badge}
                                </span>
                              )}
                            </Link>
                          )}
                        </li>
                      )
                    })}
                  </ul>
                </div>
              )
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-slate-700">
            <button
              onClick={handleLogout}
              className="w-full flex items-center px-3 py-2.5 rounded-lg text-slate-300 hover:bg-red-600 hover:text-white transition-all duration-200"
            >
              <LogOut className="w-5 h-5 mr-3" />
              <span className="font-medium text-sm">Logout</span>
            </button>
            <div className="text-xs text-slate-500 mt-3 text-center">
              v2.0.0 • Admin Panel
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
