'use client'

import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernScholarshipForm from '@/components/ui/forms/scholarship/ModernScholarshipForm'
import { Award, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function CreateScholarshipPage() {
  return (
    <ModernDashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <Link 
              href="/dashboard/scholarships/list"
              className="inline-flex items-center text-sm text-slate-600 hover:text-slate-900 mb-2 transition-colors"
            >
              <ArrowLeft className="w-4 h-4 mr-1" />
              Back to Scholarships
            </Link>
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-gradient-to-br from-orange-500 to-amber-600 rounded-xl shadow-lg">
                <Award className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900">Create New Scholarship</h1>
                <p className="text-slate-600 mt-1">Fill in the details to create a new scholarship listing</p>
              </div>
            </div>
          </div>
        </div>
        <ModernScholarshipForm />
      </div>
    </ModernDashboardLayout>
  )
}
