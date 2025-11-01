from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import Optional, List, Dict

class ArticleHandlers:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db["articles"]
    
    async def create_article(self, article_data: dict) -> dict:
        """Create a new article"""
        article_data["views_count"] = 0
        article_data["created_at"] = datetime.utcnow()
        article_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(article_data)
        article_data["_id"] = result.inserted_id
        
        return {
            "success": True,
            "message": "Article created successfully",
            "data": self._format_article(article_data)
        }
    
    async def get_all_articles(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        is_published: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ) -> dict:
        """Get all articles with filtering and sorting"""
        query = {}
        
        # Search in title, content, excerpt
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}},
                {"excerpt": {"$regex": search, "$options": "i"}},
                {"author": {"$regex": search, "$options": "i"}}
            ]
        
        # Filter by category
        if category:
            query["category"] = category
        
        # Filter by tags
        if tags:
            query["tags"] = {"$in": tags}
        
        # Filter by published status
        if is_published is not None:
            query["is_published"] = is_published
        
        # Get total count
        total = await self.collection.count_documents(query)
        
        # Get articles with pagination and sorting
        cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        articles = await cursor.to_list(length=limit)
        
        return {
            "success": True,
            "data": [self._format_article(article) for article in articles],
            "total": total,
            "skip": skip,
            "limit": limit
        }
    
    async def get_article_by_id(self, article_id: str) -> dict:
        """Get a single article by ID"""
        if not ObjectId.is_valid(article_id):
            return {"success": False, "message": "Invalid article ID"}
        
        article = await self.collection.find_one({"_id": ObjectId(article_id)})
        
        if not article:
            return {"success": False, "message": "Article not found"}
        
        # Increment view count
        await self.collection.update_one(
            {"_id": ObjectId(article_id)},
            {"$inc": {"views_count": 1}}
        )
        article["views_count"] += 1
        
        return {
            "success": True,
            "data": self._format_article(article)
        }
    
    async def update_article(self, article_id: str, update_data: dict) -> dict:
        """Update an article"""
        if not ObjectId.is_valid(article_id):
            return {"success": False, "message": "Invalid article ID"}
        
        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        if not update_data:
            return {"success": False, "message": "No data to update"}
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return {"success": False, "message": "Article not found"}
        
        updated_article = await self.collection.find_one({"_id": ObjectId(article_id)})
        
        return {
            "success": True,
            "message": "Article updated successfully",
            "data": self._format_article(updated_article)
        }
    
    async def delete_article(self, article_id: str) -> dict:
        """Delete an article"""
        if not ObjectId.is_valid(article_id):
            return {"success": False, "message": "Invalid article ID"}
        
        result = await self.collection.delete_one({"_id": ObjectId(article_id)})
        
        if result.deleted_count == 0:
            return {"success": False, "message": "Article not found"}
        
        return {
            "success": True,
            "message": "Article deleted successfully"
        }
    
    async def toggle_publish_status(self, article_id: str) -> dict:
        """Toggle article publish status"""
        if not ObjectId.is_valid(article_id):
            return {"success": False, "message": "Invalid article ID"}
        
        article = await self.collection.find_one({"_id": ObjectId(article_id)})
        
        if not article:
            return {"success": False, "message": "Article not found"}
        
        new_status = not article.get("is_published", True)
        
        await self.collection.update_one(
            {"_id": ObjectId(article_id)},
            {"$set": {"is_published": new_status, "updated_at": datetime.utcnow()}}
        )
        
        return {
            "success": True,
            "message": f"Article {'published' if new_status else 'unpublished'} successfully",
            "is_published": new_status
        }
    
    def _format_article(self, article: dict) -> dict:
        """Format article for response"""
        return {
            "id": str(article["_id"]),
            "title": article.get("title", ""),
            "content": article.get("content", ""),
            "excerpt": article.get("excerpt"),
            "author": article.get("author", ""),
            "tags": article.get("tags", []),
            "category": article.get("category", ""),
            "cover_image": article.get("cover_image"),
            "read_time": article.get("read_time"),
            "is_published": article.get("is_published", True),
            "views_count": article.get("views_count", 0),
            "created_at": article.get("created_at"),
            "updated_at": article.get("updated_at")
        }
