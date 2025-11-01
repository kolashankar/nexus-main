"""
Gemini Roadmap Generator
8-Level Nested Architecture: utils/ai/gemini/generators/roadmaps/prompts/generator.py
"""

import google.generativeai as genai
import json
import re
from typing import Dict, Any


class GeminiRoadmapGenerator:
    """Generate roadmaps using Gemini AI"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')
    
    async def generate_roadmap(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete roadmap with node-based structure
        
        Args:
            prompt_data: dict with keys:
                - title: Roadmap title
                - category: tech_roadmap or career_roadmap
                - subcategory: Specific subcategory
                - difficulty_level: beginner, intermediate, advanced
                - target_audience: Target audience description (optional)
                - focus_areas: List of specific topics to focus on (optional)
                - estimated_duration: Desired duration (optional)
        """
        title = prompt_data.get("title", "")
        category = prompt_data.get("category", "tech_roadmap")
        subcategory = prompt_data.get("subcategory", "full_stack")
        difficulty_level = prompt_data.get("difficulty_level", "beginner")
        target_audience = prompt_data.get("target_audience", "beginners")
        focus_areas = prompt_data.get("focus_areas", [])
        estimated_duration = prompt_data.get("estimated_duration", "3-6 months")
        
        focus_text = ""
        if focus_areas:
            focus_text = f"\n\nSpecific focus areas:\n" + "\n".join([f"- {area}" for area in focus_areas])
        
        prompt = f"""
You are an expert career advisor and tech educator. Generate a comprehensive visual roadmap with node-based structure.

Roadmap Title: {title}
Category: {category}
Subcategory: {subcategory}
Difficulty Level: {difficulty_level}
Target Audience: {target_audience}
Estimated Duration: {estimated_duration}
{focus_text}

Generate a complete roadmap in JSON format with the following structure:

{{
    "title": "{title}",
    "description": "Comprehensive description of what learners will achieve (200-300 words)",
    "category": "{category}",
    "subcategory": "{subcategory}",
    "difficulty_level": "{difficulty_level}",
    "estimated_duration": "{estimated_duration}",
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "nodes": [
        {{
            "id": "node_1",
            "title": "Node Title",
            "description": "What this node covers (100-150 words)",
            "content": "Full content in Markdown format (300-500 words). Include learning objectives, key concepts, practical examples, and exercises.",
            "position_x": 100,
            "position_y": 100,
            "parent_nodes": [],
            "child_nodes": ["node_2", "node_3"],
            "node_type": "content",
            "color": "#3B82F6",
            "icon": "book",
            "estimated_time": "1 week",
            "resources": [
                {{"title": "Resource Name", "url": "https://example.com"}},
                {{"title": "Another Resource", "url": "https://example.com"}}
            ]
        }}
    ]
}}

Requirements:
1. Create 15-25 nodes representing the complete learning path
2. Nodes should have logical prerequisites (parent_nodes) and progressions (child_nodes)
3. Position nodes in a visual flow:
   - Start nodes at position_x: 100-200, position_y: 100
   - Each level increases position_y by 150-200
   - Parallel paths have different position_x values (200, 500, 800 apart)
4. Node types:
   - "content": Regular learning node with full content
   - Use "content" for all nodes in this generation
5. Color codes (hex):
   - Beginner topics: #3B82F6 (blue)
   - Intermediate topics: #8B5CF6 (purple)
   - Advanced topics: #EF4444 (red)
   - Practice/Projects: #10B981 (green)
6. Icons: book, code, wrench, star, rocket, target, lightbulb, award, etc.
7. Each node should have:
   - Detailed content in Markdown (300-500 words)
   - 2-4 learning resources with real URLs
   - Realistic estimated_time (hours, days, weeks)
8. Create a logical progression from basics to advanced
9. Include practical projects/milestones every 4-5 nodes
10. Add 5-7 relevant tags for the entire roadmap

IMPORTANT: 
- Respond ONLY with valid JSON, no additional text
- Ensure parent_nodes and child_nodes IDs match actual node IDs
- Create a connected graph where most nodes have both parents and children (except start and end nodes)
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                roadmap_data = json.loads(json_match.group())
            else:
                roadmap_data = json.loads(response_text)
            
            # Ensure all required fields are present
            roadmap_data.setdefault("title", title)
            roadmap_data.setdefault("category", category)
            roadmap_data.setdefault("subcategory", subcategory)
            roadmap_data.setdefault("difficulty_level", difficulty_level)
            roadmap_data.setdefault("estimated_duration", estimated_duration)
            roadmap_data.setdefault("tags", [])
            roadmap_data.setdefault("nodes", [])
            roadmap_data.setdefault("author", "AI Generated")
            roadmap_data.setdefault("is_published", False)
            roadmap_data.setdefault("is_active", True)
            
            # Validate nodes structure
            for node in roadmap_data.get("nodes", []):
                node.setdefault("parent_nodes", [])
                node.setdefault("child_nodes", [])
                node.setdefault("node_type", "content")
                node.setdefault("color", "#3B82F6")
                node.setdefault("icon", "book")
                node.setdefault("resources", [])
                node.setdefault("is_completed", False)
            
            return roadmap_data
            
        except Exception as e:
            # Return a basic roadmap structure if AI generation fails
            return {
                "title": title,
                "description": f"A comprehensive roadmap for {title}",
                "category": category,
                "subcategory": subcategory,
                "difficulty_level": difficulty_level,
                "estimated_duration": estimated_duration,
                "tags": [subcategory, difficulty_level],
                "author": "AI Generated",
                "nodes": [],
                "is_published": False,
                "is_active": True,
                "error": f"AI generation failed: {str(e)}"
            }
