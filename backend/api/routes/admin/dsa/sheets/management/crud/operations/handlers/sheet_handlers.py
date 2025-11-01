from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import Optional, List

class DSASheetHandlers:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db['dsa_sheets']
        self.questions_collection = db['dsa_questions']
    
    async def create_sheet(self, sheet_data: dict):
        """Create a new DSA sheet"""
        sheet_data['created_at'] = datetime.utcnow()
        sheet_data['updated_at'] = datetime.utcnow()
        
        # Calculate total questions if questions are provided
        if 'questions' in sheet_data:
            sheet_data['total_questions'] = len(sheet_data['questions'])
        
        result = await self.collection.insert_one(sheet_data)
        created_sheet = await self.collection.find_one({"_id": result.inserted_id})
        
        created_sheet['id'] = str(created_sheet.pop('_id'))
        return {"success": True, "data": created_sheet}
    
    async def get_all_sheets(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        level: Optional[str] = None,
        tag: Optional[str] = None,
        is_published: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        is_premium: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ):
        """Get all sheets with filtering and sorting"""
        query = {}
        
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}},
                {'author': {'$regex': search, '$options': 'i'}}
            ]
        
        if level:
            query['level'] = level
        
        if tag:
            query['tags'] = tag
        
        if is_published is not None:
            query['is_published'] = is_published
        
        if is_featured is not None:
            query['is_featured'] = is_featured
        
        if is_premium is not None:
            query['is_premium'] = is_premium
        
        cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        sheets = await cursor.to_list(length=limit)
        
        for sheet in sheets:
            sheet['id'] = str(sheet.pop('_id'))
        
        total = await self.collection.count_documents(query)
        
        return {
            "success": True,
            "data": sheets,
            "total": total,
            "page": skip // limit + 1 if limit > 0 else 1,
            "pages": (total + limit - 1) // limit if limit > 0 else 1
        }
    
    async def get_sheet(self, sheet_id: str):
        """Get a single sheet by ID"""
        if not ObjectId.is_valid(sheet_id):
            return {"success": False, "error": "Invalid sheet ID"}
        
        sheet = await self.collection.find_one({"_id": ObjectId(sheet_id)})
        
        if not sheet:
            return {"success": False, "error": "Sheet not found"}
        
        sheet['id'] = str(sheet.pop('_id'))
        return {"success": True, "data": sheet}
    
    async def update_sheet(self, sheet_id: str, update_data: dict):
        """Update a sheet"""
        if not ObjectId.is_valid(sheet_id):
            return {"success": False, "error": "Invalid sheet ID"}
        
        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        if not update_data:
            return {"success": False, "error": "No data to update"}
        
        update_data['updated_at'] = datetime.utcnow()
        
        # Update total_questions if questions array is updated
        if 'questions' in update_data:
            update_data['total_questions'] = len(update_data['questions'])
        
        result = await self.collection.update_one(
            {"_id": ObjectId(sheet_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return {"success": False, "error": "Sheet not found"}
        
        updated_sheet = await self.collection.find_one({"_id": ObjectId(sheet_id)})
        updated_sheet['id'] = str(updated_sheet.pop('_id'))
        
        return {"success": True, "data": updated_sheet}
    
    async def delete_sheet(self, sheet_id: str):
        """Delete a sheet"""
        if not ObjectId.is_valid(sheet_id):
            return {"success": False, "error": "Invalid sheet ID"}
        
        result = await self.collection.delete_one({"_id": ObjectId(sheet_id)})
        
        if result.deleted_count == 0:
            return {"success": False, "error": "Sheet not found"}
        
        return {"success": True, "message": "Sheet deleted successfully"}
    
    async def add_question_to_sheet(self, sheet_id: str, question_id: str, order: int = 0):
        """Add a question to a sheet"""
        if not ObjectId.is_valid(sheet_id):
            return {"success": False, "error": "Invalid sheet ID"}
        
        if not ObjectId.is_valid(question_id):
            return {"success": False, "error": "Invalid question ID"}
        
        # Check if question exists
        question = await self.questions_collection.find_one({"_id": ObjectId(question_id)})
        if not question:
            return {"success": False, "error": "Question not found"}
        
        # Add question to sheet
        question_entry = {
            "question_id": question_id,
            "order": order,
            "is_completed": False
        }
        
        result = await self.collection.update_one(
            {"_id": ObjectId(sheet_id)},
            {
                "$push": {"questions": question_entry},
                "$inc": {"total_questions": 1},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if result.matched_count == 0:
            return {"success": False, "error": "Sheet not found"}
        
        return {"success": True, "message": "Question added to sheet"}
    
    async def remove_question_from_sheet(self, sheet_id: str, question_id: str):
        """Remove a question from a sheet"""
        if not ObjectId.is_valid(sheet_id):
            return {"success": False, "error": "Invalid sheet ID"}
        
        result = await self.collection.update_one(
            {"_id": ObjectId(sheet_id)},
            {
                "$pull": {"questions": {"question_id": question_id}},
                "$inc": {"total_questions": -1},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if result.matched_count == 0:
            return {"success": False, "error": "Sheet not found"}
        
        return {"success": True, "message": "Question removed from sheet"}
    
    async def toggle_publish(self, sheet_id: str):
        """Toggle publish status of a sheet"""
        if not ObjectId.is_valid(sheet_id):
            return {"success": False, "error": "Invalid sheet ID"}
        
        sheet = await self.collection.find_one({"_id": ObjectId(sheet_id)})
        if not sheet:
            return {"success": False, "error": "Sheet not found"}
        
        new_status = not sheet.get('is_published', False)
        
        await self.collection.update_one(
            {"_id": ObjectId(sheet_id)},
            {
                "$set": {
                    "is_published": new_status,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "success": True,
            "message": f"Sheet {'published' if new_status else 'unpublished'}",
            "is_published": new_status
        }
    
    async def get_sheet_stats(self):
        """Get statistics for sheets"""
        total_sheets = await self.collection.count_documents({})
        published_sheets = await self.collection.count_documents({"is_published": True})
        featured_sheets = await self.collection.count_documents({"is_featured": True})
        
        # Get sheets by level
        pipeline = [
            {"$group": {
                "_id": "$level",
                "count": {"$sum": 1}
            }}
        ]
        
        level_stats = await self.collection.aggregate(pipeline).to_list(length=None)
        
        return {
            "success": True,
            "data": {
                "total_sheets": total_sheets,
                "published_sheets": published_sheets,
                "featured_sheets": featured_sheets,
                "by_level": {item['_id']: item['count'] for item in level_stats}
            }
        }
