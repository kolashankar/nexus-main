'use client'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernDSATopicForm from '@/components/ui/forms/dsa/ModernDSATopicForm'
import { ListTree, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function CreateDSATopicPage() {
  return (
    <ModernDashboardLayout>
      <div className="space-y-6">
        <div>
          <Link href="/dashboard/dsa/topics/list" className="inline-flex items-center text-sm text-slate-600 hover:text-slate-900 mb-2"><ArrowLeft className="w-4 h-4 mr-1" /> Back</Link>
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl shadow-lg"><ListTree className="w-6 h-6 text-white" /></div>
            <div><h1 className="text-3xl font-bold text-slate-900">Create DSA Topic</h1></div>
          </div>
        </div>
        <ModernDSATopicForm />
      </div>
    </ModernDashboardLayout>
  )
}
