from typing import Dict
from datetime import datetime


class QuestNotificationService:
    """Service for quest-related notifications."""

    def create_quest_available_notification(self, quest: Dict) -> Dict:
        """Create notification for new quest availability."""
        return {
            "type": "quest_available",
            "title": "New Quest Available",
            "message": f"A new quest is available: {quest.get('title')}",
            "quest_id": quest.get('_id'),
            "priority": "medium",
            "timestamp": datetime.utcnow()
        }

    def create_quest_completed_notification(self, quest: Dict, rewards: Dict) -> Dict:
        """Create notification for quest completion."""
        reward_text = []
        if rewards.get("credits"):
            reward_text.append(f"+{rewards['credits']} credits")
        if rewards.get("xp"):
            reward_text.append(f"+{rewards['xp']} XP")
        if rewards.get("karma"):
            reward_text.append(f"+{rewards['karma']} karma")

        return {
            "type": "quest_completed",
            "title": "Quest Completed!",
            "message": f"You completed '{quest.get('title')}'. Rewards: {', '.join(reward_text)}",
            "quest_id": quest.get('_id'),
            "priority": "high",
            "timestamp": datetime.utcnow()
        }

    def create_quest_failed_notification(self, quest: Dict) -> Dict:
        """Create notification for quest failure."""
        return {
            "type": "quest_failed",
            "title": "Quest Failed",
            "message": f"Quest '{quest.get('title')}' has failed or expired.",
            "quest_id": quest.get('_id'),
            "priority": "medium",
            "timestamp": datetime.utcnow()
        }

    def create_objective_progress_notification(self, quest: Dict, objective: Dict) -> Dict:
        """Create notification for objective progress."""
        return {
            "type": "objective_progress",
            "title": "Quest Progress",
            "message": f"{objective.get('description')}: {objective.get('current')}/{objective.get('required')}",
            "quest_id": quest.get('_id'),
            "priority": "low",
            "timestamp": datetime.utcnow()
        }

    def create_daily_reset_notification(self) -> Dict:
        """Create notification for daily quest reset."""
        return {
            "type": "daily_reset",
            "title": "Daily Quests Reset",
            "message": "New daily quests are now available!",
            "priority": "medium",
            "timestamp": datetime.utcnow()
        }

    def create_hidden_quest_discovered_notification(self, quest: Dict) -> Dict:
        """Create notification for hidden quest discovery."""
        return {
            "type": "hidden_quest_discovered",
            "title": "Secret Discovered!",
            "message": f"You discovered a hidden quest: {quest.get('title')}",
            "quest_id": quest.get('_id'),
            "priority": "high",
            "timestamp": datetime.utcnow()
        }
