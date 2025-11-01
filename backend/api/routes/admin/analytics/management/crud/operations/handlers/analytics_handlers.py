from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from bson import ObjectId
import asyncio

class AnalyticsHandlers:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.user_activities = db["user_activities"]
        self.api_usage_logs = db["api_usage_logs"]
        self.gemini_api_logs = db["gemini_api_logs"]
        self.admin_users = db["admin_users"]
        self.app_users = db["app_users"]
        self.jobs = db["jobs"]
        self.applications = db["applications"]
    
    async def get_user_engagement_metrics(self) -> Dict:
        """Get user engagement metrics"""
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        week_start = now - timedelta(days=7)
        month_start = now - timedelta(days=30)
        
        # Total users (admin + app users)
        total_admins = await self.admin_users.count_documents({})
        total_app_users = await self.app_users.count_documents({})
        total_users = total_admins + total_app_users
        
        # Active users (based on user_activities)
        active_today = await self.user_activities.distinct("user_id", {"timestamp": {"$gte": today_start}})
        active_week = await self.user_activities.distinct("user_id", {"timestamp": {"$gte": week_start}})
        active_month = await self.user_activities.distinct("user_id", {"timestamp": {"$gte": month_start}})
        
        # Total sessions
        total_sessions = await self.user_activities.count_documents({})
        
        # Average session duration (mock calculation based on activities)
        avg_session_duration = 5.5  # Average in minutes
        
        return {
            "total_users": total_users,
            "active_users_today": len(active_today),
            "active_users_week": len(active_week),
            "active_users_month": len(active_month),
            "avg_session_duration": avg_session_duration,
            "total_sessions": total_sessions
        }
    
    async def get_job_application_metrics(self) -> Dict:
        """Get job application statistics"""
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        week_start = now - timedelta(days=7)
        month_start = now - timedelta(days=30)
        
        # Total applications
        total_applications = await self.applications.count_documents({}) if await self.db.list_collection_names().__contains__("applications") else 0
        
        # Applications by time period
        applications_today = await self.applications.count_documents({"applied_at": {"$gte": today_start}}) if total_applications > 0 else 0
        applications_week = await self.applications.count_documents({"applied_at": {"$gte": week_start}}) if total_applications > 0 else 0
        applications_month = await self.applications.count_documents({"applied_at": {"$gte": month_start}}) if total_applications > 0 else 0
        
        # Total jobs
        total_jobs = await self.jobs.count_documents({})
        
        # Average applications per job
        avg_applications_per_job = total_applications / total_jobs if total_jobs > 0 else 0
        
        # Top jobs by applications (mock data for now)
        top_jobs_pipeline = [
            {"$match": {}},
            {"$sort": {"views": -1}},
            {"$limit": 5},
            {"$project": {"title": 1, "company": 1, "views": 1}}
        ]
        
        top_jobs_cursor = self.jobs.aggregate(top_jobs_pipeline)
        top_jobs = []
        async for job in top_jobs_cursor:
            top_jobs.append({
                "id": str(job["_id"]),
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "applications": job.get("views", 0)
            })
        
        return {
            "total_applications": total_applications,
            "applications_today": applications_today,
            "applications_week": applications_week,
            "applications_month": applications_month,
            "avg_applications_per_job": round(avg_applications_per_job, 2),
            "top_jobs": top_jobs
        }
    
    async def get_gemini_api_usage_metrics(self) -> Dict:
        """Get Gemini API usage tracking"""
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        week_start = now - timedelta(days=7)
        month_start = now - timedelta(days=30)
        
        # Total requests
        total_requests = await self.gemini_api_logs.count_documents({})
        
        # Requests by time period
        requests_today = await self.gemini_api_logs.count_documents({"timestamp": {"$gte": today_start}})
        requests_week = await self.gemini_api_logs.count_documents({"timestamp": {"$gte": week_start}})
        requests_month = await self.gemini_api_logs.count_documents({"timestamp": {"$gte": month_start}})
        
        # By feature
        by_feature_pipeline = [
            {"$group": {"_id": "$feature", "count": {"$sum": 1}}}
        ]
        by_feature_cursor = self.gemini_api_logs.aggregate(by_feature_pipeline)
        by_feature = {}
        async for item in by_feature_cursor:
            by_feature[item["_id"]] = item["count"]
        
        # Average response time
        avg_response_pipeline = [
            {"$group": {"_id": None, "avg_time": {"$avg": "$response_time"}}}
        ]
        avg_response_cursor = self.gemini_api_logs.aggregate(avg_response_pipeline)
        avg_response_time = 0.0
        async for item in avg_response_cursor:
            avg_response_time = item.get("avg_time", 0.0)
        
        return {
            "total_requests": total_requests,
            "requests_today": requests_today,
            "requests_week": requests_week,
            "requests_month": requests_month,
            "by_feature": by_feature,
            "avg_response_time": round(avg_response_time, 3)
        }
    
    async def get_dashboard_analytics(self) -> Dict:
        """Get complete analytics dashboard data"""
        user_engagement, job_applications, gemini_usage = await asyncio.gather(
            self.get_user_engagement_metrics(),
            self.get_job_application_metrics(),
            self.get_gemini_api_usage_metrics()
        )
        
        return {
            "success": True,
            "data": {
                "user_engagement": user_engagement,
                "job_applications": job_applications,
                "gemini_api_usage": gemini_usage,
                "generated_at": datetime.utcnow().isoformat()
            }
        }
    
    async def log_user_activity(self, user_id: Optional[str], session_id: str, action: str, module: str, metadata: Dict = {}) -> Dict:
        """Log user activity"""
        activity = {
            "user_id": user_id,
            "session_id": session_id,
            "action": action,
            "module": module,
            "metadata": metadata,
            "timestamp": datetime.utcnow()
        }
        
        result = await self.user_activities.insert_one(activity)
        return {"success": True, "id": str(result.inserted_id)}
    
    async def log_api_usage(self, endpoint: str, method: str, user_id: Optional[str], status_code: int, response_time: float, error_message: Optional[str] = None) -> Dict:
        """Log API usage"""
        log_entry = {
            "endpoint": endpoint,
            "method": method,
            "user_id": user_id,
            "status_code": status_code,
            "response_time": response_time,
            "error_message": error_message,
            "timestamp": datetime.utcnow()
        }
        
        result = await self.api_usage_logs.insert_one(log_entry)
        return {"success": True, "id": str(result.inserted_id)}
    
    async def log_gemini_api_usage(self, feature: str, response_time: float, success: bool = True, error_message: Optional[str] = None, user_id: Optional[str] = None) -> Dict:
        """Log Gemini API usage"""
        log_entry = {
            "feature": feature,
            "response_time": response_time,
            "success": success,
            "error_message": error_message,
            "user_id": user_id,
            "timestamp": datetime.utcnow()
        }
        
        result = await self.gemini_api_logs.insert_one(log_entry)
        return {"success": True, "id": str(result.inserted_id)}
    
    async def get_api_usage_logs(self, limit: int = 100, skip: int = 0, status_code: Optional[int] = None) -> Dict:
        """Get API usage logs with filters"""
        query = {}
        if status_code:
            query["status_code"] = status_code
        
        logs_cursor = self.api_usage_logs.find(query).sort("timestamp", -1).skip(skip).limit(limit)
        logs = []
        async for log in logs_cursor:
            log["_id"] = str(log["_id"])
            log["timestamp"] = log["timestamp"].isoformat()
            logs.append(log)
        
        total = await self.api_usage_logs.count_documents(query)
        
        return {
            "success": True,
            "data": logs,
            "total": total,
            "page": skip // limit + 1,
            "limit": limit
        }
    
    async def get_error_logs(self, limit: int = 100, skip: int = 0) -> Dict:
        """Get error logs (API calls with status code >= 400)"""
        query = {"status_code": {"$gte": 400}}
        
        logs_cursor = self.api_usage_logs.find(query).sort("timestamp", -1).skip(skip).limit(limit)
        logs = []
        async for log in logs_cursor:
            log["_id"] = str(log["_id"])
            log["timestamp"] = log["timestamp"].isoformat()
            logs.append(log)
        
        total = await self.api_usage_logs.count_documents(query)
        
        return {
            "success": True,
            "data": logs,
            "total": total,
            "page": skip // limit + 1,
            "limit": limit
        }
