"""
Roadmap Model
8-Level Nested Architecture: models/schemas/roadmaps/fields/validators/custom/roadmap_model.py
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class RoadmapNode(BaseModel):
    """Individual node in a roadmap"""
    id: str = Field(..., description="Unique node ID")
    title: str = Field(..., description="Node title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Node description")
    content: Optional[str] = Field(None, description="Full content (markdown format)")
    
    # Node positioning
    position_x: float = Field(default=0, description="X coordinate for visual display")
    position_y: float = Field(default=0, description="Y coordinate for visual display")
    
    # Node connections
    parent_nodes: List[str] = Field(default=[], description="IDs of parent nodes (prerequisite nodes)")
    child_nodes: List[str] = Field(default=[], description="IDs of child nodes (next nodes)")
    
    # Node type and links
    node_type: str = Field(default="content", description="Type: content, roadmap_link, article_link, chapter_link")
    linked_roadmap_id: Optional[str] = Field(None, description="ID of linked roadmap (if node_type=roadmap_link)")
    linked_article_id: Optional[str] = Field(None, description="ID of linked article (if node_type=article_link)")
    linked_url: Optional[str] = Field(None, description="External URL or chapter link")
    
    # Visual styling
    color: Optional[str] = Field("#3B82F6", description="Node color (hex code)")
    icon: Optional[str] = Field(None, description="Icon identifier")
    
    # Progress tracking
    is_completed: bool = Field(default=False, description="Whether node is completed")
    estimated_time: Optional[str] = Field(None, description="Estimated completion time (e.g., '2 hours', '1 week')")
    
    # Resources
    resources: List[Dict[str, str]] = Field(default=[], description="Additional resources [{title, url}]")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "node_1",
                "title": "Introduction to React",
                "description": "Learn React fundamentals",
                "content": "# React Basics\n\nReact is a JavaScript library...",
                "position_x": 100,
                "position_y": 200,
                "parent_nodes": [],
                "child_nodes": ["node_2", "node_3"],
                "node_type": "content",
                "color": "#3B82F6",
                "estimated_time": "2 hours",
                "resources": [
                    {"title": "Official Docs", "url": "https://react.dev"}
                ]
            }
        }


class Roadmap(BaseModel):
    """Roadmap model with visual node-based structure"""
    id: Optional[str] = Field(None, description="Roadmap ID (MongoDB _id)")
    title: str = Field(..., description="Roadmap title", min_length=1, max_length=200)
    description: str = Field(..., description="Roadmap description")
    cover_image: Optional[str] = Field(None, description="Cover image URL or base64")
    
    # Categories
    category: str = Field(..., description="Category: tech_roadmap, career_roadmap")
    subcategory: str = Field(..., description="Subcategory: full_stack, frontend, backend, after_10th, after_12th, after_btech, etc.")
    
    # Nodes
    nodes: List[RoadmapNode] = Field(default=[], description="Roadmap nodes")
    
    # Metadata
    author: str = Field(default="Admin", description="Author name")
    difficulty_level: str = Field(default="beginner", description="Difficulty: beginner, intermediate, advanced")
    estimated_duration: Optional[str] = Field(None, description="Total estimated duration (e.g., '3 months')")
    reading_time: Optional[str] = Field(None, description="Auto-calculated total reading time based on content (e.g., '45 mins')")
    tags: List[str] = Field(default=[], description="Tags for categorization")
    
    # Engagement
    views_count: int = Field(default=0, description="Number of views")
    followers_count: int = Field(default=0, description="Number of followers")
    
    # Status
    is_published: bool = Field(default=False, description="Whether roadmap is published")
    is_active: bool = Field(default=True, description="Whether roadmap is active")
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Full Stack Developer Roadmap 2025",
                "description": "Complete guide to becoming a full stack developer",
                "category": "tech_roadmap",
                "subcategory": "full_stack",
                "difficulty_level": "beginner",
                "estimated_duration": "6 months",
                "tags": ["web development", "full stack", "javascript", "python"],
                "nodes": [
                    {
                        "id": "node_1",
                        "title": "HTML & CSS Basics",
                        "description": "Learn web fundamentals",
                        "node_type": "content",
                        "position_x": 100,
                        "position_y": 100
                    }
                ]
            }
        }


class RoadmapCreate(BaseModel):
    """Schema for creating a new roadmap"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str
    cover_image: Optional[str] = None
    category: str
    subcategory: str
    author: str = "Admin"
    difficulty_level: str = "beginner"
    estimated_duration: Optional[str] = None
    tags: List[str] = []
    nodes: List[RoadmapNode] = []
    is_published: bool = False


class RoadmapUpdate(BaseModel):
    """Schema for updating a roadmap"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    cover_image: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    author: Optional[str] = None
    difficulty_level: Optional[str] = None
    estimated_duration: Optional[str] = None
    tags: Optional[List[str]] = None
    nodes: Optional[List[RoadmapNode]] = None
    is_published: Optional[bool] = None
    is_active: Optional[bool] = None


class RoadmapAIGenerate(BaseModel):
    """Schema for AI roadmap generation"""
    title: str = Field(..., description="Roadmap title")
    category: str = Field(..., description="tech_roadmap or career_roadmap")
    subcategory: str = Field(..., description="Specific subcategory")
    difficulty_level: str = Field(default="beginner", description="Target difficulty level")
    target_audience: Optional[str] = Field(None, description="Target audience description")
    focus_areas: List[str] = Field(default=[], description="Specific topics to focus on")
    estimated_duration: Optional[str] = Field(None, description="Desired duration")
