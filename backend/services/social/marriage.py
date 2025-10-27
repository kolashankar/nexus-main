from datetime import datetime
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.social.relationship import Marriage


class MarriageService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.marriages = db.marriages
        self.players = db.players

    async def propose_marriage(self, proposer_id: str, proposed_to_id: str) -> dict:
        """Propose marriage (creates a pending proposal)"""
        if proposer_id == proposed_to_id:
            raise ValueError("Cannot marry yourself")

        # Check if already married
        existing = await self.marriages.find_one({
            "$or": [
                {"player1_id": proposer_id, "active": True},
                {"player2_id": proposer_id, "active": True}
            ]
        })

        if existing:
            raise ValueError("Already married")

        # Check if partner is married
        partner_married = await self.marriages.find_one({
            "$or": [
                {"player1_id": proposed_to_id, "active": True},
                {"player2_id": proposed_to_id, "active": True}
            ]
        })

        if partner_married:
            raise ValueError("Partner is already married")

        # Create pending proposal
        proposal = {
            "proposer_id": proposer_id,
            "proposed_to_id": proposed_to_id,
            "proposed_at": datetime.utcnow(),
            "status": "pending"
        }

        await self.db.marriage_proposals.insert_one(proposal)

        return proposal

    async def accept_proposal(self, proposal_id: str) -> Marriage:
        """Accept marriage proposal"""
        proposal = await self.db.marriage_proposals.find_one({"_id": proposal_id})
        if not proposal:
            raise ValueError("Proposal not found")

        if proposal.get("status") != "pending":
            raise ValueError("Proposal is not pending")

        # Create marriage
        marriage = Marriage(
            player1_id=proposal.get("proposer_id"),
            player2_id=proposal.get("proposed_to_id")
        )

        await self.marriages.insert_one(marriage.model_dump())

        # Update players
        await self.players.update_one(
            {"_id": marriage.player1_id},
            {"$set": {"spouse_id": marriage.player2_id}}
        )

        await self.players.update_one(
            {"_id": marriage.player2_id},
            {"$set": {"spouse_id": marriage.player1_id}}
        )

        # Mark proposal as accepted
        await self.db.marriage_proposals.update_one(
            {"_id": proposal_id},
            {"$set": {"status": "accepted"}}
        )

        return marriage

    async def reject_proposal(self, proposal_id: str) -> bool:
        """Reject marriage proposal"""
        await self.db.marriage_proposals.update_one(
            {"_id": proposal_id},
            {"$set": {"status": "rejected"}}
        )
        return True

    async def divorce(self, marriage_id: str, initiator_id: str) -> bool:
        """Divorce (ends marriage with karma penalty)"""
        marriage = await self.marriages.find_one({"id": marriage_id})
        if not marriage:
            raise ValueError("Marriage not found")

        if not marriage.get("active"):
            raise ValueError("Marriage is not active")

        # End marriage
        await self.marriages.update_one(
            {"id": marriage_id},
            {
                "$set": {
                    "active": False,
                    "divorced_at": datetime.utcnow()
                }
            }
        )

        # Update players
        await self.players.update_one(
            {"_id": marriage.get("player1_id")},
            {"$unset": {"spouse_id": ""}}
        )

        await self.players.update_one(
            {"_id": marriage.get("player2_id")},
            {"$unset": {"spouse_id": ""}}
        )

        # Apply karma penalty to initiator
        await self.players.update_one(
            {"_id": initiator_id},
            {"$inc": {"karma_points": -50}}  # Divorce penalty
        )

        return True

    async def get_marriage(self, marriage_id: str) -> Optional[dict]:
        """Get marriage by ID"""
        return await self.marriages.find_one({"id": marriage_id})

    async def get_player_marriage(self, player_id: str) -> Optional[dict]:
        """Get player's active marriage"""
        return await self.marriages.find_one({
            "$or": [
                {"player1_id": player_id},
                {"player2_id": player_id}
            ],
            "active": True
        })

    async def get_pending_proposals(self, player_id: str) -> List[dict]:
        """Get pending proposals for a player"""
        cursor = self.db.marriage_proposals.find({
            "proposed_to_id": player_id,
            "status": "pending"
        })
        return await cursor.to_list(length=100)

    async def update_joint_karma(self, marriage_id: str, karma: int) -> bool:
        """Update joint karma pool"""
        await self.marriages.update_one(
            {"id": marriage_id},
            {"$inc": {"joint_karma": karma}}
        )
        return True
