from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import Optional, List

class DSATopicHandlers:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db['dsa_topics']
        self.questions_collection = db['dsa_questions']
    
    async def create_topic(self, topic_data: dict):
        """Create a new DSA topic"""
        topic_data['created_at'] = datetime.utcnow()
        topic_data['updated_at'] = datetime.utcnow()
        topic_data['question_count'] = 0
        
        result = await self.collection.insert_one(topic_data)
        created_topic = await self.collection.find_one({"_id": result.inserted_id})
        
        created_topic['id'] = str(created_topic.pop('_id'))
        return {"success": True, "data": created_topic}
    
    async def get_all_topics(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        parent_topic: Optional[str] = None,
        sort_by: str = "name",
        sort_order: int = 1
    ):
        """Get all topics with filtering and sorting"""
        query = {}
        
        if search:
            query['name'] = {'$regex': search, '$options': 'i'}
        
        if is_active is not None:
            query['is_active'] = is_active
        
        if parent_topic is not None:
            if parent_topic == "null":
                query['parent_topic'] = None
            else:
                query['parent_topic'] = parent_topic
        
        # Count questions for each topic
        cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        topics = await cursor.to_list(length=limit)
        
        for topic in topics:
            topic['id'] = str(topic.pop('_id'))
            # Count questions with this topic
            topic['question_count'] = await self.questions_collection.count_documents(
                {"topics": topic['id']}
            )
        
        total = await self.collection.count_documents(query)
        
        return {
            "success": True,
            "data": topics,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "pages": (total + limit - 1) // limit if limit > 0 else 1
        }
    
    async def get_topic(self, topic_id: str):
        """Get a single topic by ID"""
        if not ObjectId.is_valid(topic_id):
            return {"success": False, "error": "Invalid topic ID"}
        
        topic = await self.collection.find_one({"_id": ObjectId(topic_id)})
        
        if not topic:
            return {"success": False, "error": "Topic not found"}
        
        topic['id'] = str(topic.pop('_id'))
        
        # Count questions with this topic
        topic['question_count'] = await self.questions_collection.count_documents(
            {"topics": topic['id']}
        )
        
        return {"success": True, "data": topic}
    
    async def update_topic(self, topic_id: str, update_data: dict):
        """Update a topic"""
        if not ObjectId.is_valid(topic_id):
            return {"success": False, "error": "Invalid topic ID"}
        
        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        if not update_data:
            return {"success": False, "error": "No data to update"}
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = await self.collection.update_one(
            {"_id": ObjectId(topic_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return {"success": False, "error": "Topic not found"}
        
        updated_topic = await self.collection.find_one({"_id": ObjectId(topic_id)})
        updated_topic['id'] = str(updated_topic.pop('_id'))
        
        # Count questions
        updated_topic['question_count'] = await self.questions_collection.count_documents(
            {"topics": updated_topic['id']}
        )
        
        return {"success": True, "data": updated_topic}
    
    async def delete_topic(self, topic_id: str):
        """Delete a topic"""
        if not ObjectId.is_valid(topic_id):
            return {"success": False, "error": "Invalid topic ID"}
        
        result = await self.collection.delete_one({"_id": ObjectId(topic_id)})
        
        if result.deleted_count == 0:
            return {"success": False, "error": "Topic not found"}
        
        return {"success": True, "message": "Topic deleted successfully"}
    
    async def get_topic_stats(self):
        """Get statistics for all topics"""
        pipeline = [
            {
                "$lookup": {
                    "from": "dsa_questions",
                    "localField": "_id",
                    "foreignField": "topics",
                    "as": "questions"
                }
            },
            {
                "$project": {
                    "name": 1,
                    "question_count": {"$size": "$questions"},
                    "is_active": 1
                }
            },
            {"$sort": {"question_count": -1}}
        ]
        
        topics = await self.collection.aggregate(pipeline).to_list(length=None)
        
        for topic in topics:
            topic['id'] = str(topic.pop('_id'))
        
        return {"success": True, "data": topics}
