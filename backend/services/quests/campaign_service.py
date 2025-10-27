"""Campaign service - Story campaign management"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

from ...models.quests.campaign import CampaignType


class CampaignService:
    """Manages story campaigns"""

    def __init__(self, db):
        self.db = db
        self.campaigns = db.campaigns
        self.players = db.players

    async def get_campaign(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get campaign by ID"""
        return await self.campaigns.find_one({"_id": campaign_id})

    async def get_player_campaigns(
        self,
        player_id: str,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get player's campaigns"""
        query = {"player_id": player_id}
        if status:
            query["status"] = status

        cursor = self.campaigns.find(query)
        return await cursor.to_list(length=100)

    async def get_available_campaigns(
        self,
        player_id: str,
        player: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Get campaigns available to player"""
        # Check player's karma and level
        player_karma = player.get("karma_points", 0)
        player.get("level", 1)

        # Determine suitable campaign types
        suitable_types = []
        if player_karma < -500:
            suitable_types.append(CampaignType.REDEMPTION)
        elif player_karma > 500:
            suitable_types.append(CampaignType.FALL_FROM_GRACE)
        else:
            suitable_types.append(CampaignType.NEUTRAL_PATH)

        # Always add other types
        suitable_types.extend([
            CampaignType.POWER_QUEST,
            CampaignType.ORIGIN_STORY,
            CampaignType.MYSTERY,
        ])

        # Get campaigns not yet started
        existing = await self.get_player_campaigns(player_id)
        existing_types = [c.get("campaign_type") for c in existing]

        available = []
        for ctype in suitable_types:
            if ctype not in existing_types:
                available.append({
                    "campaign_type": ctype,
                    "available": True,
                })

        return available

    async def start_campaign(
        self,
        player_id: str,
        player: Dict[str, Any],
        campaign_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Start a new campaign"""
        # TODO: Use Oracle AI to generate campaign
        # For now, create a basic campaign structure

        campaign_id = str(uuid.uuid4())

        campaign = {
            "_id": campaign_id,
            "campaign_type": campaign_type or "origin_story",
            "title": "Your Origin Story",
            "subtitle": "The Beginning",
            "description": "Discover your past and shape your future",
            "synopsis": "A journey of self-discovery awaits",
            "player_id": player_id,
            "total_chapters": 10,
            "chapters": [],
            "current_chapter": 1,
            "requirements": {
                "min_level": 1,
                "min_karma": None,
                "max_karma": None,
                "required_traits": {},
                "required_campaigns": [],
            },
            "rewards": {
                "credits": 5000,
                "xp": 2000,
                "karma": 100,
                "trait_boosts": {},
                "unlock_power": None,
                "unlock_title": "Origin Seeker",
                "special_item": None,
            },
            "status": "in_progress",
            "generated_by": "oracle",
            "generated_at": datetime.utcnow(),
            "seed": None,
            "started_at": datetime.utcnow(),
            "completed_at": None,
            "choices_history": [],
            "branching_path": "main",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        await self.campaigns.insert_one(campaign)
        return campaign

    async def make_choice(
        self,
        campaign_id: str,
        choice_id: str,
        option_id: str,
        player_id: str,
    ) -> Dict[str, Any]:
        """Make a choice in campaign"""
        campaign = await self.get_campaign(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")

        if campaign["player_id"] != player_id:
            raise ValueError("Not your campaign")

        # Record choice
        choice_record = {
            "choice_id": choice_id,
            "option_id": option_id,
            "made_at": datetime.utcnow(),
        }

        await self.campaigns.update_one(
            {"_id": campaign_id},
            {
                "$push": {"choices_history": choice_record},
                "$set": {"updated_at": datetime.utcnow()},
            }
        )

        return {
            "success": True,
            "message": "Choice recorded",
            "choice": choice_record,
        }

    async def advance_chapter(
        self,
        campaign_id: str,
        player_id: str,
    ) -> Dict[str, Any]:
        """Advance to next chapter"""
        campaign = await self.get_campaign(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")

        if campaign["player_id"] != player_id:
            raise ValueError("Not your campaign")

        current_chapter = campaign["current_chapter"]
        total_chapters = campaign["total_chapters"]

        if current_chapter >= total_chapters:
            # Campaign completed
            await self.campaigns.update_one(
                {"_id": campaign_id},
                {
                    "$set": {
                        "status": "completed",
                        "completed_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow(),
                    }
                }
            )
            return {
                "success": True,
                "message": "Campaign completed!",
                "completed": True,
            }

        # Advance chapter
        await self.campaigns.update_one(
            {"_id": campaign_id},
            {
                "$inc": {"current_chapter": 1},
                "$set": {"updated_at": datetime.utcnow()},
            }
        )

        return {
            "success": True,
            "message": "Advanced to next chapter",
            "current_chapter": current_chapter + 1,
            "completed": False,
        }
