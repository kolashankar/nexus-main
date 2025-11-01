'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { usersApi } from '@/lib/api/client/config/interceptors/auth/token/usersApi'
import toast from 'react-hot-toast'
import Link from 'next/link'

export default function UserDetails() {
  const params = useParams()
  const router = useRouter()
  const id = params.id as string
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchUser()
  }, [id])

  const fetchUser = async () => {
    try {
      setLoading(true)
      const response = await usersApi.getById(id)
      setUser(response.data)
    } catch (error: any) {
      toast.error('Failed to fetch user')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="p-6 text-center">Loading user...</div>
  }

  if (!user) {
    return <div className="p-6 text-center">User not found</div>
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <button
          onClick={() => router.back()}
          className="text-blue-600 hover:underline mb-4"
        >
          ← Back to Users
        </button>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center mb-6">
          <div className="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
            {user.name?.charAt(0).toUpperCase()}
          </div>
          <div className="ml-6">
            <h1 className="text-3xl font-bold">{user.name}</h1>
            <p className="text-gray-600">{user.email}</p>
            <span className={`mt-2 inline-block px-3 py-1 text-sm rounded-full ${
              user.is_banned ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
            }`}>
              {user.is_banned ? 'Banned' : 'Active'}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6 mb-6">
          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-1">Phone</h3>
            <p className="text-lg">{user.phone || 'N/A'}</p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-1">Date Joined</h3>
            <p className="text-lg">{new Date(user.created_at).toLocaleDateString()}</p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-1">Last Login</h3>
            <p className="text-lg">{user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}</p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-1">Total Applications</h3>
            <p className="text-lg">{user.application_count || 0}</p>
          </div>
        </div>

        <div className="flex gap-4">
          <Link
            href={`/dashboard/users/${id}/activity`}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            View Activity
          </Link>
          <button
            onClick={() => router.push('/dashboard/users/list')}
            className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400"
          >
            Back to List
          </button>
        </div>
      </div>
    </div>
  )
}
