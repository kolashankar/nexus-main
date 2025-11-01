'use client'

import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernInternshipForm from '@/components/ui/forms/internship/ModernInternshipForm'
import { GraduationCap, ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function CreateInternshipPage() {
  return (
    <ModernDashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <Link 
              href="/dashboard/internships/list"
              className="inline-flex items-center text-sm text-slate-600 hover:text-slate-900 mb-2 transition-colors"
            >
              <ArrowLeft className="w-4 h-4 mr-1" />
              Back to Internships
            </Link>
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl shadow-lg">
                <GraduationCap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900">Create New Internship</h1>
                <p className="text-slate-600 mt-1">Fill in the details to create a new internship listing</p>
              </div>
            </div>
          </div>
        </div>
        <ModernInternshipForm />
      </div>
    </ModernDashboardLayout>
  )
}
