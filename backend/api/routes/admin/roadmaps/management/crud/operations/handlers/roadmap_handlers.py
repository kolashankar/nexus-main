"""
Roadmap Handlers
8-Level Nested Architecture: routes/admin/roadmaps/management/crud/operations/handlers/roadmap_handlers.py
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import List, Dict, Any, Optional
import re


class RoadmapHandlers:
    """Handlers for Roadmap CRUD operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.roadmaps
    
    def _calculate_reading_time(self, nodes: List[Dict[str, Any]]) -> str:
        """
        Calculate total reading time based on node content
        Average reading speed: 200 words per minute
        """
        total_words = 0
        
        for node in nodes:
            # Count words from content field
            content = node.get("content", "")
            if content:
                # Remove markdown syntax and count words
                clean_content = re.sub(r'[#*_`\[\]()]', '', content)
                words = len(clean_content.split())
                total_words += words
            
            # Count words from description field
            description = node.get("description", "")
            if description:
                words = len(description.split())
                total_words += words
        
        # Calculate reading time (200 words per minute)
        if total_words == 0:
            return "0 mins"
        
        minutes = total_words // 200
        if minutes == 0:
            return "1 min"
        elif minutes < 60:
            return f"{minutes} mins"
        else:
            hours = minutes // 60
            remaining_mins = minutes % 60
            if remaining_mins == 0:
                return f"{hours} hr{'s' if hours > 1 else ''}"
            else:
                return f"{hours} hr{'s' if hours > 1 else ''} {remaining_mins} mins"
    
    async def create_roadmap(self, roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new roadmap"""
        roadmap_data["created_at"] = datetime.utcnow()
        roadmap_data["updated_at"] = datetime.utcnow()
        roadmap_data["views_count"] = 0
        roadmap_data["followers_count"] = 0
        
        # Auto-calculate reading time based on node content
        nodes = roadmap_data.get("nodes", [])
        if nodes:
            roadmap_data["reading_time"] = self._calculate_reading_time(nodes)
        
        result = await self.collection.insert_one(roadmap_data)
        roadmap_data["_id"] = result.inserted_id
        return self._format_roadmap(roadmap_data)
    
    async def get_roadmaps(
        self,
        skip: int = 0,
        limit: int = 50,
        search: Optional[str] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        difficulty_level: Optional[str] = None,
        is_published: Optional[bool] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Dict[str, Any]:
        """Get list of roadmaps with filters"""
        query = {}
        
        # Build query
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
                {"tags": {"$in": [search]}}
            ]
        if category:
            query["category"] = category
        if subcategory:
            query["subcategory"] = subcategory
        if difficulty_level:
            query["difficulty_level"] = difficulty_level
        if is_published is not None:
            query["is_published"] = is_published
        if is_active is not None:
            query["is_active"] = is_active
        
        # Sort
        sort_direction = 1 if sort_order == "asc" else -1
        
        # Get total count
        total = await self.collection.count_documents(query)
        
        # Get roadmaps
        cursor = self.collection.find(query).sort(sort_by, sort_direction).skip(skip).limit(limit)
        roadmaps = await cursor.to_list(length=limit)
        
        return {
            "success": True,
            "roadmaps": [self._format_roadmap(r) for r in roadmaps],
            "total": total,
            "page": (skip // limit) + 1,
            "limit": limit
        }
    
    async def get_roadmap_by_id(self, roadmap_id: str) -> Optional[Dict[str, Any]]:
        """Get single roadmap by ID"""
        try:
            roadmap = await self.collection.find_one({"_id": ObjectId(roadmap_id)})
            return self._format_roadmap(roadmap) if roadmap else None
        except Exception:
            return None
    
    async def update_roadmap(self, roadmap_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update roadmap"""
        try:
            update_data["updated_at"] = datetime.utcnow()
            
            # Recalculate reading time if nodes are updated
            if "nodes" in update_data and update_data["nodes"]:
                update_data["reading_time"] = self._calculate_reading_time(update_data["nodes"])
            
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(roadmap_id)},
                {"$set": update_data},
                return_document=True
            )
            return self._format_roadmap(result) if result else None
        except Exception:
            return None
    
    async def delete_roadmap(self, roadmap_id: str) -> bool:
        """Delete roadmap"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(roadmap_id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    async def toggle_publish(self, roadmap_id: str) -> Dict[str, Any]:
        """Toggle publish status"""
        try:
            roadmap = await self.collection.find_one({"_id": ObjectId(roadmap_id)})
            if not roadmap:
                return {"success": False, "message": "Roadmap not found"}
            
            new_status = not roadmap.get("is_published", False)
            
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(roadmap_id)},
                {"$set": {"is_published": new_status, "updated_at": datetime.utcnow()}},
                return_document=True
            )
            
            return {
                "success": True,
                "is_published": new_status,
                "roadmap": self._format_roadmap(result)
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def increment_views(self, roadmap_id: str) -> bool:
        """Increment view count"""
        try:
            await self.collection.update_one(
                {"_id": ObjectId(roadmap_id)},
                {"$inc": {"views_count": 1}}
            )
            return True
        except Exception:
            return False
    
    async def add_node(self, roadmap_id: str, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a node to roadmap"""
        try:
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(roadmap_id)},
                {
                    "$push": {"nodes": node_data},
                    "$set": {"updated_at": datetime.utcnow()}
                },
                return_document=True
            )
            return {"success": True, "roadmap": self._format_roadmap(result)} if result else {"success": False}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_node(self, roadmap_id: str, node_id: str, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific node in roadmap"""
        try:
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(roadmap_id), "nodes.id": node_id},
                {
                    "$set": {
                        "nodes.$": node_data,
                        "updated_at": datetime.utcnow()
                    }
                },
                return_document=True
            )
            return {"success": True, "roadmap": self._format_roadmap(result)} if result else {"success": False}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def delete_node(self, roadmap_id: str, node_id: str) -> Dict[str, Any]:
        """Delete a node from roadmap"""
        try:
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(roadmap_id)},
                {
                    "$pull": {"nodes": {"id": node_id}},
                    "$set": {"updated_at": datetime.utcnow()}
                },
                return_document=True
            )
            return {"success": True, "roadmap": self._format_roadmap(result)} if result else {"success": False}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get roadmap statistics"""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_roadmaps": {"$sum": 1},
                    "published_roadmaps": {
                        "$sum": {"$cond": [{"$eq": ["$is_published", True]}, 1, 0]}
                    },
                    "total_views": {"$sum": "$views_count"},
                    "tech_roadmaps": {
                        "$sum": {"$cond": [{"$eq": ["$category", "tech_roadmap"]}, 1, 0]}
                    },
                    "career_roadmaps": {
                        "$sum": {"$cond": [{"$eq": ["$category", "career_roadmap"]}, 1, 0]}
                    }
                }
            }
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        
        if result:
            stats = result[0]
            return {
                "success": True,
                "total_roadmaps": stats.get("total_roadmaps", 0),
                "published_roadmaps": stats.get("published_roadmaps", 0),
                "total_views": stats.get("total_views", 0),
                "tech_roadmaps": stats.get("tech_roadmaps", 0),
                "career_roadmaps": stats.get("career_roadmaps", 0)
            }
        
        return {
            "success": True,
            "total_roadmaps": 0,
            "published_roadmaps": 0,
            "total_views": 0,
            "tech_roadmaps": 0,
            "career_roadmaps": 0
        }
    
    def _format_roadmap(self, roadmap: Dict[str, Any]) -> Dict[str, Any]:
        """Format roadmap document for response"""
        if not roadmap:
            return {}
        
        roadmap["id"] = str(roadmap.pop("_id"))
        
        # Format datetime fields
        if "created_at" in roadmap and roadmap["created_at"]:
            roadmap["created_at"] = roadmap["created_at"].isoformat()
        if "updated_at" in roadmap and roadmap["updated_at"]:
            roadmap["updated_at"] = roadmap["updated_at"].isoformat()
        
        return roadmap
