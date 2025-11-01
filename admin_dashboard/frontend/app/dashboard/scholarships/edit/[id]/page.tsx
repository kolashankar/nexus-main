'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernScholarshipForm from '@/components/ui/forms/scholarship/ModernScholarshipForm'
import { Award, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function EditScholarshipPage() {
  const params = useParams()
  const [scholarship, setScholarship] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchScholarship = async () => {
      try {
        const response = await fetch(`/api/admin/scholarships/${params.id}`)
        const data = await response.json()
        setScholarship(data)
      } catch (error) {
        console.error('Error fetching scholarship:', error)
        alert('Failed to load scholarship')
      } finally {
        setLoading(false)
      }
    }

    if (params.id) {
      fetchScholarship()
    }
  }, [params.id])

  if (loading) {
    return (
      <ModernDashboardLayout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600"></div>
        </div>
      </ModernDashboardLayout>
    )
  }

  return (
    <ModernDashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <Link 
              href="/dashboard/scholarships/list"
              className="inline-flex items-center text-sm text-slate-600 hover:text-slate-900 mb-2 transition-colors"
            >
              <ArrowLeft className="w-4 h-4 mr-1" />
              Back to Scholarships
            </Link>
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-gradient-to-br from-orange-500 to-amber-600 rounded-xl shadow-lg">
                <Award className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900">Edit Scholarship</h1>
                <p className="text-slate-600 mt-1">Update scholarship details</p>
              </div>
            </div>
          </div>
        </div>
        {scholarship && <ModernScholarshipForm initialData={scholarship} isEditing />}
      </div>
    </ModernDashboardLayout>
  )
}
