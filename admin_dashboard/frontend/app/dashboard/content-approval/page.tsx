'use client'

import { useState, useEffect } from 'react'
import { contentApprovalApi } from '@/lib/api/client/config/interceptors/auth/token/contentApprovalApi'
import toast from 'react-hot-toast'

export default function ContentApproval() {
  const [pendingItems, setPendingItems] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedItem, setSelectedItem] = useState<any>(null)

  useEffect(() => {
    fetchPendingItems()
  }, [])

  const fetchPendingItems = async () => {
    try {
      setLoading(true)
      const response = await contentApprovalApi.getPending()
      setPendingItems(response.data.submissions || [])
    } catch (error: any) {
      toast.error('Failed to fetch pending items')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async (id: string) => {
    const comment = prompt('Add approval comment (optional):')
    try {
      await contentApprovalApi.approve(id, comment || undefined)
      toast.success('Content approved successfully')
      fetchPendingItems()
    } catch (error: any) {
      toast.error('Failed to approve content')
    }
  }

  const handleReject = async (id: string) => {
    const comment = prompt('Rejection reason (required):')
    if (!comment) return
    try {
      await contentApprovalApi.reject(id, comment)
      toast.success('Content rejected')
      fetchPendingItems()
    } catch (error: any) {
      toast.error('Failed to reject content')
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Content Approval Workflow</h1>

      {loading ? (
        <div className="text-center py-12">Loading...</div>
      ) : pendingItems.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No pending approvals</div>
      ) : (
        <div className="grid gap-4">
          {pendingItems.map((item) => (
            <div key={item._id} className="bg-white p-6 rounded-lg shadow">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-bold">{item.title}</h3>
                    <span className="px-2 py-1 rounded text-xs bg-yellow-100 text-yellow-800">
                      {item.content_type}
                    </span>
                  </div>
                  <p className="text-gray-600 mb-3">{item.description}</p>
                  <div className="flex gap-4 text-sm text-gray-500">
                    <span>Submitted by: {item.submitted_by}</span>
                    <span>Date: {new Date(item.submitted_at).toLocaleDateString()}</span>
                  </div>
                </div>
                <div className="flex flex-col gap-2 ml-4">
                  <button
                    onClick={() => setSelectedItem(item)}
                    className="text-blue-600 hover:underline text-sm"
                  >
                    View Details
                  </button>
                  <button
                    onClick={() => handleApprove(item._id)}
                    className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 text-sm"
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => handleReject(item._id)}
                    className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 text-sm"
                  >
                    Reject
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Detail Modal */}
      {selectedItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white p-6 rounded-lg w-full max-w-3xl max-h-[80vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">{selectedItem.title}</h2>
            <div className="prose max-w-none mb-4">
              <p><strong>Type:</strong> {selectedItem.content_type}</p>
              <p><strong>Submitted by:</strong> {selectedItem.submitted_by}</p>
              <p><strong>Submitted at:</strong> {new Date(selectedItem.submitted_at).toLocaleString()}</p>
              <div className="mt-4">
                <strong>Content:</strong>
                <div className="mt-2 p-4 bg-gray-50 rounded">
                  {JSON.stringify(selectedItem.content, null, 2)}
                </div>
              </div>
            </div>
            <button
              onClick={() => setSelectedItem(null)}
              className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
