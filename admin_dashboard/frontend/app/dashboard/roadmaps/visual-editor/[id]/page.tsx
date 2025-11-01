'use client'

import { useState, useEffect, useCallback } from 'react'
import { useParams, useRouter } from 'next/navigation'
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge,
  Node,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { roadmapsApi } from '@/lib/api/client/config/interceptors/auth/token/roadmapsApi'
import toast from 'react-hot-toast'

export default function RoadmapVisualEditor() {
  const params = useParams()
  const router = useRouter()
  const id = params.id as string
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [roadmap, setRoadmap] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    fetchRoadmap()
  }, [id])

  const fetchRoadmap = async () => {
    try {
      setLoading(true)
      const response = await roadmapsApi.getById(id)
      const data = response.roadmap
      setRoadmap(data)

      // Convert backend nodes to ReactFlow nodes
      const flowNodes = data.nodes.map((node: any) => ({
        id: node.id || node.node_id,
        type: 'default',
        position: { x: node.position_x, y: node.position_y },
        data: { 
          label: node.title,
          description: node.description,
          type: node.type,
        },
        style: {
          background: node.type === 'content' ? '#3b82f6' : node.type === 'roadmap_link' ? '#8b5cf6' : '#10b981',
          color: 'white',
          padding: '10px',
          borderRadius: '8px',
          minWidth: '150px',
        },
      }))

      // Convert connections to edges
      const flowEdges: Edge[] = []
      data.nodes.forEach((node: any) => {
        const nodeId = node.id || node.node_id;
        node.connections.forEach((targetId: string) => {
          flowEdges.push({
            id: `${nodeId}-${targetId}`,
            source: nodeId,
            target: targetId,
            animated: true,
          })
        })
      })

      setNodes(flowNodes)
      setEdges(flowEdges)
    } catch (error: any) {
      toast.error('Failed to fetch roadmap')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const onConnect = useCallback(
    (params: Connection | Edge) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  )

  const handleSave = async () => {
    try {
      setSaving(true)
      
      // Convert ReactFlow nodes back to backend format
      const backendNodes = nodes.map((node: Node) => {
        const connections = edges
          .filter(edge => edge.source === node.id)
          .map(edge => edge.target)
        
        return {
          id: node.id,
          title: node.data.label,
          description: node.data.description || '',
          type: node.data.type || 'content',
          position_x: node.position.x,
          position_y: node.position.y,
          connections,
        }
      })

      await roadmapsApi.update(id, { nodes: backendNodes })
      toast.success('Roadmap saved successfully')
    } catch (error: any) {
      toast.error('Failed to save roadmap')
      console.error(error)
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return <div className="p-6 text-center">Loading roadmap...</div>
  }

  return (
    <div className="h-screen flex flex-col">
      <div className="bg-white p-4 border-b flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">{roadmap?.title}</h1>
          <p className="text-sm text-gray-600">{roadmap?.description}</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleSave}
            disabled={saving}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
          <button
            onClick={() => router.back()}
            className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400"
          >
            Back
          </button>
        </div>
      </div>

      <div className="flex-1">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
        >
          <Controls />
          <MiniMap />
          <Background gap={12} size={1} />
        </ReactFlow>
      </div>

      <div className="bg-white p-4 border-t">
        <div className="flex gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-blue-600 rounded"></div>
            <span>Content Node</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-purple-600 rounded"></div>
            <span>Roadmap Link</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-green-600 rounded"></div>
            <span>Article Link</span>
          </div>
        </div>
      </div>
    </div>
  )
}
