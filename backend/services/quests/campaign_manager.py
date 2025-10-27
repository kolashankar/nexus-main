"""Story campaign management service."""

from datetime import datetime
from typing import Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class CampaignManager:
    """Manages story campaign progression."""

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.campaigns = db.campaigns
        self.campaign_progress = db.campaign_progress
        self.players = db.players

    async def start_campaign(self, player_id: str, campaign_id: str) -> Dict:
        """Start a new campaign for player."""
        try:
            # Get campaign
            campaign = await self.campaigns.find_one({"_id": ObjectId(campaign_id)})
            if not campaign:
                raise ValueError("Campaign not found")

            # Check if already started
            existing = await self.campaign_progress.find_one({
                "player_id": player_id,
                "campaign_id": ObjectId(campaign_id)
            })

            if existing:
                return existing

            # Create progress record
            progress = {
                "player_id": player_id,
                "campaign_id": ObjectId(campaign_id),
                "status": "active",
                "started_at": datetime.utcnow(),
                "current_chapter": 0,
                "chapters_completed": 0,
                "total_chapters": len(campaign.get("chapters", [])),
                "choices_made": [],
                "branching_path": "main"
            }

            result = await self.campaign_progress.insert_one(progress)
            progress["_id"] = result.inserted_id

            return progress

        except Exception as e:
            logger.error(f"Error starting campaign: {e}")
            raise

    async def get_current_chapter(self, player_id: str, campaign_id: str) -> Optional[Dict]:
        """Get current chapter for player in campaign."""
        try:
            # Get progress
            progress = await self.campaign_progress.find_one({
                "player_id": player_id,
                "campaign_id": ObjectId(campaign_id),
                "status": "active"
            })

            if not progress:
                return None

            # Get campaign
            campaign = await self.campaigns.find_one({"_id": ObjectId(campaign_id)})
            if not campaign:
                return None

            # Get current chapter
            chapters = campaign.get("chapters", [])
            chapter_index = progress["current_chapter"]

            if chapter_index >= len(chapters):
                return None

            chapter = chapters[chapter_index]
            chapter["chapter_number"] = chapter_index + 1
            chapter["total_chapters"] = len(chapters)

            return chapter

        except Exception as e:
            logger.error(f"Error getting current chapter: {e}")
            return None

    async def make_choice(self, player_id: str, campaign_id: str, choice_id: str) -> Dict:
        """Make a choice in campaign story."""
        try:
            # Get progress
            progress = await self.campaign_progress.find_one({
                "player_id": player_id,
                "campaign_id": ObjectId(campaign_id),
                "status": "active"
            })

            if not progress:
                raise ValueError("Campaign progress not found")

            # Get campaign and chapter
            campaign = await self.campaigns.find_one({"_id": ObjectId(campaign_id)})
            chapter = campaign["chapters"][progress["current_chapter"]]

            # Find choice
            choice = None
            for c in chapter.get("choices", []):
                if c["id"] == choice_id:
                    choice = c
                    break

            if not choice:
                raise ValueError("Choice not found")

            # Record choice
            choice_record = {
                "chapter": progress["current_chapter"],
                "choice_id": choice_id,
                "choice_text": choice["text"],
                "made_at": datetime.utcnow()
            }

            # Update progress
            updates = {
                "$push": {"choices_made": choice_record}
            }

            # Check if choice affects branching
            if "branching" in choice:
                updates["$set"] = {"branching_path": choice["branching"]}

            await self.campaign_progress.update_one(
                {"_id": progress["_id"]},
                updates
            )

            # Apply consequences
            consequences = await self._apply_choice_consequences(player_id, choice)

            return {
                "choice_made": choice_record,
                "consequences": consequences,
                "next_chapter": progress["current_chapter"] + 1
            }

        except Exception as e:
            logger.error(f"Error making choice: {e}")
            raise

    async def complete_chapter(self, player_id: str, campaign_id: str) -> Dict:
        """Complete current chapter and advance to next."""
        try:
            # Get progress
            progress = await self.campaign_progress.find_one({
                "player_id": player_id,
                "campaign_id": ObjectId(campaign_id),
                "status": "active"
            })

            if not progress:
                raise ValueError("Campaign progress not found")

            # Advance chapter
            next_chapter = progress["current_chapter"] + 1
            chapters_completed = progress["chapters_completed"] + 1

            updates = {
                "current_chapter": next_chapter,
                "chapters_completed": chapters_completed
            }

            # Check if campaign completed
            if next_chapter >= progress["total_chapters"]:
                updates["status"] = "completed"
                updates["completed_at"] = datetime.utcnow()

            await self.campaign_progress.update_one(
                {"_id": progress["_id"]},
                {"$set": updates}
            )

            # Get updated progress
            updated = await self.campaign_progress.find_one({"_id": progress["_id"]})

            return updated

        except Exception as e:
            logger.error(f"Error completing chapter: {e}")
            raise

    async def _apply_choice_consequences(self, player_id: str, choice: Dict) -> Dict:
        """Apply consequences of player's choice."""
        try:
            consequences = choice.get("consequences", {})
            applied = {}

            # Karma changes
            if "karma" in consequences:
                await self.players.update_one(
                    {"_id": player_id},
                    {"$inc": {"karma_points": consequences["karma"]}}
                )
                applied["karma"] = consequences["karma"]

            # Trait changes
            if "traits" in consequences:
                for trait, change in consequences["traits"].items():
                    player = await self.players.find_one({"_id": player_id})
                    current = player["traits"].get(trait, 0)
                    new_value = max(0, min(100, current + change))

                    await self.players.update_one(
                        {"_id": player_id},
                        {"$set": {f"traits.{trait}": new_value}}
                    )
                    applied[f"trait_{trait}"] = change

            # Rewards
            if "rewards" in consequences:
                from .rewards import RewardDistributor
                distributor = RewardDistributor(self.db)
                rewards = await distributor.distribute_rewards(player_id, consequences["rewards"])
                applied["rewards"] = rewards

            return applied

        except Exception as e:
            logger.error(f"Error applying consequences: {e}")
            return {}

    async def get_player_campaigns(self, player_id: str, status: Optional[str] = None) -> List[Dict]:
        """Get player's campaigns."""
        try:
            query = {"player_id": player_id}
            if status:
                query["status"] = status

            campaigns = await self.campaign_progress.find(query).to_list(None)

            # Enrich with campaign data
            enriched = []
            for progress in campaigns:
                campaign = await self.campaigns.find_one({"_id": progress["campaign_id"]})
                if campaign:
                    progress["campaign_title"] = campaign.get("title")
                    progress["campaign_description"] = campaign.get(
                        "description")
                    enriched.append(progress)

            return enriched

        except Exception as e:
            logger.error(f"Error getting player campaigns: {e}")
            return []
