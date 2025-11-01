from fastapi import HTTPException
from typing import Optional
from datetime import datetime
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class ScholarshipHandlers:
    def __init__(self, db):
        self.db = db
        self.collection = db.scholarships
    
    async def create_scholarship(self, scholarship_data: dict) -> dict:
        try:
            scholarship_data['created_at'] = datetime.utcnow()
            scholarship_data['updated_at'] = datetime.utcnow()
            
            result = await self.collection.insert_one(scholarship_data)
            
            if result.inserted_id:
                created = await self.collection.find_one({"_id": result.inserted_id})
                created['_id'] = str(created['_id'])
                return created
            else:
                raise HTTPException(status_code=500, detail="Failed to create scholarship")
        except Exception as e:
            logger.error(f"Error creating scholarship: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_all_scholarships(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        scholarship_type: Optional[str] = None,
        education_level: Optional[str] = None,
        country: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ) -> dict:
        try:
            filter_query = {}
            
            if search:
                filter_query['$or'] = [
                    {"title": {"$regex": search, "$options": "i"}},
                    {"provider": {"$regex": search, "$options": "i"}}
                ]
            
            if scholarship_type:
                filter_query['scholarship_type'] = scholarship_type
            
            if education_level:
                filter_query['education_level'] = education_level
            
            if country:
                filter_query['country'] = country
            
            if is_active is not None:
                filter_query['is_active'] = is_active
            
            total = await self.collection.count_documents(filter_query)
            cursor = self.collection.find(filter_query)
            cursor = cursor.sort(sort_by, sort_order).skip(skip).limit(limit)
            
            scholarships = await cursor.to_list(length=limit)
            
            for scholarship in scholarships:
                scholarship['_id'] = str(scholarship['_id'])
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "scholarships": scholarships
            }
        except Exception as e:
            logger.error(f"Error fetching scholarships: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_scholarship_by_id(self, scholarship_id: str) -> dict:
        try:
            if not ObjectId.is_valid(scholarship_id):
                raise HTTPException(status_code=400, detail="Invalid scholarship ID")
            
            scholarship = await self.collection.find_one({"_id": ObjectId(scholarship_id)})
            
            if not scholarship:
                raise HTTPException(status_code=404, detail="Scholarship not found")
            
            scholarship['_id'] = str(scholarship['_id'])
            return scholarship
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching scholarship: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def update_scholarship(self, scholarship_id: str, update_data: dict) -> dict:
        try:
            if not ObjectId.is_valid(scholarship_id):
                raise HTTPException(status_code=400, detail="Invalid scholarship ID")
            
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            if not update_data:
                raise HTTPException(status_code=400, detail="No data to update")
            
            update_data['updated_at'] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(scholarship_id)},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Scholarship not found")
            
            updated = await self.collection.find_one({"_id": ObjectId(scholarship_id)})
            updated['_id'] = str(updated['_id'])
            
            return updated
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating scholarship: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def delete_scholarship(self, scholarship_id: str) -> dict:
        try:
            if not ObjectId.is_valid(scholarship_id):
                raise HTTPException(status_code=400, detail="Invalid scholarship ID")
            
            result = await self.collection.delete_one({"_id": ObjectId(scholarship_id)})
            
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Scholarship not found")
            
            return {"message": "Scholarship deleted successfully", "id": scholarship_id}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting scholarship: {e}")
            raise HTTPException(status_code=500, detail=str(e))
