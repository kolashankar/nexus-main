from datetime import datetime
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.social.relationship import Mentorship


class MentorshipService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.mentorships = db.mentorships
        self.players = db.players

    async def request_mentorship(self, apprentice_id: str, mentor_id: str) -> dict:
        """Request mentorship (creates pending request)"""
        if apprentice_id == mentor_id:
            raise ValueError("Cannot mentor yourself")

        # Check if apprentice already has a mentor
        existing = await self.mentorships.find_one({
            "apprentice_id": apprentice_id,
            "active": True
        })

        if existing:
            raise ValueError("Already have a mentor")

        # Check mentor level (must be at least level 50)
        mentor = await self.players.find_one({"_id": mentor_id})
        if not mentor or mentor.get("level", 0) < 50:
            raise ValueError("Mentor must be at least level 50")

        # Create pending request
        request = {
            "apprentice_id": apprentice_id,
            "mentor_id": mentor_id,
            "requested_at": datetime.utcnow(),
            "status": "pending"
        }

        await self.db.mentorship_requests.insert_one(request)

        return request

    async def accept_mentorship(self, request_id: str) -> Mentorship:
        """Accept mentorship request"""
        request = await self.db.mentorship_requests.find_one({"_id": request_id})
        if not request:
            raise ValueError("Request not found")

        if request.get("status") != "pending":
            raise ValueError("Request is not pending")

        # Get apprentice level
        apprentice = await self.players.find_one({"_id": request.get("apprentice_id")})

        # Create mentorship
        mentorship = Mentorship(
            mentor_id=request.get("mentor_id"),
            apprentice_id=request.get("apprentice_id"),
            apprentice_level=apprentice.get("level", 1) if apprentice else 1
        )

        await self.mentorships.insert_one(mentorship.model_dump())

        # Update players
        await self.players.update_one(
            {"_id": mentorship.mentor_id},
            {"$push": {"apprentices": mentorship.apprentice_id}}
        )

        await self.players.update_one(
            {"_id": mentorship.apprentice_id},
            {"$set": {"mentor_id": mentorship.mentor_id}}
        )

        # Mark request as accepted
        await self.db.mentorship_requests.update_one(
            {"_id": request_id},
            {"$set": {"status": "accepted"}}
        )

        return mentorship

    async def reject_mentorship(self, request_id: str) -> bool:
        """Reject mentorship request"""
        await self.db.mentorship_requests.update_one(
            {"_id": request_id},
            {"$set": {"status": "rejected"}}
        )
        return True

    async def graduate_apprentice(self, mentorship_id: str) -> bool:
        """Graduate apprentice (they reached level 50)"""
        mentorship = await self.mentorships.find_one({"id": mentorship_id})
        if not mentorship:
            raise ValueError("Mentorship not found")

        if not mentorship.get("active"):
            raise ValueError("Mentorship is not active")

        # Check apprentice level
        apprentice = await self.players.find_one({"_id": mentorship.get("apprentice_id")})
        if not apprentice or apprentice.get("level", 0) < 50:
            raise ValueError(
                "Apprentice must be at least level 50 to graduate")

        # End mentorship
        await self.mentorships.update_one(
            {"id": mentorship_id},
            {
                "$set": {
                    "active": False,
                    "graduated_at": datetime.utcnow()
                }
            }
        )

        # Update players
        await self.players.update_one(
            {"_id": mentorship.get("mentor_id")},
            {
                "$pull": {"apprentices": mentorship.get("apprentice_id")},
                "$inc": {"legacy_points": 100}  # Reward for graduation
            }
        )

        await self.players.update_one(
            {"_id": mentorship.get("apprentice_id")},
            {"$unset": {"mentor_id": ""}}
        )

        return True

    async def complete_lesson(self, mentorship_id: str) -> bool:
        """Complete a lesson (awards progress)"""
        mentorship = await self.mentorships.find_one({"id": mentorship_id})
        if not mentorship:
            raise ValueError("Mentorship not found")

        # Update lesson count and rewards
        await self.mentorships.update_one(
            {"id": mentorship_id},
            {
                "$inc": {
                    "lessons_completed": 1,
                    "mentor_legacy_points": 5
                }
            }
        )

        # Award mentor legacy points
        await self.players.update_one(
            {"_id": mentorship.get("mentor_id")},
            {"$inc": {"legacy_points": 5}}
        )

        return True

    async def get_mentorship(self, mentorship_id: str) -> Optional[dict]:
        """Get mentorship by ID"""
        return await self.mentorships.find_one({"id": mentorship_id})

    async def get_player_mentorship(self, player_id: str, as_mentor: bool = False) -> Optional[dict]:
        """Get player's active mentorship"""
        if as_mentor:
            # Get one of the mentorships where player is mentor
            return await self.mentorships.find_one({
                "mentor_id": player_id,
                "active": True
            })
        else:
            # Get mentorship where player is apprentice
            return await self.mentorships.find_one({
                "apprentice_id": player_id,
                "active": True
            })

    async def get_pending_requests(self, player_id: str) -> List[dict]:
        """Get pending mentorship requests"""
        cursor = self.db.mentorship_requests.find({
            "mentor_id": player_id,
            "status": "pending"
        })
        return await cursor.to_list(length=100)

    async def list_mentors(self, skip: int = 0, limit: int = 20) -> List[dict]:
        """List available mentors (level 50+)"""
        cursor = self.players.find({
            "level": {"$gte": 50}
        }).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
