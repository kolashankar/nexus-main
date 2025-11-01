'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernDSAQuestionForm from '@/components/ui/forms/dsa/ModernDSAQuestionForm'
import { Code2, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function EditDSAQuestionPage() {
  const params = useParams()
  const [question, setQuestion] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await fetch(`/api/admin/dsa/questions/${params.id}`)
        setQuestion(await res.json())
      } catch (error) {
        alert('Failed to load')
      } finally {
        setLoading(false)
      }
    }
    if (params.id) fetch()
  }, [params.id])

  if (loading) return <ModernDashboardLayout><div className="flex items-center justify-center h-96"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div></div></ModernDashboardLayout>

  return (
    <ModernDashboardLayout>
      <div className="space-y-6">
        <div>
          <Link href="/dashboard/dsa/questions/list" className="inline-flex items-center text-sm text-slate-600 hover:text-slate-900 mb-2">
            <ArrowLeft className="w-4 h-4 mr-1" /> Back
          </Link>
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg">
              <Code2 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900">Edit Question</h1>
            </div>
          </div>
        </div>
        {question && <ModernDSAQuestionForm initialData={question} isEditing />}
      </div>
    </ModernDashboardLayout>
  )
}
