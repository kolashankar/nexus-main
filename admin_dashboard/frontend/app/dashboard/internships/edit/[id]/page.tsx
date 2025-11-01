'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernInternshipForm from '@/components/ui/forms/internship/ModernInternshipForm'
import { GraduationCap, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function EditInternshipPage() {
  const params = useParams()
  const [internship, setInternship] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchInternship = async () => {
      try {
        const response = await fetch(`/api/admin/internships/${params.id}`)
        const data = await response.json()
        setInternship(data)
      } catch (error) {
        console.error('Error fetching internship:', error)
        alert('Failed to load internship')
      } finally {
        setLoading(false)
      }
    }

    if (params.id) {
      fetchInternship()
    }
  }, [params.id])

  if (loading) {
    return (
      <ModernDashboardLayout>
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
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
              href="/dashboard/internships/list"
              className="inline-flex items-center text-sm text-slate-600 hover:text-slate-900 mb-2 transition-colors"
            >
              <ArrowLeft className="w-4 h-4 mr-1" />
              Back to Internships
            </Link>
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl shadow-lg">
                <GraduationCap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900">Edit Internship</h1>
                <p className="text-slate-600 mt-1">Update internship details</p>
              </div>
            </div>
          </div>
        </div>
        {internship && <ModernInternshipForm initialData={internship} isEditing />}
      </div>
    </ModernDashboardLayout>
  )
}
