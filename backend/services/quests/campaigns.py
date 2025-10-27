from typing import List, Dict, Optional
from datetime import datetime
import uuid
from ...models.player.player import Player
from ...models.quests.campaign import Campaign, CampaignChapter


class CampaignService:
    """Service for managing story campaigns."""

    def __init__(self):
        self.campaign_types = self._load_campaign_types()

    def _load_campaign_types(self) -> Dict:
        """Load available campaign types."""
        return {
            "redemption_arc": {
                "title": "The Path to Redemption",
                "description": "Journey from darkness to light",
                "total_chapters": 10,
                "estimated_duration": "20-30 hours"
            },
            "fall_from_grace": {
                "title": "The Fall from Grace",
                "description": "Temptation and moral decay",
                "total_chapters": 12,
                "estimated_duration": "25-35 hours"
            },
            "rise_to_power": {
                "title": "Rise to Power",
                "description": "Climb the ranks of society",
                "total_chapters": 15,
                "estimated_duration": "30-40 hours"
            },
            "resistance": {
                "title": "The Resistance",
                "description": "Fight against oppression",
                "total_chapters": 20,
                "estimated_duration": "40-50 hours"
            }
        }

    async def get_available_campaigns(self, player_id: str) -> List[Dict]:
        """Get available campaigns for player."""
        campaigns = []
        for campaign_id, info in self.campaign_types.items():
            campaigns.append({
                "id": campaign_id,
                "campaign_type": campaign_id,
                **info
            })
        return campaigns

    async def get_active_campaign(self, player_id: str) -> Optional[Dict]:
        """Get player's active campaign."""
        player = await Player.find_one({"_id": player_id})
        if not player:
            return None

        campaign_id = player.get("active_campaign_id")
        if not campaign_id:
            return None

        return await Campaign.find_one({"_id": campaign_id})

    async def start_campaign(
        self,
        player_id: str,
        campaign_type: str
    ) -> Dict:
        """Start a new campaign."""
        player = await Player.find_one({"_id": player_id})
        if not player:
            return {"success": False, "error": "Player not found"}

        # Check if already in campaign
        if player.get("active_campaign_id"):
            return {"success": False, "error": "Already in an active campaign"}

        # Get campaign info
        campaign_info = self.campaign_types.get(campaign_type)
        if not campaign_info:
            return {"success": False, "error": "Invalid campaign type"}

        # Create campaign
        campaign_id = str(uuid.uuid4())

        # Initialize chapters
        chapters = []
        for i in range(1, campaign_info["total_chapters"] + 1):
            chapters.append(CampaignChapter(
                chapter_number=i,
                title=f"Chapter {i}",
                description=f"Chapter {i} of {campaign_info['title']}",
                quest_ids=[],
                completed=False,
                unlocked=(i == 1)  # Only first chapter unlocked
            ).dict())

        campaign = {
            "_id": campaign_id,
            "player_id": player_id,
            "campaign_type": campaign_type,
            "title": campaign_info["title"],
            "description": campaign_info["description"],
            "chapters": chapters,
            "current_chapter": 1,
            "total_chapters": campaign_info["total_chapters"],
            "status": "active",
            "started_at": datetime.utcnow(),
            "choices_made": []
        }

        await Campaign.insert_one(campaign)

        # Update player
        await Player.update_one(
            {"_id": player_id},
            {"$set": {"active_campaign_id": campaign_id}}
        )

        return {
            "success": True,
            "campaign_id": campaign_id,
            "campaign": campaign
        }

    async def get_campaign_progress(self, player_id: str) -> Optional[Dict]:
        """Get campaign progress."""
        campaign = await self.get_active_campaign(player_id)
        if not campaign:
            return None

        chapters = campaign.get("chapters", [])
        completed_chapters = sum(
            1 for ch in chapters if ch.get("completed", False))
        total_chapters = campaign.get("total_chapters", len(chapters))

        completion_percentage = (
            completed_chapters / total_chapters * 100) if total_chapters > 0 else 0

        return {
            "campaign_id": campaign.get("_id"),
            "title": campaign.get("title"),
            "current_chapter": campaign.get("current_chapter"),
            "total_chapters": total_chapters,
            "completion_percentage": completion_percentage,
            "chapters": chapters
        }

    async def make_choice(
        self,
        player_id: str,
        chapter_number: int,
        choice: str
    ) -> Dict:
        """Record a campaign choice."""
        campaign = await self.get_active_campaign(player_id)
        if not campaign:
            return {"success": False, "error": "No active campaign"}

        # Record choice
        choices_made = campaign.get("choices_made", [])
        choices_made.append({
            "chapter": chapter_number,
            "choice": choice,
            "timestamp": datetime.utcnow()
        })

        await Campaign.update_one(
            {"_id": campaign.get("_id")},
            {"$set": {"choices_made": choices_made}}
        )

        return {
            "success": True,
            "choice_recorded": choice
        }
