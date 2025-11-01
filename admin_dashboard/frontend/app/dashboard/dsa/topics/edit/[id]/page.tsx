'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernDSATopicForm from '@/components/ui/forms/dsa/ModernDSATopicForm'
import { ListTree, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function EditDSATopicPage() {
  const params = useParams()
  const [topic, setTopic] = useState(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    const load = async () => {
      try { const res = await fetch(`/api/admin/dsa/topics/${params.id}`); setTopic(await res.json()) }
      catch (e) { alert('Failed') } finally { setLoading(false) }
    }
    if (params.id) load()
  }, [params.id])
  if (loading) return <ModernDashboardLayout><div className="flex items-center justify-center h-96"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-600"></div></div></ModernDashboardLayout>
  return <ModernDashboardLayout><div className="space-y-6"><div><Link href="/dashboard/dsa/topics/list" className="inline-flex items-center text-sm text-slate-600 mb-2"><ArrowLeft className="w-4 h-4 mr-1" />Back</Link><div className="flex items-center space-x-3"><div className="p-3 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl shadow-lg"><ListTree className="w-6 h-6 text-white" /></div><div><h1 className="text-3xl font-bold text-slate-900">Edit Topic</h1></div></div></div>{topic && <ModernDSATopicForm initialData={topic} isEditing />}</div></ModernDashboardLayout>
}
