'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernRoadmapForm from '@/components/ui/forms/roadmap/ModernRoadmapForm'
import { Map, ArrowLeft } from 'lucide-react'
import Link from 'next/link'
export default function EditRoadmapPage() {
  const params = useParams()
  const [roadmap, setRoadmap] = useState(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => { const load = async () => { try { const res = await fetch(`/api/admin/roadmaps/${params.id}`); setRoadmap(await res.json()) } catch (e) { alert('Failed') } finally { setLoading(false) } }; if (params.id) load() }, [params.id])
  if (loading) return <ModernDashboardLayout><div className="flex items-center justify-center h-96"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div></div></ModernDashboardLayout>
  return <ModernDashboardLayout><div className="space-y-6"><div><Link href="/dashboard/roadmaps/list" className="inline-flex items-center text-sm text-slate-600 mb-2"><ArrowLeft className="w-4 h-4 mr-1" />Back</Link><div className="flex items-center space-x-3"><div className="p-3 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-xl shadow-lg"><Map className="w-6 h-6 text-white" /></div><div><h1 className="text-3xl font-bold text-slate-900">Edit Roadmap</h1></div></div></div>{roadmap && <ModernRoadmapForm initialData={roadmap} isEditing />}</div></ModernDashboardLayout>
}
