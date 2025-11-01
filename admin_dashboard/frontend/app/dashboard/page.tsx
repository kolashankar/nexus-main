'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import apiClient from '@/lib/api/client/config/interceptors/auth/token/apiClient'

interface DashboardStats {
  jobs_count: number
  internships_count: number
  scholarships_count: number
  articles_count: number
  users_count: number
  dsa_questions_count: number
  dsa_topics_count: number
  roadmaps_count: number
}

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [stats, setStats] = useState<DashboardStats>({
    jobs_count: 0,
    internships_count: 0,
    scholarships_count: 0,
    articles_count: 0,
    users_count: 0,
    dsa_questions_count: 0,
    dsa_topics_count: 0,
    roadmaps_count: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    
    if (!token || !userData) {
      router.push('/login')
      return
    }
    
    setUser(JSON.parse(userData))
    fetchDashboardStats()
  }, [router])

  const fetchDashboardStats = async () => {
    try {
      setLoading(true)
      
      // Fetch counts from various endpoints
      const [
        jobsRes,
        internshipsRes,
        scholarshipsRes,
        articlesRes,
        dsaQuestionsRes,
        dsaTopicsRes,
        roadmapsRes,
      ] = await Promise.all([
        apiClient.get('/admin/jobs'),
        apiClient.get('/admin/internships'),
        apiClient.get('/admin/scholarships'),
        apiClient.get('/admin/articles'),
        apiClient.get('/admin/dsa/questions'),
        apiClient.get('/admin/dsa/topics'),
        apiClient.get('/admin/roadmaps'),
      ])

      setStats({
        jobs_count: jobsRes.data?.data?.length || 0,
        internships_count: internshipsRes.data?.data?.length || 0,
        scholarships_count: scholarshipsRes.data?.data?.length || 0,
        articles_count: articlesRes.data?.data?.length || 0,
        users_count: 0, // Will be fetched from analytics
        dsa_questions_count: dsaQuestionsRes.data?.data?.length || 0,
        dsa_topics_count: dsaTopicsRes.data?.data?.length || 0,
        roadmaps_count: roadmapsRes.data?.data?.length || 0,
      })
    } catch (error) {
      console.error('Error fetching dashboard stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const quickLinks = [
    { title: 'Analytics', href: '/dashboard/analytics', icon: '📊', color: 'bg-blue-100 text-blue-600' },
    { title: 'Jobs', href: '/dashboard/jobs/list', icon: '💼', color: 'bg-green-100 text-green-600' },
    { title: 'Internships', href: '/dashboard/internships/list', icon: '🎓', color: 'bg-purple-100 text-purple-600' },
    { title: 'Scholarships', href: '/dashboard/scholarships/list', icon: '🏆', color: 'bg-yellow-100 text-yellow-600' },
    { title: 'Learning Articles', href: '/dashboard/learning/articles/list', icon: '📚', color: 'bg-indigo-100 text-indigo-600' },
    { title: 'DSA Corner', href: '/dashboard/dsa/dashboard', icon: '💻', color: 'bg-pink-100 text-pink-600' },
    { title: 'Roadmaps', href: '/dashboard/roadmaps/list', icon: '🗺️', color: 'bg-teal-100 text-teal-600' },
    { title: 'Career Tools', href: '/dashboard/career-tools/templates', icon: '🛠️', color: 'bg-orange-100 text-orange-600' },
  ]

  const managementLinks = [
    { title: 'Notifications', href: '/dashboard/notifications/list', icon: '🔔' },
    { title: 'Content Approval', href: '/dashboard/content-approval', icon: '✅' },
    { title: 'Users', href: '/dashboard/users/list', icon: '👥' },
    { title: 'Admins', href: '/dashboard/admins/list', icon: '👨‍💼' },
    { title: 'Bulk Operations', href: '/dashboard/bulk-operations', icon: '📦' },
    { title: 'Settings', href: '/dashboard/settings', icon: '⚙️' },
  ]

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6">
      {/* Welcome Section */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back, {user.name || user.email}! 👋
        </h1>
        <p className="text-gray-600">
          Here's your admin dashboard overview. Quick access to all major sections.
        </p>
      </div>

      {/* Quick Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl">💼</span>
            <span className="text-2xl font-bold text-blue-600">
              {loading ? '...' : stats.jobs_count}
            </span>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-1">Jobs</h3>
          <p className="text-sm text-gray-600">Total job listings</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl">🎓</span>
            <span className="text-2xl font-bold text-purple-600">
              {loading ? '...' : stats.internships_count}
            </span>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-1">Internships</h3>
          <p className="text-sm text-gray-600">Total internship listings</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl">📚</span>
            <span className="text-2xl font-bold text-green-600">
              {loading ? '...' : stats.articles_count}
            </span>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-1">Articles</h3>
          <p className="text-sm text-gray-600">Learning content published</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl">💻</span>
            <span className="text-2xl font-bold text-pink-600">
              {loading ? '...' : stats.dsa_questions_count}
            </span>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-1">DSA Questions</h3>
          <p className="text-sm text-gray-600">Total DSA problems</p>
        </div>
      </div>

      {/* Additional Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl">🏆</span>
            <span className="text-2xl font-bold text-yellow-600">
              {loading ? '...' : stats.scholarships_count}
            </span>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-1">Scholarships</h3>
          <p className="text-sm text-gray-600">Available scholarships</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl">🗺️</span>
            <span className="text-2xl font-bold text-teal-600">
              {loading ? '...' : stats.roadmaps_count}
            </span>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-1">Roadmaps</h3>
          <p className="text-sm text-gray-600">Career roadmaps created</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl">🏷️</span>
            <span className="text-2xl font-bold text-indigo-600">
              {loading ? '...' : stats.dsa_topics_count}
            </span>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-1">DSA Topics</h3>
          <p className="text-sm text-gray-600">DSA topics available</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <span className="text-3xl">👥</span>
            <span className="text-2xl font-bold text-orange-600">
              {loading ? '...' : stats.users_count}
            </span>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-1">Users</h3>
          <p className="text-sm text-gray-600">Registered app users</p>
        </div>
      </div>

      {/* Quick Links Section */}
      <div className="mb-8">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Content Management</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="bg-white rounded-lg shadow-sm p-6 border border-gray-100 hover:shadow-md transition-shadow group"
            >
              <div className={`w-12 h-12 rounded-lg ${link.color} flex items-center justify-center mb-4 text-2xl`}>
                {link.icon}
              </div>
              <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                {link.title}
              </h3>
            </Link>
          ))}
        </div>
      </div>

      {/* Management Links */}
      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-4">System Management</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {managementLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="bg-white rounded-lg shadow-sm p-6 border border-gray-100 hover:shadow-md transition-shadow group"
            >
              <div className="flex items-center">
                <span className="text-3xl mr-4">{link.icon}</span>
                <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                  {link.title}
                </h3>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
