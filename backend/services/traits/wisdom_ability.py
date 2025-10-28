"""Wisdom meta trait ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional, List
import random
from datetime import datetime

class WisdomAbility:
    """Implementation of Wisdom meta trait - Sage Insight ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def sage_insight(
        self,
        player_id: str,
        situation_type: str,
        trait_level: int
    ) -> Dict:
        """Gain wisdom-based insight into situations and optimal paths.
        
        Args:
            player_id: ID of wise player
            situation_type: Type of situation (combat, social, economic, strategic)
            trait_level: Wisdom trait level (1-100)
        
        Returns:
            Dict with success, insights, recommendations, message
        """
        
        # Get player
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {
                "success": False,
                "insights": [],
                "message": "Player not found"
            }
        
        # Calculate insight quality based on trait level
        insight_quality = trait_level  # 1-100
        
        insights = []
        recommendations = []
        
        # Provide insights based on situation type
        if situation_type == "combat":
            insights.extend(self._get_combat_insights(player, insight_quality))
        elif situation_type == "social":
            insights.extend(self._get_social_insights(player, insight_quality))
        elif situation_type == "economic":
            insights.extend(self._get_economic_insights(player, insight_quality))
        elif situation_type == "strategic":
            insights.extend(self._get_strategic_insights(player, insight_quality))
        else:
            insights.append("Unknown situation type")
        
        # Apply wisdom buff (enhanced learning and XP)
        duration = 300 + int((trait_level / 100) * 300)  # 5-10 minutes
        
        buff_data = {
            "type": "sage_insight",
            "xp_boost_percent": 25 + int((trait_level / 100) * 25),  # 25-50% XP boost
            "skill_learning_boost_percent": 30,
            "wisdom_bonus": True,
            "expires_at": datetime.utcnow().timestamp() + duration,
            "source_trait": "wisdom",
            "visual_effect": "ethereal_glow"
        }
        
        await self.db.players.update_one(
            {"_id": player_id},
            {"$push": {"buffs": buff_data}}
        )
        
        # Moderate karma gain (wisdom is virtuous)
        karma_gain = random.randint(5, 10)
        await self.db.players.update_one(
            {"_id": player_id},
            {"$inc": {"karma.current": karma_gain}}
        )
        
        return {
            "success": True,
            "insights": insights,
            "recommendations": recommendations,
            "xp_boost": 25 + int((trait_level / 100) * 25),
            "duration": duration,
            "karma_gain": karma_gain,
            "message": f"Sage Insight activated! {len(insights)} insights gained"
        }
    
    def _get_combat_insights(self, player: Dict, quality: int) -> List[str]:
        """Generate combat insights based on player stats."""
        insights = []
        stats = player.get("stats", {})
        
        if quality >= 20:
            insights.append(f"Your combat rating: {stats.get('combat_rating', 50)}/100")
        
        if quality >= 40:
            if stats.get("defense", 50) < 40:
                insights.append("⚠️ Low defense detected. Consider defensive traits or armor.")
            if stats.get("speed", 50) > 70:
                insights.append("✓ High speed advantage. Use hit-and-run tactics.")
        
        if quality >= 60:
            insights.append("Strategic positioning is key. Use terrain to your advantage.")
        
        if quality >= 80:
            insights.append("Advanced Tip: Chain abilities for combo damage bonuses.")
        
        return insights
    
    def _get_social_insights(self, player: Dict, quality: int) -> List[str]:
        """Generate social insights."""
        insights = []
        karma = player.get("karma", {}).get("current", 50)
        
        if quality >= 20:
            insights.append(f"Your karma: {karma}/100 - {self._get_karma_alignment(karma)}")
        
        if quality >= 40:
            if karma < 40:
                insights.append("⚠️ Low karma may limit positive social interactions.")
            elif karma > 70:
                insights.append("✓ High karma opens doors to virtuous opportunities.")
        
        if quality >= 60:
            insights.append("Reputation with factions affects available quests and rewards.")
        
        if quality >= 80:
            insights.append("Advanced Tip: Balance multiple faction relationships for maximum benefit.")
        
        return insights
    
    def _get_economic_insights(self, player: Dict, quality: int) -> List[str]:
        """Generate economic insights."""
        insights = []
        credits = player.get("economy", {}).get("credits", 0)
        
        if quality >= 20:
            insights.append(f"Current credits: {credits}")
        
        if quality >= 40:
            insights.append("💡 Diversify income: trading, quests, and investments.")
        
        if quality >= 60:
            insights.append("Market timing is crucial. Buy low during off-peak hours.")
        
        if quality >= 80:
            insights.append("Advanced Tip: High-risk investments in rare traits can yield 300%+ returns.")
        
        return insights
    
    def _get_strategic_insights(self, player: Dict, quality: int) -> List[str]:
        """Generate strategic insights."""
        insights = []
        level = player.get("level", 1)
        
        if quality >= 20:
            insights.append(f"Player level: {level}")
        
        if quality >= 40:
            insights.append("⚡ Focus on synergistic trait combinations for multiplicative benefits.")
        
        if quality >= 60:
            insights.append("Long-term strategy: Specialize in 2-3 trait trees for mastery bonuses.")
        
        if quality >= 80:
            insights.append("Advanced Tip: Meta traits amplify your primary abilities exponentially.")
        
        return insights
    
    def _get_karma_alignment(self, karma: int) -> str:
        """Get karma alignment description."""
        if karma >= 80:
            return "Saint"
        elif karma >= 60:
            return "Good"
        elif karma >= 40:
            return "Neutral"
        elif karma >= 20:
            return "Evil"
        else:
            return "Corrupted"
    
    async def learning_acceleration(
        self,
        player_id: str,
        skill_name: str,
        trait_level: int
    ) -> Dict:
        """Passive ability: Learn skills and traits faster.
        
        Args:
            player_id: ID of player
            skill_name: Name of skill being learned
            trait_level: Wisdom trait level (1-100)
        
        Returns:
            Dict with success, xp_multiplier, message
        """
        
        # Calculate XP multiplier (1.1x to 2.0x based on trait level)
        min_multiplier = 1.1
        max_multiplier = 2.0
        xp_multiplier = min_multiplier + (trait_level / 100) * (max_multiplier - min_multiplier)
        
        return {
            "success": True,
            "xp_multiplier": round(xp_multiplier, 2),
            "skill_name": skill_name,
            "message": f"Wisdom accelerates {skill_name} learning by {round((xp_multiplier - 1) * 100)}%"
        }
