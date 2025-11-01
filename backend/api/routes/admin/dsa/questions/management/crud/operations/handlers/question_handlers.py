from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import Optional, List

class DSAQuestionHandlers:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db['dsa_questions']
        self.topics_collection = db['dsa_topics']
    
    async def create_question(self, question_data: dict):
        """Create a new DSA question"""
        question_data['created_at'] = datetime.utcnow()
        question_data['updated_at'] = datetime.utcnow()
        
        result = await self.collection.insert_one(question_data)
        created_question = await self.collection.find_one({"_id": result.inserted_id})
        
        created_question['id'] = str(created_question.pop('_id'))
        return {"success": True, "data": created_question}
    
    async def get_all_questions(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        difficulty: Optional[str] = None,
        topics: Optional[str] = None,  # comma-separated topic IDs
        company: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_premium: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ):
        """Get all questions with filtering and sorting"""
        query = {}
        
        if search:
            query['$or'] = [
                {'title': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}}
            ]
        
        if difficulty:
            query['difficulty'] = difficulty
        
        if topics:
            topic_ids = topics.split(',')
            query['topics'] = {'$in': topic_ids}
        
        if company:
            query['companies'] = {'$regex': company, '$options': 'i'}
        
        if is_active is not None:
            query['is_active'] = is_active
        
        if is_premium is not None:
            query['is_premium'] = is_premium
        
        cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        questions = await cursor.to_list(length=limit)
        
        for question in questions:
            question['id'] = str(question.pop('_id'))
        
        total = await self.collection.count_documents(query)
        
        return {
            "success": True,
            "data": questions,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "pages": (total + limit - 1) // limit if limit > 0 else 1
        }
    
    async def get_question(self, question_id: str):
        """Get a single question by ID"""
        if not ObjectId.is_valid(question_id):
            return {"success": False, "error": "Invalid question ID"}
        
        question = await self.collection.find_one({"_id": ObjectId(question_id)})
        
        if not question:
            return {"success": False, "error": "Question not found"}
        
        question['id'] = str(question.pop('_id'))
        return {"success": True, "data": question}
    
    async def update_question(self, question_id: str, update_data: dict):
        """Update a question"""
        if not ObjectId.is_valid(question_id):
            return {"success": False, "error": "Invalid question ID"}
        
        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        if not update_data:
            return {"success": False, "error": "No data to update"}
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = await self.collection.update_one(
            {"_id": ObjectId(question_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return {"success": False, "error": "Question not found"}
        
        updated_question = await self.collection.find_one({"_id": ObjectId(question_id)})
        updated_question['id'] = str(updated_question.pop('_id'))
        
        return {"success": True, "data": updated_question}
    
    async def delete_question(self, question_id: str):
        """Delete a question"""
        if not ObjectId.is_valid(question_id):
            return {"success": False, "error": "Invalid question ID"}
        
        result = await self.collection.delete_one({"_id": ObjectId(question_id)})
        
        if result.deleted_count == 0:
            return {"success": False, "error": "Question not found"}
        
        return {"success": True, "message": "Question deleted successfully"}
    
    async def get_questions_by_difficulty(self):
        """Get question count grouped by difficulty"""
        pipeline = [
            {"$group": {
                "_id": "$difficulty",
                "count": {"$sum": 1}
            }}
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=None)
        
        difficulty_stats = {
            "easy": 0,
            "medium": 0,
            "hard": 0
        }
        
        for item in result:
            difficulty_stats[item['_id']] = item['count']
        
        return {"success": True, "data": difficulty_stats}
    
    async def get_questions_by_topic(self):
        """Get question count grouped by topic"""
        # Get all topics
        topics = await self.topics_collection.find().to_list(length=None)
        
        topic_stats = []
        for topic in topics:
            topic_id = str(topic['_id'])
            count = await self.collection.count_documents({"topics": topic_id})
            
            topic_stats.append({
                "topic_id": topic_id,
                "topic_name": topic.get('name', 'Unknown'),
                "count": count
            })
        
        # Sort by count
        topic_stats.sort(key=lambda x: x['count'], reverse=True)
        
        return {"success": True, "data": topic_stats}
    
    async def increment_submission(self, question_id: str, is_accepted: bool = False):
        """Increment submission count for a question"""
        if not ObjectId.is_valid(question_id):
            return {"success": False, "error": "Invalid question ID"}
        
        update_data = {
            "$inc": {"total_submissions": 1}
        }
        
        if is_accepted:
            update_data["$inc"]["total_accepted"] = 1
        
        result = await self.collection.update_one(
            {"_id": ObjectId(question_id)},
            update_data
        )
        
        if result.matched_count == 0:
            return {"success": False, "error": "Question not found"}
        
        # Calculate acceptance rate
        question = await self.collection.find_one({"_id": ObjectId(question_id)})
        if question['total_submissions'] > 0:
            acceptance_rate = (question['total_accepted'] / question['total_submissions']) * 100
            await self.collection.update_one(
                {"_id": ObjectId(question_id)},
                {"$set": {"acceptance_rate": round(acceptance_rate, 2)}}
            )
        
        return {"success": True, "message": "Submission recorded"}
