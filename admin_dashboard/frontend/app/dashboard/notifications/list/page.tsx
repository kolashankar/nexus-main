'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import axios from 'axios'
import { Trash2, Send, Plus, Eye } from 'lucide-react'

interface Notification {
  _id: string
  title: string
  message: string
  target_audience: string
  priority: string
  status: string
  sent_count: number
  opened_count: number
  created_at: string
  scheduled_for: string
}

export default function NotificationsList() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchNotifications()
  }, [])

  const fetchNotifications = async () => {
    try {
      const response = await axios.get('/api/admin/notifications')
      setNotifications(response.data.data || [])
    } catch (error) {
      console.error('Error fetching notifications:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSend = async (id: string) => {
    if (!confirm('Are you sure you want to send this notification?')) return

    try {
      await axios.post(`/api/admin/notifications/${id}/send`)
      fetchNotifications()
      alert('Notification sent successfully!')
    } catch (error) {
      console.error('Error sending notification:', error)
      alert('Failed to send notification')
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this notification?')) return

    try {
      await axios.delete(`/api/admin/notifications/${id}`)
      fetchNotifications()
    } catch (error) {
      console.error('Error deleting notification:', error)
      alert('Failed to delete notification')
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'sent': return 'bg-green-100 text-green-800'
      case 'scheduled': return 'bg-blue-100 text-blue-800'
      case 'draft': return 'bg-yellow-100 text-yellow-800'
      case 'failed': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return <div className="flex justify-center items-center h-64"><div className="text-lg text-gray-600">Loading notifications...</div></div>
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Push Notifications</h1>
        <Link href="/dashboard/notifications/create" className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center gap-2">
          <Plus size={20} />
          Create Notification
        </Link>
      </div>

      <div className="grid gap-4">
        {notifications.length === 0 ? (
          <div className="bg-white p-8 rounded-lg shadow text-center text-gray-500">
            No notifications found. Create your first notification!
          </div>
        ) : (
          notifications.map((notification) => (
            <div key={notification._id} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-semibold text-gray-800">{notification.title}</h3>
                    <span className={`px-3 py-1 text-xs rounded-full font-semibold ${getStatusColor(notification.status)}`}>
                      {notification.status}
                    </span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-800 text-xs rounded-full">
                      {notification.priority}
                    </span>
                  </div>
                  <p className="text-gray-600 mb-3">{notification.message}</p>
                  
                  <div className="flex gap-4 text-sm text-gray-600">
                    <span>Audience: {notification.target_audience}</span>
                    {notification.sent_count > 0 && (
                      <>
                        <span>Sent: {notification.sent_count}</span>
                        <span>Opened: {notification.opened_count} ({Math.round((notification.opened_count / notification.sent_count) * 100)}%)</span>
                      </>
                    )}
                  </div>
                  
                  <div className="text-sm text-gray-500 mt-2">
                    {notification.scheduled_for 
                      ? `Scheduled for: ${new Date(notification.scheduled_for).toLocaleString()}`
                      : `Created: ${new Date(notification.created_at).toLocaleString()}`
                    }
                  </div>
                </div>

                <div className="flex gap-2">
                  {notification.status === 'draft' && (
                    <button
                      onClick={() => handleSend(notification._id)}
                      className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 flex items-center gap-2"
                    >
                      <Send size={16} />
                      Send
                    </button>
                  )}
                  <button
                    onClick={() => handleDelete(notification._id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
