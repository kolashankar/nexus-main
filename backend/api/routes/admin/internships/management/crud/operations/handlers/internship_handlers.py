from fastapi import HTTPException
from typing import Optional
from datetime import datetime
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class InternshipHandlers:
    def __init__(self, db):
        self.db = db
        self.collection = db.internships
    
    async def create_internship(self, internship_data: dict) -> dict:
        try:
            internship_data['created_at'] = datetime.utcnow()
            internship_data['updated_at'] = datetime.utcnow()
            
            result = await self.collection.insert_one(internship_data)
            
            if result.inserted_id:
                created = await self.collection.find_one({"_id": result.inserted_id})
                created['_id'] = str(created['_id'])
                return created
            else:
                raise HTTPException(status_code=500, detail="Failed to create internship")
        except Exception as e:
            logger.error(f"Error creating internship: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_all_internships(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category: Optional[str] = None,
        internship_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ) -> dict:
        try:
            filter_query = {}
            
            if search:
                filter_query['$or'] = [
                    {"title": {"$regex": search, "$options": "i"}},
                    {"company": {"$regex": search, "$options": "i"}}
                ]
            
            if category:
                filter_query['category'] = category
            
            if internship_type:
                filter_query['internship_type'] = internship_type
            
            if is_active is not None:
                filter_query['is_active'] = is_active
            
            total = await self.collection.count_documents(filter_query)
            cursor = self.collection.find(filter_query)
            cursor = cursor.sort(sort_by, sort_order).skip(skip).limit(limit)
            
            internships = await cursor.to_list(length=limit)
            
            for internship in internships:
                internship['_id'] = str(internship['_id'])
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "internships": internships
            }
        except Exception as e:
            logger.error(f"Error fetching internships: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_internship_by_id(self, internship_id: str) -> dict:
        try:
            if not ObjectId.is_valid(internship_id):
                raise HTTPException(status_code=400, detail="Invalid internship ID")
            
            internship = await self.collection.find_one({"_id": ObjectId(internship_id)})
            
            if not internship:
                raise HTTPException(status_code=404, detail="Internship not found")
            
            internship['_id'] = str(internship['_id'])
            return internship
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching internship: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def update_internship(self, internship_id: str, update_data: dict) -> dict:
        try:
            if not ObjectId.is_valid(internship_id):
                raise HTTPException(status_code=400, detail="Invalid internship ID")
            
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            if not update_data:
                raise HTTPException(status_code=400, detail="No data to update")
            
            update_data['updated_at'] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(internship_id)},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Internship not found")
            
            updated = await self.collection.find_one({"_id": ObjectId(internship_id)})
            updated['_id'] = str(updated['_id'])
            
            return updated
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating internship: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def delete_internship(self, internship_id: str) -> dict:
        try:
            if not ObjectId.is_valid(internship_id):
                raise HTTPException(status_code=400, detail="Invalid internship ID")
            
            result = await self.collection.delete_one({"_id": ObjectId(internship_id)})
            
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Internship not found")
            
            return {"message": "Internship deleted successfully", "id": internship_id}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting internship: {e}")
            raise HTTPException(status_code=500, detail=str(e))
