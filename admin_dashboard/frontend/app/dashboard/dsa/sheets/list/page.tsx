'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { dsaApi } from '@/lib/api/client/config/interceptors/auth/token/dsaApi'
import toast from 'react-hot-toast'

export default function DSASheetsList() {
  const [sheets, setSheets] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSheets()
  }, [])

  const fetchSheets = async () => {
    try {
      setLoading(true)
      const response = await dsaApi.sheets.getAll()
      setSheets(response.data.sheets || [])
    } catch (error: any) {
      toast.error('Failed to fetch sheets')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure?')) return
    try {
      await dsaApi.sheets.delete(id)
      toast.success('Sheet deleted successfully')
      fetchSheets()
    } catch (error: any) {
      toast.error('Failed to delete sheet')
    }
  }

  const handleTogglePublish = async (id: string) => {
    try {
      await dsaApi.sheets.togglePublish(id)
      toast.success('Sheet status updated')
      fetchSheets()
    } catch (error: any) {
      toast.error('Failed to update sheet')
    }
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">DSA Sheets</h1>
        <div className="flex gap-2">
          <Link href="/dashboard/dsa/sheets/create" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Create Sheet</Link>
          <Link href="/dashboard/dsa/sheets/create-ai" className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">Generate with AI</Link>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">Loading...</div>
      ) : sheets.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No sheets found</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sheets.map((sheet) => (
            <div key={sheet._id} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <h3 className="text-xl font-bold mb-2">{sheet.name}</h3>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">{sheet.description}</p>
              <div className="flex gap-4 text-sm text-gray-500 mb-3">
                <span>Level: {sheet.level}</span>
                <span>Questions: {sheet.questions?.length || 0}</span>
                <span className={`px-2 py-1 rounded ${sheet.is_published ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                  {sheet.is_published ? 'Published' : 'Draft'}
                </span>
              </div>
              <div className="flex gap-2">
                <Link href={`/dashboard/dsa/sheets/edit/${sheet._id}`} className="text-blue-600 hover:underline text-sm">Edit</Link>
                <button onClick={() => handleTogglePublish(sheet._id)} className="text-orange-600 hover:underline text-sm">
                  {sheet.is_published ? 'Unpublish' : 'Publish'}
                </button>
                <button onClick={() => handleDelete(sheet._id)} className="text-red-600 hover:underline text-sm">Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
