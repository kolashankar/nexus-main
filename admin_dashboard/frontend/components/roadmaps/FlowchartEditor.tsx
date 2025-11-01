'use client'

import React, { useCallback, useState, useEffect } from 'react'
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Node,
  Edge,
  Connection,
  BackgroundVariant,
  Panel,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { RoadmapNode } from '@/lib/api/client/config/interceptors/auth/token/roadmapsApi'
import { Plus, Save, Upload, Download, Trash2, Edit2 } from 'lucide-react'

interface FlowchartEditorProps {
  initialNodes?: RoadmapNode[]
  onSave: (nodes: RoadmapNode[]) => void
  readonly?: boolean
}

// Custom node types for different roadmap nodes
const nodeTypes = {
  content: ({ data }: any) => (
    <div className={`px-4 py-3 rounded-lg border-2 shadow-md ${data.selected ? 'border-blue-500' : 'border-gray-300'} bg-white min-w-[200px]`}>
      <div className="flex items-center gap-2 mb-1">
        <div className="w-3 h-3 rounded-full bg-blue-500"></div>
        <div className="font-semibold text-sm">{data.label}</div>
      </div>
      {data.description && <div className="text-xs text-gray-600 mt-1">{data.description}</div>}
      {data.estimatedTime && <div className="text-xs text-gray-500 mt-1">⏱️ {data.estimatedTime}</div>}
    </div>
  ),
  roadmap_link: ({ data }: any) => (
    <div className={`px-4 py-3 rounded-lg border-2 shadow-md ${data.selected ? 'border-purple-500' : 'border-purple-300'} bg-purple-50 min-w-[200px]`}>
      <div className="flex items-center gap-2 mb-1">
        <div className="w-3 h-3 rounded-full bg-purple-500"></div>
        <div className="font-semibold text-sm">🗺️ {data.label}</div>
      </div>
      {data.description && <div className="text-xs text-gray-600 mt-1">{data.description}</div>}
    </div>
  ),
  article_link: ({ data }: any) => (
    <div className={`px-4 py-3 rounded-lg border-2 shadow-md ${data.selected ? 'border-green-500' : 'border-green-300'} bg-green-50 min-w-[200px]`}>
      <div className="flex items-center gap-2 mb-1">
        <div className="w-3 h-3 rounded-full bg-green-500"></div>
        <div className="font-semibold text-sm">📄 {data.label}</div>
      </div>
      {data.description && <div className="text-xs text-gray-600 mt-1">{data.description}</div>}
    </div>
  ),
}

