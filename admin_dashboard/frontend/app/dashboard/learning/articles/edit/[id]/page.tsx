'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import ModernDashboardLayout from '@/components/ui/layout/sidebar/navigation/items/menu/handlers/ModernDashboardLayout'
import ModernArticleForm from '@/components/ui/forms/learning/ModernArticleForm'
import { BookOpen, ArrowLeft } from 'lucide-react'
import Link from 'next/link'
export default function EditArticlePage() {
  const params = useParams()
  const [article, setArticle] = useState(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => { const load = async () => { try { const res = await fetch(`/api/admin/learning/articles/${params.id}`); setArticle(await res.json()) } catch (e) { alert('Failed') } finally { setLoading(false) } }; if (params.id) load() }, [params.id])
  if (loading) return <ModernDashboardLayout><div className="flex items-center justify-center h-96"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-rose-600"></div></div></ModernDashboardLayout>
  return <ModernDashboardLayout><div className="space-y-6"><div><Link href="/dashboard/learning/articles/list" className="inline-flex items-center text-sm text-slate-600 mb-2"><ArrowLeft className="w-4 h-4 mr-1" />Back</Link><div className="flex items-center space-x-3"><div className="p-3 bg-gradient-to-br from-rose-500 to-pink-600 rounded-xl shadow-lg"><BookOpen className="w-6 h-6 text-white" /></div><div><h1 className="text-3xl font-bold text-slate-900">Edit Article</h1></div></div></div>{article && <ModernArticleForm initialData={article} isEditing />}</div></ModernDashboardLayout>
}
