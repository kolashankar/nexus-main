'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import DashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/DashboardLayout'
import InternshipForm from '@/components/ui/forms/internship/create/fields/input/validation/InternshipForm'
import { internshipsApi, type Internship } from '@/lib/api/client/config/interceptors/auth/token/internshipsApi'

export default function EditInternshipPage() {
  const router = useRouter()
  const params = useParams()
  const [internship, setInternship] = useState<Internship | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchInternship = async () => {
      try {
        if (!params.id || typeof params.id !== 'string') {
          setError('Invalid internship ID')
          setLoading(false)
          return
        }

        const internshipData = await internshipsApi.getById(params.id)
        setInternship(internshipData)
      } catch (err: any) {
        console.error('Error fetching internship:', err)
        setError(err.response?.data?.detail || 'Failed to load internship')
      } finally {
        setLoading(false)
      }
    }

    fetchInternship()
  }, [params.id])

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading internship details...</p>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  if (error || !internship) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <div className="text-red-500 text-xl mb-4">❌ {error || 'Internship not found'}</div>
          <button
            onClick={() => router.push('/dashboard/internships/list')}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            Back to Internships List
          </button>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Edit Internship</h1>
          <p className="text-gray-600 mt-1">Update internship listing details</p>
        </div>
        <InternshipForm initialData={internship} isEditing={true} />
      </div>
    </DashboardLayout>
  )
}
