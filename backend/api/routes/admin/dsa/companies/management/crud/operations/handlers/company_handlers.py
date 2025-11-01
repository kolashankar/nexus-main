"""
DSA Company Handlers
8-Level Nested Architecture: routes/admin/dsa/companies/management/crud/operations/handlers/company_handlers.py
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import List, Dict, Any, Optional


class CompanyHandlers:
    """Handlers for DSA Company CRUD operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.dsa_companies
    
    async def create_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new company"""
        company_data["created_at"] = datetime.utcnow()
        company_data["updated_at"] = datetime.utcnow()
        company_data["problem_count"] = 0  # Initialize counts
        company_data["job_count"] = 0
        
        result = await self.collection.insert_one(company_data)
        company_data["_id"] = result.inserted_id
        return self._format_company(company_data)
    
    async def get_companies(
        self,
        skip: int = 0,
        limit: int = 50,
        search: Optional[str] = None,
        industry: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "name",
        sort_order: str = "asc"
    ) -> Dict[str, Any]:
        """Get list of companies with filters"""
        query = {}
        
        # Build query
        if search:
            query["name"] = {"$regex": search, "$options": "i"}
        if industry:
            query["industry"] = industry
        if is_active is not None:
            query["is_active"] = is_active
        
        # Sort
        sort_direction = 1 if sort_order == "asc" else -1
        
        # Get total count
        total = await self.collection.count_documents(query)
        
        # Get companies
        cursor = self.collection.find(query).sort(sort_by, sort_direction).skip(skip).limit(limit)
        companies = await cursor.to_list(length=limit)
        
        return {
            "success": True,
            "companies": [self._format_company(c) for c in companies],
            "total": total,
            "page": (skip // limit) + 1,
            "limit": limit
        }
    
    async def get_company_by_id(self, company_id: str) -> Optional[Dict[str, Any]]:
        """Get single company by ID"""
        try:
            company = await self.collection.find_one({"_id": ObjectId(company_id)})
            return self._format_company(company) if company else None
        except Exception:
            return None
    
    async def update_company(self, company_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update company"""
        try:
            update_data["updated_at"] = datetime.utcnow()
            
            result = await self.collection.find_one_and_update(
                {"_id": ObjectId(company_id)},
                {"$set": update_data},
                return_document=True
            )
            return self._format_company(result) if result else None
        except Exception:
            return None
    
    async def delete_company(self, company_id: str) -> bool:
        """Delete company"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(company_id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get company statistics"""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_companies": {"$sum": 1},
                    "active_companies": {
                        "$sum": {"$cond": [{"$eq": ["$is_active", True]}, 1, 0]}
                    },
                    "total_problems": {"$sum": "$problem_count"},
                    "total_jobs": {"$sum": "$job_count"}
                }
            }
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        
        if result:
            stats = result[0]
            return {
                "success": True,
                "total_companies": stats.get("total_companies", 0),
                "active_companies": stats.get("active_companies", 0),
                "total_problems": stats.get("total_problems", 0),
                "total_jobs": stats.get("total_jobs", 0)
            }
        
        return {
            "success": True,
            "total_companies": 0,
            "active_companies": 0,
            "total_problems": 0,
            "total_jobs": 0
        }
    
    async def get_top_companies(self, limit: int = 10, by: str = "problems") -> List[Dict[str, Any]]:
        """Get top companies by problem count or job count"""
        sort_field = "problem_count" if by == "problems" else "job_count"
        
        cursor = self.collection.find({"is_active": True}).sort(sort_field, -1).limit(limit)
        companies = await cursor.to_list(length=limit)
        
        return [self._format_company(c) for c in companies]
    
    async def increment_problem_count(self, company_id: str) -> bool:
        """Increment problem count for a company"""
        try:
            await self.collection.update_one(
                {"_id": ObjectId(company_id)},
                {"$inc": {"problem_count": 1}}
            )
            return True
        except Exception:
            return False
    
    async def decrement_problem_count(self, company_id: str) -> bool:
        """Decrement problem count for a company"""
        try:
            await self.collection.update_one(
                {"_id": ObjectId(company_id)},
                {"$inc": {"problem_count": -1}}
            )
            return True
        except Exception:
            return False
    
    async def increment_job_count(self, company_id: str) -> bool:
        """Increment job count for a company"""
        try:
            await self.collection.update_one(
                {"_id": ObjectId(company_id)},
                {"$inc": {"job_count": 1}}
            )
            return True
        except Exception:
            return False
    
    async def decrement_job_count(self, company_id: str) -> bool:
        """Decrement job count for a company"""
        try:
            await self.collection.update_one(
                {"_id": ObjectId(company_id)},
                {"$inc": {"job_count": -1}}
            )
            return True
        except Exception:
            return False
    
    def _format_company(self, company: Dict[str, Any]) -> Dict[str, Any]:
        """Format company document for response"""
        if not company:
            return {}
        
        company["id"] = str(company.pop("_id"))
        
        # Format datetime fields
        if "created_at" in company and company["created_at"]:
            company["created_at"] = company["created_at"].isoformat()
        if "updated_at" in company and company["updated_at"]:
            company["updated_at"] = company["updated_at"].isoformat()
        
        return company
