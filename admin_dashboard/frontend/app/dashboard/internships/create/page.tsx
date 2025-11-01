'use client'

import DashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/DashboardLayout'
import InternshipForm from '@/components/ui/forms/internship/create/fields/input/validation/InternshipForm'

export default function CreateInternshipPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Create New Internship</h1>
          <p className="text-gray-600 mt-1">Fill in the details to create a new internship listing manually</p>
        </div>
        <InternshipForm />
      </div>
    </DashboardLayout>
  )
}
