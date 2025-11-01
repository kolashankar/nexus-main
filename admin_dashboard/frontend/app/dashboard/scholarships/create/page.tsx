'use client'

import DashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/DashboardLayout'
import ScholarshipForm from '@/components/ui/forms/scholarship/create/fields/input/validation/ScholarshipForm'

export default function CreateScholarshipPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Create New Scholarship</h1>
          <p className="text-gray-600 mt-1">Fill in the details to create a new scholarship listing manually</p>
        </div>
        <ScholarshipForm />
      </div>
    </DashboardLayout>
  )
}
