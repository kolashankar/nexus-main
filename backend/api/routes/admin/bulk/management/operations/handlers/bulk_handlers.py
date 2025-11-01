from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Dict
import csv
import io
from datetime import datetime
from bson import ObjectId

class BulkOperationsHandlers:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.jobs = db["jobs"]
        self.internships = db["internships"]
        self.scholarships = db["scholarships"]
        self.dsa_questions = db["dsa_questions"]
        self.dsa_topics = db["dsa_topics"]
    
    # ==================== JOBS BULK OPERATIONS ====================
    
    async def export_jobs_csv(self, filters: Dict = {}) -> str:
        """Export jobs to CSV format"""
        jobs_cursor = self.jobs.find(filters)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        headers = ["ID", "Title", "Company", "Location", "Job Type", "Category", "Experience Level", 
                   "Salary Min", "Salary Max", "Description", "Skills", "Qualifications", 
                   "Responsibilities", "Benefits", "Is Active", "Posted Date"]
        writer.writerow(headers)
        
        # Write data
        async for job in jobs_cursor:
            writer.writerow([
                str(job["_id"]),
                job.get("title", ""),
                job.get("company", ""),
                job.get("location", ""),
                job.get("job_type", ""),
                job.get("category", ""),
                job.get("experience_level", ""),
                job.get("salary", {}).get("min", ""),
                job.get("salary", {}).get("max", ""),
                job.get("description", ""),
                ", ".join(job.get("skills", [])),
                ", ".join(job.get("qualifications", [])),
                ", ".join(job.get("responsibilities", [])),
                ", ".join(job.get("benefits", [])),
                job.get("is_active", True),
                job.get("posted_date", datetime.utcnow()).isoformat()
            ])
        
        return output.getvalue()
    
    async def import_jobs_csv(self, csv_data: str) -> Dict:
        """Import jobs from CSV data"""
        reader = csv.DictReader(io.StringIO(csv_data))
        
        success_count = 0
        error_count = 0
        errors = []
        
        for row in reader:
            try:
                job_data = {
                    "title": row.get("Title", ""),
                    "company": row.get("Company", ""),
                    "location": row.get("Location", ""),
                    "job_type": row.get("Job Type", "full_time"),
                    "category": row.get("Category", ""),
                    "experience_level": row.get("Experience Level", "entry"),
                    "salary": {
                        "min": int(row.get("Salary Min", 0)) if row.get("Salary Min") else 0,
                        "max": int(row.get("Salary Max", 0)) if row.get("Salary Max") else 0,
                        "currency": "USD"
                    },
                    "description": row.get("Description", ""),
                    "skills": [s.strip() for s in row.get("Skills", "").split(",") if s.strip()],
                    "qualifications": [q.strip() for q in row.get("Qualifications", "").split(",") if q.strip()],
                    "responsibilities": [r.strip() for r in row.get("Responsibilities", "").split(",") if r.strip()],
                    "benefits": [b.strip() for b in row.get("Benefits", "").split(",") if b.strip()],
                    "is_active": row.get("Is Active", "True").lower() == "true",
                    "posted_date": datetime.utcnow(),
                    "views": 0
                }
                
                await self.jobs.insert_one(job_data)
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Row {reader.line_num}: {str(e)}")
        
        return {
            "success": True,
            "data": {
                "imported": success_count,
                "errors": error_count,
                "error_details": errors
            }
        }
    
    # ==================== INTERNSHIPS BULK OPERATIONS ====================
    
    async def export_internships_csv(self, filters: Dict = {}) -> str:
        """Export internships to CSV format"""
        internships_cursor = self.internships.find(filters)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        headers = ["ID", "Title", "Company", "Location", "Internship Type", "Category", 
                   "Duration", "Stipend", "Description", "Skills", "Qualifications", 
                   "Learning Outcomes", "Is Active", "Posted Date"]
        writer.writerow(headers)
        
        # Write data
        async for internship in internships_cursor:
            writer.writerow([
                str(internship["_id"]),
                internship.get("title", ""),
                internship.get("company", ""),
                internship.get("location", ""),
                internship.get("internship_type", ""),
                internship.get("category", ""),
                internship.get("duration", ""),
                internship.get("stipend", ""),
                internship.get("description", ""),
                ", ".join(internship.get("skills", [])),
                ", ".join(internship.get("qualifications", [])),
                ", ".join(internship.get("learning_outcomes", [])),
                internship.get("is_active", True),
                internship.get("posted_date", datetime.utcnow()).isoformat()
            ])
        
        return output.getvalue()
    
    async def import_internships_csv(self, csv_data: str) -> Dict:
        """Import internships from CSV data"""
        reader = csv.DictReader(io.StringIO(csv_data))
        
        success_count = 0
        error_count = 0
        errors = []
        
        for row in reader:
            try:
                internship_data = {
                    "title": row.get("Title", ""),
                    "company": row.get("Company", ""),
                    "location": row.get("Location", ""),
                    "internship_type": row.get("Internship Type", "remote"),
                    "category": row.get("Category", ""),
                    "duration": row.get("Duration", ""),
                    "stipend": row.get("Stipend", ""),
                    "description": row.get("Description", ""),
                    "skills": [s.strip() for s in row.get("Skills", "").split(",") if s.strip()],
                    "qualifications": [q.strip() for q in row.get("Qualifications", "").split(",") if q.strip()],
                    "learning_outcomes": [l.strip() for l in row.get("Learning Outcomes", "").split(",") if l.strip()],
                    "is_active": row.get("Is Active", "True").lower() == "true",
                    "posted_date": datetime.utcnow(),
                    "views": 0
                }
                
                await self.internships.insert_one(internship_data)
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Row {reader.line_num}: {str(e)}")
        
        return {
            "success": True,
            "data": {
                "imported": success_count,
                "errors": error_count,
                "error_details": errors
            }
        }
    
    # ==================== BULK DELETE OPERATIONS ====================
    
    async def bulk_delete_jobs(self, job_ids: List[str]) -> Dict:
        """Delete multiple jobs"""
        try:
            object_ids = [ObjectId(jid) for jid in job_ids]
            result = await self.jobs.delete_many({"_id": {"$in": object_ids}})
            
            return {
                "success": True,
                "data": {
                    "deleted": result.deleted_count
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def bulk_delete_internships(self, internship_ids: List[str]) -> Dict:
        """Delete multiple internships"""
        try:
            object_ids = [ObjectId(iid) for iid in internship_ids]
            result = await self.internships.delete_many({"_id": {"$in": object_ids}})
            
            return {
                "success": True,
                "data": {
                    "deleted": result.deleted_count
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== BULK UPDATE OPERATIONS ====================
    
    async def bulk_update_jobs_status(self, job_ids: List[str], is_active: bool) -> Dict:
        """Update status for multiple jobs"""
        try:
            object_ids = [ObjectId(jid) for jid in job_ids]
            result = await self.jobs.update_many(
                {"_id": {"$in": object_ids}},
                {"$set": {"is_active": is_active}}
            )
            
            return {
                "success": True,
                "data": {
                    "updated": result.modified_count
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def bulk_update_internships_status(self, internship_ids: List[str], is_active: bool) -> Dict:
        """Update status for multiple internships"""
        try:
            object_ids = [ObjectId(iid) for iid in internship_ids]
            result = await self.internships.update_many(
                {"_id": {"$in": object_ids}},
                {"$set": {"is_active": is_active}}
            )
            
            return {
                "success": True,
                "data": {
                    "updated": result.modified_count
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
