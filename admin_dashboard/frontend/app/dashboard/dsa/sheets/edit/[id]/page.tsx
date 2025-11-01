'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernDSASheetForm from '@/components/ui/forms/dsa/ModernDSASheetForm'
import { Layers, ArrowLeft } from 'lucide-react'
import Link from 'next/link'
export default function EditDSASheetPage() {
  const params = useParams()
  const [sheet, setSheet] = useState(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => { const load = async () => { try { const res = await fetch(`/api/admin/dsa/sheets/${params.id}`); setSheet(await res.json()) } catch (e) { alert('Failed') } finally { setLoading(false) } }; if (params.id) load() }, [params.id])
  if (loading) return <ModernDashboardLayout><div className="flex items-center justify-center h-96"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-violet-600"></div></div></ModernDashboardLayout>
  return <ModernDashboardLayout><div className="space-y-6"><div><Link href="/dashboard/dsa/sheets/list" className="inline-flex items-center text-sm text-slate-600 mb-2"><ArrowLeft className="w-4 h-4 mr-1" />Back</Link><div className="flex items-center space-x-3"><div className="p-3 bg-gradient-to-br from-violet-500 to-purple-600 rounded-xl shadow-lg"><Layers className="w-6 h-6 text-white" /></div><div><h1 className="text-3xl font-bold text-slate-900">Edit Sheet</h1></div></div></div>{sheet && <ModernDSASheetForm initialData={sheet} isEditing />}</div></ModernDashboardLayout>
}
