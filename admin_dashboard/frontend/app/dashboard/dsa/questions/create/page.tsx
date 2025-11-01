'use client'

import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernDSAQuestionForm from '@/components/ui/forms/dsa/ModernDSAQuestionForm'
import { Code2, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function CreateDSAQuestionPage() {
  return (
    <ModernDashboardLayout>
      <div className="space-y-6">
        <div>
          <Link href="/dashboard/dsa/questions/list"
            className="inline-flex items-center text-sm text-slate-600 hover:text-slate-900 mb-2 transition-colors">
            <ArrowLeft className="w-4 h-4 mr-1" /> Back to Questions
          </Link>
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg">
              <Code2 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900">Create DSA Question</h1>
              <p className="text-slate-600 mt-1">Add a new coding problem</p>
            </div>
          </div>
        </div>
        <ModernDSAQuestionForm />
      </div>
    </ModernDashboardLayout>
  )
}
