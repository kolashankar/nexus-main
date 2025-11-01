'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import DashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/DashboardLayout'
import ScholarshipForm from '@/components/ui/forms/scholarship/create/fields/input/validation/ScholarshipForm'
import { scholarshipsApi, type Scholarship } from '@/lib/api/client/config/interceptors/auth/token/scholarshipsApi'

export default function EditScholarshipPage() {
  const router = useRouter()
  const params = useParams()
  const [scholarship, setScholarship] = useState<Scholarship | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchScholarship = async () => {
      try {
        if (!params.id || typeof params.id !== 'string') {
          setError('Invalid scholarship ID')
          setLoading(false)
          return
        }

        const scholarshipData = await scholarshipsApi.getById(params.id)
        setScholarship(scholarshipData)
      } catch (err: any) {
        console.error('Error fetching scholarship:', err)
        setError(err.response?.data?.detail || 'Failed to load scholarship')
      } finally {
        setLoading(false)
      }
    }

    fetchScholarship()
  }, [params.id])

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading scholarship details...</p>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  if (error || !scholarship) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <div className="text-red-500 text-xl mb-4">❌ {error || 'Scholarship not found'}</div>
          <button
            onClick={() => router.push('/dashboard/scholarships/list')}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Back to Scholarships List
          </button>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Edit Scholarship</h1>
          <p className="text-gray-600 mt-1">Update scholarship listing details</p>
        </div>
        <ScholarshipForm initialData={scholarship} isEditing={true} />
      </div>
    </DashboardLayout>
  )
}