export default function FlowchartEditor({ initialNodes = [], onSave, readonly = false }: FlowchartEditorProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [selectedNode, setSelectedNode] = useState<Node | null>(null)
  const [showNodeEditor, setShowNodeEditor] = useState(false)
  const [nodeFormData, setNodeFormData] = useState({
    id: '',
    title: '',
    description: '',
    content: '',
    node_type: 'content',
    estimated_time: '',
    linked_roadmap_id: '',
    linked_article_id: '',
    linked_url: '',
    color: '#3B82F6',
  })

  // Convert RoadmapNode[] to ReactFlow nodes and edges
  useEffect(() => {
    if (initialNodes && initialNodes.length > 0) {
      const flowNodes: Node[] = initialNodes.map((node) => ({
        id: node.id,
        type: node.node_type || 'content',
        position: { x: node.position_x || 0, y: node.position_y || 0 },
        data: {
          label: node.title,
          description: node.description,
          estimatedTime: node.estimated_time,
          nodeType: node.node_type,
          content: node.content,
          color: node.color,
        },
      }))

      const flowEdges: Edge[] = []
      initialNodes.forEach((node) => {
        node.child_nodes?.forEach((childId) => {
          flowEdges.push({
            id: `${node.id}-${childId}`,
            source: node.id,
            target: childId,
            type: 'smoothstep',
            animated: true,
          })
        })
      })

      setNodes(flowNodes)
      setEdges(flowEdges)
    }
  }, [initialNodes, setNodes, setEdges])

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge({ ...params, type: 'smoothstep', animated: true }, eds)),
    [setEdges]
  )

  const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
    if (!readonly) {
      setSelectedNode(node)
    }
  }, [readonly])

  const addNewNode = () => {
    const newNodeId = `node_${Date.now()}`
    setNodeFormData({
      id: newNodeId,
      title: '',
      description: '',
      content: '',
      node_type: 'content',
      estimated_time: '',
      linked_roadmap_id: '',
      linked_article_id: '',
      linked_url: '',
      color: '#3B82F6',
    })
    setShowNodeEditor(true)
  }

  const editNode = () => {
    if (!selectedNode) return
    
    // Find the original node data
    const originalNode = initialNodes.find(n => n.id === selectedNode.id)
    setNodeFormData({
      id: selectedNode.id,
      title: selectedNode.data.label || '',
      description: selectedNode.data.description || '',
      content: originalNode?.content || '',
      node_type: selectedNode.data.nodeType || 'content',
      estimated_time: selectedNode.data.estimatedTime || '',
      linked_roadmap_id: originalNode?.linked_roadmap_id || '',
      linked_article_id: originalNode?.linked_article_id || '',
      linked_url: originalNode?.linked_url || '',
      color: selectedNode.data.color || '#3B82F6',
    })
    setShowNodeEditor(true)
  }

  const deleteNode = () => {
    if (!selectedNode) return
    setNodes((nds) => nds.filter((n) => n.id !== selectedNode.id))
    setEdges((eds) => eds.filter((e) => e.source !== selectedNode.id && e.target !== selectedNode.id))
    setSelectedNode(null)
  }

  const saveNode = () => {
    if (nodeFormData.title.trim() === '') {
      alert('Node title is required')
      return
    }

    const isNewNode = !nodes.find((n) => n.id === nodeFormData.id)

    if (isNewNode) {
      const newNode: Node = {
        id: nodeFormData.id,
        type: nodeFormData.node_type,
        position: { x: Math.random() * 400 + 100, y: Math.random() * 400 + 100 },
        data: {
          label: nodeFormData.title,
          description: nodeFormData.description,
          estimatedTime: nodeFormData.estimated_time,
          nodeType: nodeFormData.node_type,
          content: nodeFormData.content,
          color: nodeFormData.color,
        },
      }
      setNodes((nds) => [...nds, newNode])
    } else {
      setNodes((nds) =>
        nds.map((node) =>
          node.id === nodeFormData.id
            ? {
                ...node,
                type: nodeFormData.node_type,
                data: {
                  label: nodeFormData.title,
                  description: nodeFormData.description,
                  estimatedTime: nodeFormData.estimated_time,
                  nodeType: nodeFormData.node_type,
                  content: nodeFormData.content,
                  color: nodeFormData.color,
                },
              }
            : node
        )
      )
    }

    setShowNodeEditor(false)
    setNodeFormData({
      id: '',
      title: '',
      description: '',
      content: '',
      node_type: 'content',
      estimated_time: '',
      linked_roadmap_id: '',
      linked_article_id: '',
      linked_url: '',
      color: '#3B82F6',
    })
  }

  const handleSave = () => {
    // Convert ReactFlow nodes/edges back to RoadmapNode[]
    const roadmapNodes: RoadmapNode[] = nodes.map((node) => {
      const childNodes = edges
        .filter((edge) => edge.source === node.id)
        .map((edge) => edge.target)
      
      const parentNodes = edges
        .filter((edge) => edge.target === node.id)
        .map((edge) => edge.source)

      return {
        id: node.id,
        title: node.data.label,
        description: node.data.description || '',
        content: node.data.content || '',
        position_x: node.position.x,
        position_y: node.position.y,
        parent_nodes: parentNodes,
        child_nodes: childNodes,
        node_type: node.data.nodeType || 'content',
        linked_roadmap_id: nodeFormData.linked_roadmap_id || undefined,
        linked_article_id: nodeFormData.linked_article_id || undefined,
        linked_url: nodeFormData.linked_url || undefined,
        color: node.data.color || '#3B82F6',
        estimated_time: node.data.estimatedTime || undefined,
        is_completed: false,
        resources: [],
      }
    })

    onSave(roadmapNodes)
  }

  const exportJSON = () => {
    const roadmapNodes: RoadmapNode[] = nodes.map((node) => {
      const childNodes = edges.filter((edge) => edge.source === node.id).map((edge) => edge.target)
      const parentNodes = edges.filter((edge) => edge.target === node.id).map((edge) => edge.source)

      return {
        id: node.id,
        title: node.data.label,
        description: node.data.description || '',
        content: node.data.content || '',
        position_x: node.position.x,
        position_y: node.position.y,
        parent_nodes: parentNodes,
        child_nodes: childNodes,
        node_type: node.data.nodeType || 'content',
        color: node.data.color || '#3B82F6',
        estimated_time: node.data.estimatedTime || undefined,
        is_completed: false,
        resources: [],
      }
    })

    const dataStr = JSON.stringify(roadmapNodes, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'roadmap-nodes.json'
    link.click()
  }

  const importJSON = () => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = '.json'
    input.onchange = (e: any) => {
      const file = e.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (event) => {
          try {
            const importedNodes: RoadmapNode[] = JSON.parse(event.target?.result as string)
            
            const flowNodes: Node[] = importedNodes.map((node) => ({
              id: node.id,
              type: node.node_type || 'content',
              position: { x: node.position_x || 0, y: node.position_y || 0 },
              data: {
                label: node.title,
                description: node.description,
                estimatedTime: node.estimated_time,
                nodeType: node.node_type,
                content: node.content,
                color: node.color,
              },
            }))

            const flowEdges: Edge[] = []
            importedNodes.forEach((node) => {
              node.child_nodes?.forEach((childId) => {
                flowEdges.push({
                  id: `${node.id}-${childId}`,
                  source: node.id,
                  target: childId,
                  type: 'smoothstep',
                  animated: true,
                })
              })
            })

            setNodes(flowNodes)
            setEdges(flowEdges)
            alert('Roadmap imported successfully!')
          } catch (error) {
            alert('Failed to import JSON. Please check the file format.')
          }
        }
        reader.readAsText(file)
      }
    }
    input.click()
  }

  return (
    <div className="w-full h-[600px] border rounded-lg overflow-hidden bg-gray-50">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-right"
      >
        <Controls />
        <MiniMap />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
        
        {!readonly && (
          <Panel position="top-left" className="bg-white p-2 rounded-lg shadow-lg space-y-2">
            <div className="flex flex-col gap-2">
              <button
                onClick={addNewNode}
                className="flex items-center gap-2 px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
              >
                <Plus size={16} />
                Add Node
              </button>
              
              {selectedNode && (
                <>
                  <button
                    onClick={editNode}
                    className="flex items-center gap-2 px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
                  >
                    <Edit2 size={16} />
                    Edit Node
                  </button>
                  <button
                    onClick={deleteNode}
                    className="flex items-center gap-2 px-3 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
                  >
                    <Trash2 size={16} />
                    Delete Node
                  </button>
                </>
              )}
              
              <div className="border-t pt-2 space-y-2">
                <button
                  onClick={importJSON}
                  className="flex items-center gap-2 px-3 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 text-sm w-full"
                >
                  <Upload size={16} />
                  Import JSON
                </button>
                <button
                  onClick={exportJSON}
                  className="flex items-center gap-2 px-3 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 text-sm w-full"
                >
                  <Download size={16} />
                  Export JSON
                </button>
                <button
                  onClick={handleSave}
                  className="flex items-center gap-2 px-3 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 text-sm w-full"
                >
                  <Save size={16} />
                  Save Changes
                </button>
              </div>
            </div>
          </Panel>
        )}

        <Panel position="top-right" className="bg-white p-3 rounded-lg shadow-lg">
          <div className="text-xs space-y-2">
            <div className="font-semibold mb-2">Legend:</div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-500"></div>
              <span>Content Node</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-purple-500"></div>
              <span>Roadmap Link</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span>Article Link</span>
            </div>
          </div>
        </Panel>
      </ReactFlow>

      {/* Node Editor Modal */}
      {showNodeEditor && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">
              {nodeFormData.id && nodes.find(n => n.id === nodeFormData.id) ? 'Edit Node' : 'Add New Node'}
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Node Title *</label>
                <input
                  type="text"
                  value={nodeFormData.title}
                  onChange={(e) => setNodeFormData({ ...nodeFormData, title: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg"
                  placeholder="e.g., Learn React Basics"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <textarea
                  value={nodeFormData.description}
                  onChange={(e) => setNodeFormData({ ...nodeFormData, description: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg"
                  rows={3}
                  placeholder="Brief description of this node"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Node Type *</label>
                <select
                  value={nodeFormData.node_type}
                  onChange={(e) => setNodeFormData({ ...nodeFormData, node_type: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg"
                >
                  <option value="content">Content Node</option>
                  <option value="roadmap_link">Roadmap Link</option>
                  <option value="article_link">Article Link</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Content (Markdown)</label>
                <textarea
                  value={nodeFormData.content}
                  onChange={(e) => setNodeFormData({ ...nodeFormData, content: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg font-mono text-sm"
                  rows={6}
                  placeholder="# Heading\n\nMarkdown content here..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Estimated Time</label>
                <input
                  type="text"
                  value={nodeFormData.estimated_time}
                  onChange={(e) => setNodeFormData({ ...nodeFormData, estimated_time: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg"
                  placeholder="e.g., 2 hours, 1 week"
                />
              </div>

              {nodeFormData.node_type === 'roadmap_link' && (
                <div>
                  <label className="block text-sm font-medium mb-1">Linked Roadmap ID</label>
                  <input
                    type="text"
                    value={nodeFormData.linked_roadmap_id}
                    onChange={(e) => setNodeFormData({ ...nodeFormData, linked_roadmap_id: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg"
                    placeholder="Roadmap ID"
                  />
                </div>
              )}

              {nodeFormData.node_type === 'article_link' && (
                <div>
                  <label className="block text-sm font-medium mb-1">Linked Article ID</label>
                  <input
                    type="text"
                    value={nodeFormData.linked_article_id}
                    onChange={(e) => setNodeFormData({ ...nodeFormData, linked_article_id: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg"
                    placeholder="Article ID"
                  />
                </div>
              )}

              <div>
                <label className="block text-sm font-medium mb-1">External URL (Optional)</label>
                <input
                  type="url"
                  value={nodeFormData.linked_url}
                  onChange={(e) => setNodeFormData({ ...nodeFormData, linked_url: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg"
                  placeholder="https://example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Node Color</label>
                <input
                  type="color"
                  value={nodeFormData.color}
                  onChange={(e) => setNodeFormData({ ...nodeFormData, color: e.target.value })}
                  className="w-full h-10 border rounded-lg"
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={saveNode}
                className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
              >
                Save Node
              </button>
              <button
                onClick={() => {
                  setShowNodeEditor(false)
                  setNodeFormData({
                    id: '',
                    title: '',
                    description: '',
                    content: '',
                    node_type: 'content',
                    estimated_time: '',
                    linked_roadmap_id: '',
                    linked_article_id: '',
                    linked_url: '',
                    color: '#3B82F6',
                  })
                }}
                className="px-4 py-2 border rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
