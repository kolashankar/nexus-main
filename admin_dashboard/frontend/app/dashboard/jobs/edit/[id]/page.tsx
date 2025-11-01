'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernJobForm from '@/components/ui/forms/job/create/fields/input/validation/ModernJobForm'
import { jobsApi, type Job } from '@/lib/api/client/config/interceptors/auth/token/jobsApi'
import { Briefcase, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function EditJobPage() {
  const router = useRouter()
  const params = useParams()
  const [job, setJob] = useState<Job | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchJob = async () => {
      try {
        if (!params.id || typeof params.id !== 'string') {
          setError('Invalid job ID')
          setLoading(false)
          return
        }

        const jobData = await jobsApi.getById(params.id)
        setJob(jobData)
      } catch (err: any) {
        console.error('Error fetching job:', err)
        setError(err.response?.data?.detail || 'Failed to load job')
      } finally {
        setLoading(false)
      }
    }

    fetchJob()
  }, [params.id])

  if (loading) {
    return (
      <ModernDashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-slate-600">Loading job details...</p>
          </div>
        </div>
      </ModernDashboardLayout>
    )
  }

  if (error || !job) {
    return (
      <ModernDashboardLayout>
        <div className="text-center py-12">
          <div className="text-red-500 text-xl mb-4">❌ {error || 'Job not found'}</div>
          <button
            onClick={() => router.push('/dashboard/jobs/list')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all"
          >
            Back to Jobs List
          </button>
        </div>
      </ModernDashboardLayout>
    )
  }

  return (
    <ModernDashboardLayout>
      <div className="space-y-6">
        <div>
          <Link 
            href="/dashboard/jobs/list"
            className="inline-flex items-center text-sm text-slate-600 hover:text-slate-900 mb-2 transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to Jobs
          </Link>
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl shadow-lg">
              <Briefcase className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900">Edit Job</h1>
              <p className="text-slate-600 mt-1">Update job listing details</p>
            </div>
          </div>
        </div>
        <ModernJobForm initialData={job} isEditing={true} />
      </div>
    </ModernDashboardLayout>
  )
}
