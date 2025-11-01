'use client'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernRoadmapForm from '@/components/ui/forms/roadmap/ModernRoadmapForm'
import { Map, ArrowLeft } from 'lucide-react'
import Link from 'next/link'
export default function CreateRoadmapPage() {
  return <ModernDashboardLayout><div className="space-y-6"><div><Link href="/dashboard/roadmaps/list" className="inline-flex items-center text-sm text-slate-600 mb-2"><ArrowLeft className="w-4 h-4 mr-1" />Back</Link><div className="flex items-center space-x-3"><div className="p-3 bg-gradient-to-br from-indigo-500 to-blue-600 rounded-xl shadow-lg"><Map className="w-6 h-6 text-white" /></div><div><h1 className="text-3xl font-bold text-slate-900">Create Roadmap</h1></div></div></div><ModernRoadmapForm /></div></ModernDashboardLayout>
}
