'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { dsaApi } from '@/lib/api/client/config/interceptors/auth/token/dsaApi'
import toast from 'react-hot-toast'

export default function DSACompaniesList() {
  const [companies, setCompanies] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCompanies()
  }, [])

  const fetchCompanies = async () => {
    try {
      setLoading(true)
      const response = await dsaApi.companies.getAll()
      setCompanies(response.data.companies || [])
    } catch (error: any) {
      toast.error('Failed to fetch companies')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure?')) return
    try {
      await dsaApi.companies.delete(id)
      toast.success('Company deleted successfully')
      fetchCompanies()
    } catch (error: any) {
      toast.error('Failed to delete company')
    }
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">DSA Companies</h1>
        <Link href="/dashboard/dsa/companies/create" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Add Company</Link>
      </div>

      {loading ? (
        <div className="text-center py-12">Loading...</div>
      ) : companies.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No companies found</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {companies.map((company) => (
            <div key={company._id} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition text-center">
              {company.logo && <img src={company.logo} alt={company.name} className="w-16 h-16 mx-auto mb-3 rounded" />}
              <h3 className="text-lg font-bold mb-1">{company.name}</h3>
              <p className="text-sm text-gray-600 mb-3">{company.industry}</p>
              <div className="text-xs text-gray-500 space-y-1 mb-3">
                <div>Problems: {company.problem_count || 0}</div>
                <div>Jobs: {company.job_count || 0}</div>
              </div>
              <div className="flex gap-2 justify-center">
                <Link href={`/dashboard/dsa/companies/edit/${company._id}`} className="text-blue-600 hover:underline text-sm">Edit</Link>
                <button onClick={() => handleDelete(company._id)} className="text-red-600 hover:underline text-sm">Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
