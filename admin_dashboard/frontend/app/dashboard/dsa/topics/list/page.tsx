'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import { Plus, Search, Edit, Trash2, ListTree } from 'lucide-react'

export default function DSATopicsListPage() {
  const [topics, setTopics] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  const fetch = async () => {
    try {
      setLoading(true)
      const res = await fetch(`/api/admin/dsa/topics?search=${search}`)
      const data = await res.json()
      setTopics(data.topics || data.items || [])
    } catch (e) {}
    finally { setLoading(false) }
  }
  useEffect(() => { fetch() }, [search])

  const handleDelete = async (id: string) => {
    if (!confirm('Delete?')) return
    try { await fetch(`/api/admin/dsa/topics/${id}`, { method: 'DELETE' }); alert('Deleted'); fetch() } catch (e) { alert('Failed') }
  }

  return (
    <ModernDashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl shadow-lg"><ListTree className="w-6 h-6 text-white" /></div>
            <div><h1 className="text-3xl font-bold text-slate-900">DSA Topics</h1></div>
          </div>
          <Link href="/dashboard/dsa/topics/create"><button className="px-6 py-3 bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-lg shadow-lg flex items-center"><Plus className="w-5 h-5 mr-2" />Create</button></Link>
        </div>
        <div className="bg-white rounded-xl shadow-lg border p-6">
          <div className="relative"><Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input type="text" placeholder="Search..." value={search} onChange={(e) => setSearch(e.target.value)} className="w-full pl-11 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-cyan-500" />
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-lg border overflow-hidden">
          {loading ? <div className="p-12 text-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-600 mx-auto"></div></div> :
          topics.length === 0 ? <div className="p-12 text-center"><p>No topics</p></div> :
          <table className="w-full"><thead className="bg-slate-50"><tr><th className="px-6 py-4 text-left text-xs font-semibold uppercase">Name</th><th className="px-6 py-4 text-left text-xs font-semibold uppercase">Category</th><th className="px-6 py-4 text-left text-xs font-semibold uppercase">Difficulty</th><th className="px-6 py-4 text-right text-xs font-semibold uppercase">Actions</th></tr></thead>
          <tbody className="divide-y">{topics.map((t) => <tr key={t._id} className="hover:bg-slate-50"><td className="px-6 py-4 font-semibold">{t.name}</td><td className="px-6 py-4">{t.category}</td><td className="px-6 py-4">{t.difficulty_level}</td><td className="px-6 py-4 text-right"><Link href={`/dashboard/dsa/topics/edit/${t._id}`}><button className="p-2 text-cyan-600 hover:bg-cyan-50 rounded-lg"><Edit className="w-4 h-4" /></button></Link><button onClick={() => handleDelete(t._id)} className="p-2 text-red-600 hover:bg-red-50 rounded-lg ml-2"><Trash2 className="w-4 h-4" /></button></td></tr>)}</tbody>
          </table>}
        </div>
      </div>
    </ModernDashboardLayout>
  )
}
