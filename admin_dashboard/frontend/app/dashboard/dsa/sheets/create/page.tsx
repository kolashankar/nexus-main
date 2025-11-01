'use client'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernDSASheetForm from '@/components/ui/forms/dsa/ModernDSASheetForm'
import { Layers, ArrowLeft } from 'lucide-react'
import Link from 'next/link'
export default function CreateDSASheetPage() {
  return <ModernDashboardLayout><div className="space-y-6"><div><Link href="/dashboard/dsa/sheets/list" className="inline-flex items-center text-sm text-slate-600 mb-2"><ArrowLeft className="w-4 h-4 mr-1" />Back</Link><div className="flex items-center space-x-3"><div className="p-3 bg-gradient-to-br from-violet-500 to-purple-600 rounded-xl shadow-lg"><Layers className="w-6 h-6 text-white" /></div><div><h1 className="text-3xl font-bold text-slate-900">Create DSA Sheet</h1></div></div></div><ModernDSASheetForm /></div></ModernDashboardLayout>
}
