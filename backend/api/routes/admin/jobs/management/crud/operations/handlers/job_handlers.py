from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class JobHandlers:
    def __init__(self, db):
        self.db = db
        self.collection = db.jobs
    
    async def create_job(self, job_data: dict) -> dict:
        """
        Create a new job listing
        """
        try:
            # Ensure is_active is set (default to True if not provided)
            if 'is_active' not in job_data:
                job_data['is_active'] = True
                
            job_data['created_at'] = datetime.utcnow()
            job_data['updated_at'] = datetime.utcnow()
            
            logger.info(f"Creating job: {job_data.get('title', 'Unknown')} at {job_data.get('company', 'Unknown')}")
            
            result = await self.collection.insert_one(job_data)
            
            if result.inserted_id:
                created_job = await self.collection.find_one({"_id": result.inserted_id})
                created_job['_id'] = str(created_job['_id'])
                
                logger.info(f"Job created successfully with ID: {created_job['_id']}, is_active: {created_job.get('is_active')}")
                
                return {
                    "success": True,
                    "message": "Job created successfully",
                    "data": created_job
                }
            else:
                logger.error("Failed to create job - no inserted_id returned")
                raise HTTPException(status_code=500, detail="Failed to create job")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating job: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")
    
    async def get_job_by_id(self, job_id: str) -> dict:
        """
        Get a specific job by ID
        """
        try:
            if not ObjectId.is_valid(job_id):
                raise HTTPException(status_code=400, detail="Invalid job ID")
            
            job = await self.collection.find_one({"_id": ObjectId(job_id)})
            
            if not job:
                raise HTTPException(status_code=404, detail="Job not found")
            
            job['_id'] = str(job['_id'])
            return job
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching job: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_all_jobs(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category: Optional[str] = None,
        job_type: Optional[str] = None,
        experience_level: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ) -> dict:
        """
        Get all jobs with filtering, searching, and sorting
        """
        try:
            # Build filter query
            filter_query = {}
            
            if search:
                filter_query['$or'] = [
                    {"title": {"$regex": search, "$options": "i"}},
                    {"company": {"$regex": search, "$options": "i"}},
                    {"description": {"$regex": search, "$options": "i"}}
                ]
            
            if category:
                filter_query['category'] = category
            
            if job_type:
                filter_query['job_type'] = job_type
            
            if experience_level:
                filter_query['experience_level'] = experience_level
            
            if is_active is not None:
                filter_query['is_active'] = is_active
            
            logger.info(f"Fetching jobs with filters: {filter_query}, is_active filter: {is_active}")
            
            # Get total count
            total = await self.collection.count_documents(filter_query)
            
            logger.info(f"Total jobs matching filters: {total}")
            
            # Get jobs with pagination and sorting
            cursor = self.collection.find(filter_query)
            cursor = cursor.sort(sort_by, sort_order).skip(skip).limit(limit)
            
            jobs = await cursor.to_list(length=limit)
            
            # Convert ObjectId to string
            for job in jobs:
                job['_id'] = str(job['_id'])
            
            logger.info(f"Returning {len(jobs)} jobs (skip: {skip}, limit: {limit})")
            
            return {
                "success": True,
                "total": total,
                "skip": skip,
                "limit": limit,
                "data": jobs,
                "jobs": jobs  # Keep backward compatibility
            }
        except Exception as e:
            logger.error(f"Error fetching jobs: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to fetch jobs: {str(e)}")
    
    async def update_job(self, job_id: str, update_data: dict) -> dict:
        """
        Update a job listing
        """
        try:
            if not ObjectId.is_valid(job_id):
                raise HTTPException(status_code=400, detail="Invalid job ID")
            
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            if not update_data:
                raise HTTPException(status_code=400, detail="No data to update")
            
            update_data['updated_at'] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(job_id)},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Job not found")
            
            updated_job = await self.collection.find_one({"_id": ObjectId(job_id)})
            updated_job['_id'] = str(updated_job['_id'])
            
            return updated_job
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating job: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def delete_job(self, job_id: str) -> dict:
        """
        Delete a job listing
        """
        try:
            if not ObjectId.is_valid(job_id):
                raise HTTPException(status_code=400, detail="Invalid job ID")
            
            result = await self.collection.delete_one({"_id": ObjectId(job_id)})
            
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Job not found")
            
            return {"message": "Job deleted successfully", "id": job_id}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting job: {e}")
            raise HTTPException(status_code=500, detail=str(e))
