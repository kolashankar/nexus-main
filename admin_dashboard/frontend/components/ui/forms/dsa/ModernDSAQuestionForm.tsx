'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Code2, CheckCircle, X, Plus, Lightbulb } from 'lucide-react'

interface DSAQuestion {
  _id?: string
  title: string
  description: string
  difficulty: string
  topic: string
  companies: string[]
  code_template: string
  test_cases: Array<{ input: string; output: string; explanation: string }>
  hints: string[]
  solution: string
  is_active: boolean
}

interface DSAQuestionFormProps {
  initialData?: DSAQuestion
  isEditing?: boolean
}

export default function ModernDSAQuestionForm({ initialData, isEditing = false }: DSAQuestionFormProps) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('basic')
  const [formData, setFormData] = useState<Partial<DSAQuestion>>({
    title: initialData?.title || '',
    description: initialData?.description || '',
    difficulty: initialData?.difficulty || 'Easy',
    topic: initialData?.topic || 'Arrays',
    companies: initialData?.companies || [],
    code_template: initialData?.code_template || '',
    test_cases: initialData?.test_cases || [],
    hints: initialData?.hints || [],
    solution: initialData?.solution || '',
    is_active: initialData?.is_active ?? true,
  })

  const [companyInput, setCompanyInput] = useState('')
  const [hintInput, setHintInput] = useState('')
  const [testCaseInput, setTestCaseInput] = useState({ input: '', output: '', explanation: '' })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.title || !formData.description) {
      alert('Please fill in all required fields')
      return
    }

    setLoading(true)
    try {
      const url = isEditing && initialData?._id 
        ? `/api/admin/dsa/questions/${initialData._id}`
        : '/api/admin/dsa/questions'
      
      const response = await fetch(url, {
        method: isEditing ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (!response.ok) throw new Error('Failed to save question')
      alert(`✅ Question ${isEditing ? 'updated' : 'created'} successfully!`)
      router.push('/dashboard/dsa/questions/list')
    } catch (error: any) {
      alert(`❌ Failed to save question: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const addCompany = () => {
    if (companyInput.trim()) {
      setFormData({ ...formData, companies: [...(formData.companies || []), companyInput.trim()] })
      setCompanyInput('')
    }
  }

  const addHint = () => {
    if (hintInput.trim()) {
      setFormData({ ...formData, hints: [...(formData.hints || []), hintInput.trim()] })
      setHintInput('')
    }
  }

  const addTestCase = () => {
    if (testCaseInput.input && testCaseInput.output) {
      setFormData({ ...formData, test_cases: [...(formData.test_cases || []), testCaseInput] })
      setTestCaseInput({ input: '', output: '', explanation: '' })
    }
  }

  const tabs = [
    { id: 'basic', name: 'Basic Info', icon: Code2 },
    { id: 'code', name: 'Code & Tests', icon: CheckCircle },
    { id: 'hints', name: 'Hints & Solution', icon: Lightbulb },
  ]

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden">
        <div className="border-b border-slate-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button key={tab.id} type="button" onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id ? 'border-green-600 text-green-600' : 'border-transparent text-slate-500 hover:text-slate-700'
                  }`}>
                  <Icon className="w-4 h-4" />
                  <span>{tab.name}</span>
                </button>
              )
            })}
          </nav>
        </div>

        <div className="p-8">
          {activeTab === 'basic' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Question Title *</label>
                  <input type="text" required value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                    placeholder="e.g., Two Sum Problem" />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Difficulty *</label>
                  <select required value={formData.difficulty}
                    onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all">
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Topic *</label>
                  <select required value={formData.topic}
                    onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all">
                    <option value="Arrays">Arrays</option>
                    <option value="Strings">Strings</option>
                    <option value="Linked Lists">Linked Lists</option>
                    <option value="Trees">Trees</option>
                    <option value="Graphs">Graphs</option>
                    <option value="Dynamic Programming">Dynamic Programming</option>
                    <option value="Sorting">Sorting</option>
                    <option value="Searching">Searching</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Description *</label>
                <textarea required value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })} rows={6}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all resize-none"
                  placeholder="Describe the problem..." />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-3">Companies</label>
                <div className="flex gap-2 mb-3">
                  <input type="text" value={companyInput} onChange={(e) => setCompanyInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCompany())}
                    className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    placeholder="e.g., Google, Amazon" />
                  <button type="button" onClick={addCompany}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center">
                    <Plus className="w-4 h-4 mr-1" /> Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {formData.companies?.map((company, index) => (
                    <span key={index} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                      {company}
                      <button type="button" onClick={() => setFormData({ ...formData, companies: formData.companies?.filter((_, i) => i !== index) })}
                        className="ml-2 text-green-600 hover:text-green-800">
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'code' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Code Template</label>
                <textarea value={formData.code_template}
                  onChange={(e) => setFormData({ ...formData, code_template: e.target.value })} rows={8}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 font-mono text-sm bg-slate-50"
                  placeholder="def twoSum(nums, target):\n    pass" />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-3">Test Cases</label>
                <div className="space-y-3 mb-3">
                  <input type="text" placeholder="Input" value={testCaseInput.input}
                    onChange={(e) => setTestCaseInput({ ...testCaseInput, input: e.target.value })}
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500" />
                  <input type="text" placeholder="Expected Output" value={testCaseInput.output}
                    onChange={(e) => setTestCaseInput({ ...testCaseInput, output: e.target.value })}
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500" />
                  <input type="text" placeholder="Explanation (optional)" value={testCaseInput.explanation}
                    onChange={(e) => setTestCaseInput({ ...testCaseInput, explanation: e.target.value })}
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500" />
                  <button type="button" onClick={addTestCase}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center">
                    <Plus className="w-4 h-4 mr-1" /> Add Test Case
                  </button>
                </div>
                <div className="space-y-2">
                  {formData.test_cases?.map((tc, index) => (
                    <div key={index} className="p-3 bg-green-50 border border-green-200 rounded-lg">
                      <div className="text-sm"><strong>Input:</strong> {tc.input}</div>
                      <div className="text-sm"><strong>Output:</strong> {tc.output}</div>
                      {tc.explanation && <div className="text-sm text-slate-600">{tc.explanation}</div>}
                      <button type="button" onClick={() => setFormData({ ...formData, test_cases: formData.test_cases?.filter((_, i) => i !== index) })}
                        className="mt-2 text-red-600 hover:text-red-800 text-sm">Remove</button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'hints' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-3">Hints</label>
                <div className="flex gap-2 mb-3">
                  <input type="text" value={hintInput} onChange={(e) => setHintInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addHint())}
                    className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    placeholder="e.g., Try using a hash map" />
                  <button type="button" onClick={addHint}
                    className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors flex items-center">
                    <Plus className="w-4 h-4 mr-1" /> Add
                  </button>
                </div>
                <div className="space-y-2">
                  {formData.hints?.map((hint, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <span className="text-sm text-yellow-900">{hint}</span>
                      <button type="button" onClick={() => setFormData({ ...formData, hints: formData.hints?.filter((_, i) => i !== index) })}
                        className="text-yellow-600 hover:text-yellow-800">
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Solution</label>
                <textarea value={formData.solution}
                  onChange={(e) => setFormData({ ...formData, solution: e.target.value })} rows={10}
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-green-500 font-mono text-sm bg-slate-50"
                  placeholder="Provide the complete solution..." />
              </div>
              <div className="flex items-center">
                <input type="checkbox" id="is_active" checked={formData.is_active}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  className="w-4 h-4 text-green-600 border-slate-300 rounded focus:ring-green-500" />
                <label htmlFor="is_active" className="ml-2 text-sm font-medium text-slate-700">Active</label>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="flex justify-end space-x-4">
        <button type="button" onClick={() => router.back()}
          className="px-6 py-3 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-all font-medium">
          Cancel
        </button>
        <button type="submit" disabled={loading}
          className="px-8 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-700 hover:to-emerald-700 shadow-lg shadow-green-500/50 transition-all font-medium disabled:opacity-50 flex items-center">
          {loading ? <><div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>Saving...</> :
            <><CheckCircle className="w-5 h-5 mr-2" />{isEditing ? 'Update Question' : 'Create Question'}</>}
        </button>
      </div>
    </form>
  )
}
