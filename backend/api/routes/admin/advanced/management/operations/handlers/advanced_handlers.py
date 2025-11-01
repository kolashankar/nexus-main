from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional, List
from datetime import datetime
from bson import ObjectId

class ContentApprovalHandlers:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.content_submissions = db["content_submissions"]
        self.jobs = db["jobs"]
        self.internships = db["internships"]
        self.articles = db["articles"]
    
    async def submit_content_for_approval(self, content_type: str, content_data: Dict, submitted_by: str) -> Dict:
        """Submit content for admin approval"""
        submission = {
            "content_type": content_type,  # jobs, internships, articles, etc.
            "content_data": content_data,
            "submitted_by": submitted_by,
            "status": "pending",  # pending, approved, rejected
            "submitted_at": datetime.utcnow(),
            "reviewed_by": None,
            "reviewed_at": None,
            "review_notes": None
        }
        
        result = await self.content_submissions.insert_one(submission)
        
        return {
            "success": True,
            "data": {
                "id": str(result.inserted_id),
                "status": "pending",
                "message": "Content submitted for approval"
            }
        }
    
    async def get_pending_submissions(self, content_type: Optional[str] = None, limit: int = 50, skip: int = 0) -> Dict:
        """Get all pending content submissions"""
        query = {"status": "pending"}
        if content_type:
            query["content_type"] = content_type
        
        submissions_cursor = self.content_submissions.find(query).sort("submitted_at", -1).skip(skip).limit(limit)
        submissions = []
        
        async for submission in submissions_cursor:
            submission["_id"] = str(submission["_id"])
            submission["submitted_at"] = submission["submitted_at"].isoformat()
            submissions.append(submission)
        
        total = await self.content_submissions.count_documents(query)
        
        return {
            "success": True,
            "data": submissions,
            "total": total,
            "page": skip // limit + 1,
            "limit": limit
        }
    
    async def approve_submission(self, submission_id: str, reviewed_by: str, review_notes: Optional[str] = None) -> Dict:
        """Approve a content submission and publish it"""
        try:
            submission = await self.content_submissions.find_one({"_id": ObjectId(submission_id)})
            
            if not submission:
                return {"success": False, "error": "Submission not found"}
            
            if submission["status"] != "pending":
                return {"success": False, "error": "Submission already reviewed"}
            
            # Insert content into respective collection
            content_type = submission["content_type"]
            content_data = submission["content_data"]
            
            if content_type == "jobs":
                await self.jobs.insert_one(content_data)
            elif content_type == "internships":
                await self.internships.insert_one(content_data)
            elif content_type == "articles":
                await self.articles.insert_one(content_data)
            
            # Update submission status
            await self.content_submissions.update_one(
                {"_id": ObjectId(submission_id)},
                {
                    "$set": {
                        "status": "approved",
                        "reviewed_by": reviewed_by,
                        "reviewed_at": datetime.utcnow(),
                        "review_notes": review_notes
                    }
                }
            )
            
            return {
                "success": True,
                "data": {
                    "message": "Content approved and published"
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def reject_submission(self, submission_id: str, reviewed_by: str, review_notes: str) -> Dict:
        """Reject a content submission"""
        try:
            result = await self.content_submissions.update_one(
                {"_id": ObjectId(submission_id), "status": "pending"},
                {
                    "$set": {
                        "status": "rejected",
                        "reviewed_by": reviewed_by,
                        "reviewed_at": datetime.utcnow(),
                        "review_notes": review_notes
                    }
                }
            )
            
            if result.modified_count == 0:
                return {"success": False, "error": "Submission not found or already reviewed"}
            
            return {
                "success": True,
                "data": {
                    "message": "Content rejected"
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_submission_stats(self) -> Dict:
        """Get content approval statistics"""
        total_pending = await self.content_submissions.count_documents({"status": "pending"})
        total_approved = await self.content_submissions.count_documents({"status": "approved"})
        total_rejected = await self.content_submissions.count_documents({"status": "rejected"})
        
        # By content type
        pipeline = [
            {"$group": {"_id": {"type": "$content_type", "status": "$status"}, "count": {"$sum": 1}}}
        ]
        
        stats_cursor = self.content_submissions.aggregate(pipeline)
        by_type = {}
        async for stat in stats_cursor:
            content_type = stat["_id"]["type"]
            status = stat["_id"]["status"]
            
            if content_type not in by_type:
                by_type[content_type] = {"pending": 0, "approved": 0, "rejected": 0}
            
            by_type[content_type][status] = stat["count"]
        
        return {
            "success": True,
            "data": {
                "total_pending": total_pending,
                "total_approved": total_approved,
                "total_rejected": total_rejected,
                "by_content_type": by_type
            }
        }


class PushNotificationHandlers:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.push_notifications = db["push_notifications"]
        self.notification_logs = db["notification_logs"]
    
    async def create_notification(self, title: str, message: str, target: str, target_ids: Optional[List[str]] = None, data: Optional[Dict] = None, scheduled_at: Optional[datetime] = None) -> Dict:
        """Create a push notification"""
        notification = {
            "title": title,
            "message": message,
            "target": target,  # all, specific_users, admins
            "target_ids": target_ids or [],
            "data": data or {},
            "status": "pending",  # pending, sent, failed
            "scheduled_at": scheduled_at or datetime.utcnow(),
            "created_at": datetime.utcnow(),
            "sent_at": None,
            "sent_count": 0,
            "failed_count": 0
        }
        
        result = await self.push_notifications.insert_one(notification)
        
        return {
            "success": True,
            "data": {
                "id": str(result.inserted_id),
                "status": "pending"
            }
        }
    
    async def get_notifications(self, status: Optional[str] = None, limit: int = 50, skip: int = 0) -> Dict:
        """Get push notifications with optional status filter"""
        query = {}
        if status:
            query["status"] = status
        
        notifications_cursor = self.push_notifications.find(query).sort("created_at", -1).skip(skip).limit(limit)
        notifications = []
        
        async for notification in notifications_cursor:
            notification["_id"] = str(notification["_id"])
            notification["created_at"] = notification["created_at"].isoformat()
            notification["scheduled_at"] = notification["scheduled_at"].isoformat() if notification.get("scheduled_at") else None
            notification["sent_at"] = notification["sent_at"].isoformat() if notification.get("sent_at") else None
            notifications.append(notification)
        
        total = await self.push_notifications.count_documents(query)
        
        return {
            "success": True,
            "data": notifications,
            "total": total,
            "page": skip // limit + 1,
            "limit": limit
        }
    
    async def send_notification(self, notification_id: str) -> Dict:
        """Send a push notification (mock implementation)"""
        try:
            notification = await self.push_notifications.find_one({"_id": ObjectId(notification_id)})
            
            if not notification:
                return {"success": False, "error": "Notification not found"}
            
            # Mock sending logic (in real app, integrate with Firebase/OneSignal/etc.)
            sent_count = len(notification.get("target_ids", [])) if notification["target"] == "specific_users" else 100
            
            # Update notification status
            await self.push_notifications.update_one(
                {"_id": ObjectId(notification_id)},
                {
                    "$set": {
                        "status": "sent",
                        "sent_at": datetime.utcnow(),
                        "sent_count": sent_count,
                        "failed_count": 0
                    }
                }
            )
            
            # Log the notification
            await self.notification_logs.insert_one({
                "notification_id": notification_id,
                "sent_count": sent_count,
                "failed_count": 0,
                "sent_at": datetime.utcnow()
            })
            
            return {
                "success": True,
                "data": {
                    "message": "Notification sent",
                    "sent_count": sent_count
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def delete_notification(self, notification_id: str) -> Dict:
        """Delete a push notification"""
        try:
            result = await self.push_notifications.delete_one({"_id": ObjectId(notification_id)})
            
            if result.deleted_count == 0:
                return {"success": False, "error": "Notification not found"}
            
            return {
                "success": True,
                "data": {
                    "message": "Notification deleted"
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_notification_stats(self) -> Dict:
        """Get push notification statistics"""
        total_sent = await self.push_notifications.count_documents({"status": "sent"})
        total_pending = await self.push_notifications.count_documents({"status": "pending"})
        total_failed = await self.push_notifications.count_documents({"status": "failed"})
        
        # Total recipients reached
        pipeline = [
            {"$match": {"status": "sent"}},
            {"$group": {"_id": None, "total_recipients": {"$sum": "$sent_count"}}}
        ]
        
        recipients_cursor = self.push_notifications.aggregate(pipeline)
        total_recipients = 0
        async for stat in recipients_cursor:
            total_recipients = stat.get("total_recipients", 0)
        
        return {
            "success": True,
            "data": {
                "total_sent": total_sent,
                "total_pending": total_pending,
                "total_failed": total_failed,
                "total_recipients_reached": total_recipients
            }
        }
